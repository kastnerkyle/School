#!/usr/bin/python
#Attempt to apply spectral correlation function to data and plot 3D
#http://www.johnvinyard.com/blog/?p=268
import scipy.io.wavfile as wavfile
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plot
from matplotlib import cm
from numpy.lib.stride_tricks import as_strided as ast
import copy
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as st

parser = argparse.ArgumentParser(description="Apply ")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-n", "--noplot", dest="noplot", action="store_true", help="WAV file to be processed")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")
parser.add_argument("-s", "--specgram", dest="specgram", action="store_true", help="Show spectrogram of input wavefile")
parser.add_argument("-c", "--coherence", dest="coherence", action="store_true", help="Plot cyclic coherence of input")
parser.add_argument("-f", "--fft", type=int, dest="fft", action="store", default=1024, help="Optionally set FFT size, default is 1024")

def run_specgram():
    sr, data = wavfile.read(args.filename)
    data = np.asarray(data, dtype=np.int16)
    vec_len, = data.shape
    fft_size = args.fft
    if args.verbose > 0:
        print `args.filename` + " has shape of " + `data.shape`
        print `args.filename` + " has sample rate of " + `sr`
    leftover = vec_len%fft_size
    if leftover != 0:
        data = np.hstack((data, np.zeros(fft_size-leftover)))
        vec_len, = data.shape
        if args.verbose > 0:
            print "FFT size chosen is " + `fft_size` + " bins"
            print "FFT size does not match data shape, resizing by appending zeros"
            print "Adding " + `fft_size-leftover` + " zeros to data"

    time_aligned = data.reshape((vec_len/fft_size, fft_size))
    if args.verbose > 0:
        print "Resizing data to match chosen FFT size"
        print "Resized data now has shape of " + `time_aligned.shape`

        fft = np.fft.fftn(time_aligned, s=(fft_size,), axes=(1,))
        if args.verbose:
            print "Calculating spectrogram"
            print "Size of FFT specrogram data " + `fft.shape`
        if not args.noplot:
            plot.imshow(abs(fft))
            plot.show()
        else:
            print "No plot option chosen, skipping plot..."
            print "Exiting, spectrogram complete!"
            sys.exit()

def alpha_run(d1, d2, alpha, beta):
    if d1.shape != d2.shape:
        print "Items to be correlated do not have the same dimensions!"
        sys.exit()
    vec_len, = d1.shape
    spacing = d1.itemsize
    block = args.fft/2
    #Need 67% overlap for SCF using Hann window according to Cyclic Spectral Analysis in Practice - Jerome Antoni
    increment = int(block*.33)
    #Add extra zeros for tail end in order to avoid junk data - must keep dtype as int16 - otherwise weird broadcasting rules will take over...
    #http://www.utc.fr/~antoni/programm.htm
    d1 = np.hstack((d1, np.zeros(block, dtype=np.complex64)))
    d2 = np.hstack((d2, np.zeros(block, dtype=np.complex64)))
    t = np.arange(0,d1.shape[0])
    plus_alpha = np.asarray([np.exp(1j*np.pi*alpha*beta*n) for n in t], dtype=np.complex64)
    minus_alpha = np.asarray([np.exp(-1j*np.pi*alpha*beta*n) for n in t], dtype=np.complex64)
    x = d1*minus_alpha
    y = d2*plus_alpha
    def overlap(d):
        return ast(d, shape=(vec_len/increment,block), strides=(increment*spacing, spacing))
    window = np.hanning(block)
    Xconj = np.conjugate(np.fft.fftn(overlap(x)*window, s=(args.fft,), axes=(1,)))
    Y = np.fft.fftn(overlap(y)*window, s=(args.fft,), axes=(1,))
    normalizing_factor = Y.shape[0]*np.linalg.norm(window)**2
    return (np.sum(Xconj*Y, axis=0, dtype=np.complex64)/float(normalizing_factor), window, increment)

