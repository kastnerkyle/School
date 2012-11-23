#!/usr/bin/python

#Attempt to apply spectral correlation function to data and plot 3D
import scipy.io.wavfile as wavfile
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plot

parser = argparse.ArgumentParser(description="Apply ")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-n", "--noplot", dest="noplot", action="store_true", help="WAV file to be processed")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")
parser.add_argument("-f", "--fft", type=int, dest="fft", action="store", default=1024, help="Optionally set FFT size, default is 1024")
parser.add_argument("-s", "--specgram", dest="specgram", action="store_true", help="Show spectrogram of input wavefile")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

sr, data = wavfile.read(args.filename)
data = np.asarray(data)
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

if args.specgram:
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
