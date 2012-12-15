#!/usr/bin/python
#Attempt to apply spectral correlation function to data and plot 3D
#http://www.johnvinyard.com/blog/?p=268
import scipy.io.wavfile as wavfile
from scipy.io import loadmat
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plot
from matplotlib import cm
from numpy.lib.stride_tricks import as_strided as ast
import copy
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as st
import scipy.signal as sg
import time
import pandas
from spectral import specgram

class EndpointsAction(argparse.Action):
    def __call__(self, parser, args, values, option = None):
        setattr(args, self.dest, map(int,values))
        if len(args.endpoints) < 3:
            defaults = [5000, 6000, 1]
            print "Wrong number of arguments, require 3 values, --endpoints start stop step"
            print "Using default endpoints of " + `args.endpoints`
            setattr(args, self.dest, defaults)

parser = argparse.ArgumentParser(description="Apply filterbank to input data")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")
parser.add_argument("-f", "--filters", dest="filters", action="store_true", help="Show filter plots")
parser.add_argument("-p", "--plots", dest="plots", action="store_true", help="Show bank plots")
parser.add_argument("-e", "--endpoints", dest="endpoints", default=[5000,6000, 1], action=EndpointsAction, nargs="*", help='Start and stop endpoints for data')

def polyphase_analysis(data):
    filt_const = 1000
    num_filters = 16
    num_taps = num_filters*filt_const
    b = sg.firwin(num_taps,1./(num_filters))
    x = [0]*num_filters
    if args.verbose > 0:
        print "Original shape of data was " + `data.shape`
        print "Splitting into " + `num_filters` + " streams of data"
    for i in range(num_filters):
        x[i] = data[0+i::num_filters]
        if i > 0:
            len_diff = x[i-1].shape[0] - x[i].shape[0]
            if len_diff != 0:
                if args.verbose > 0:
                    print "Size mismatch - extending data stream " + `i` + " with " + `len_diff` + " zeros"
                x[i] = np.hstack((x[i],[0]*len_diff))
        if args.verbose > 0:
            print "Shape of decimated datastream " + `i` + " is now " + `x[i].shape`
            if args.verbose > 1:
                print x[i]

    if num_taps%num_filters != 0:
        num_taps += num_filters-num_taps%num_filters
        print "Changing num_taps to " + `num_taps`

    polyphase_filts = np.zeros((num_filters,num_taps/num_filters),dtype=np.complex64)
    for i in range(num_filters):
        polyphase_filts[i,:] = np.asarray(b[0+i::num_filters]).T

    if args.filters:
        w,h = sg.freqz(b)
        plot.plot(w/max(w), np.abs(h))
        plot.show()

    decimated = np.vstack(x)
    filtered = np.asarray([sg.fftconvolve(polyphase_filts[n,:], decimated[n,:]) for n in range(num_filters)])
    out = np.fft.fft(filtered, axis=0)
    if args.plots:
        plot.specgram(data)
        plot.show()
        for i in range(num_filters):
            plot.specgram(out[i,:], 256)
            plot.show()

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

if args.filename[-4:] == ".mat":
    mat = loadmat(args.filename)
    data = mat["x"].flatten()
    data = np.asarray(data, dtype=np.complex64)[::args.endpoints[2]]
    data = data[args.endpoints[0]:args.endpoints[1]]
    sr = -1

elif args.filename[-4:] == ".wav":
    sr, data = wavfile.read(args.filename)
    data = np.asarray(data, dtype=np.complex64)[::args.endpoints[2]]
    data = data[args.endpoints[0]:args.endpoints[1]]

polyphase_analysis(data)