def run_cyclic_coherence():
    significance = .01
    P = significance
    sr, data = wavfile.read(args.filename)
    data = np.asarray(data[0:1000], dtype=np.complex64)
    coh = None
    start_alpha = 1
    stop_alpha = 500
    step_alpha = 1
    alphas = range(start_alpha, stop_alpha, step_alpha)
    alphas = [ 1./x if x !=0 else None for x in alphas ]
    alphas = filter(lambda x: x != None, alphas)
    #http://stackoverflow.com/questions/9152958/matplotlib-3d-plot-2d-format-for-input-data
    beta = .5
    max_step = 1./data.shape[0]
    yaxis = np.arange(0,args.fft)
    xaxis = alphas
    xaxis = np.asarray(xaxis)
    for n,alpha in enumerate(xaxis):
        if args.verbose > 0:
            print "Running alpha " + `1./alpha`
        t = np.arange(0,data.shape[0])
        plus_alpha = np.asarray([np.exp(1j*np.pi*alpha*beta*k) for k in t], dtype=np.complex64)
        minus_alpha = np.asarray([np.exp(-1j*np.pi*alpha*beta*k) for k in t], dtype=np.complex64)
        y = data*minus_alpha
        x = data*plus_alpha
        #Window and delta are the same for x and y for every alpha, so we can overwrte each time without issue
        xx,window,delta = alpha_run(x, x, 0, beta)
        yx,window,delta = alpha_run(y, x, 0, beta)
        yy,window,delta = alpha_run(y, y, 0, beta)
        res = yx/np.sqrt(yy*xx)
        if coh == None:
            coh = np.zeros((xaxis.shape[0],args.fft), dtype=np.complex64)
        coh[n,:] = res

    def chi2inv(p, v):
        return st.invgamma(v/2,scale=2).ppf(p)

    acorr_window = np.correlate(window,window,"full")
    #Number of windows is the same
    K = xx.shape[0]
    k_start = len(window) + delta
    k_stop = min(len(acorr_window), (len(window))+delta*(K-1))
    k_step = delta
    k = np.arange(k_start, k_stop, k_step)
    if len(k) > 1:
        var_reduction = acorr_window[len(window)]**2/K + 2/K*(1-np.arange(len(k))/K)*(acorr_window[k_start:k_stop:k_step]**2)
    else:
        var_reduction = acorr_window[len(window)]**2/K

    print chi2inv(1-P, 2)*(var_reduction/2.)
    print chi2inv(1-P, 2)
    X, Y = np.meshgrid(xaxis, yaxis[:args.fft/2])
    Z = abs(coh.T[:args.fft/2,:]) #Transpose needed for plotting to work correctly...
    f = plot.figure()
    ax = Axes3D(f)
    ax.plot_surface(X, Y, Z, cmap=cm.jet)
    xlocs, xlabels = plot.xticks()
    ylocs, ylabels  = plot.yticks()
    plot.xticks(xlocs, [1./x for x in xaxis][::len(xaxis)/len(xlocs)])
    plot.yticks(ylocs, np.asarray(yaxis[::len(yaxis)/len(ylocs)])*(sr/(1000*float(args.fft))))
    plot.title("Cyclic Coherence")
    plot.xlabel("Cyclic Frequency(Hz)")
    plot.ylabel("Spectral Frequency(kHz)")

    plot.figure()
    plot.imshow(Z, cmap=cm.jet)
    plot.title("Cyclic Coherence Heatmap")
    plot.xlabel("Cyclic Frequency(Hz)")
    plot.ylabel("Spectral Frequency(kHz)")
    plot.colorbar()

    plot.figure()
    Zmean = np.mean(Z, axis=0)
    Zmin = np.amin(Z,0)
    Zmax = np.amax(Z,0)
    Zmed = np.median(Z, axis=0)
    plot.plot(Zmax, label="Max")
    plot.plot(Zmin, label="Min")
    plot.plot(Zmean, label="Mean")
    plot.plot(Zmed, label="Median")
    plot.title("Cyclic Coherence vs. Cyclic Frequency")
    plot.xlabel("Cyclic Frequency(Hz)")
    plot.ylabel("Coherence")
    plot.legend()

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

if args.specgram:
    run_specgram()
elif args.coherence:
    run_cyclic_coherence()
