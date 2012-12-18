#!/usr/bin/python
#Needs the following libs
#sudo apt-get install python-numpy python-scipy python-matplotlib

import scipy.io.wavfile as wavfile
from scipy.io import loadmat
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plot
import scipy.stats as st
import scipy.signal as sg

class EndpointsAction(argparse.Action):
    def __call__(self, parser, args, values, option = None):
        setattr(args, self.dest, map(int,values))
        if len(args.endpoints) < 3:
            defaults = [0, -1, 1]
            print "Wrong number of arguments, require 3 values, --endpoints start stop step"
            print "Using default endpoints of " + `args.endpoints`
            setattr(args, self.dest, defaults)

parser = argparse.ArgumentParser(description="Apply filterbank to input data")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")
parser.add_argument("-n", "--noplots", dest="noplots", action="store_true", help="Don't show plots")
parser.add_argument("-e", "--endpoints", dest="endpoints", default=[0,-1, 1], action=EndpointsAction, nargs="*", help='Start and stop endpoints for data, default will try to process the whole file')

FILT_CONST = 50
DECIMATE_BY = 4
def decimate(data):
    num_filters = DECIMATE_BY
    #decimate original data
    x = [0]*num_filters
    if args.verbose > 0:
        print "Original shape of data was " + `data.shape`
        print "Splitting into " + `num_filters` + " streams of data"
    for i in range(num_filters):
        idx = num_filters - i if i > 0 else i
        x[idx] = np.asarray(data[0+i::num_filters])
        x[idx] = np.append(x[idx], 0) if idx == 0 else np.insert(x[idx], 0, 0)
        if args.verbose > 0:
            print "Shape of decimated datastream " + `i` + " is now " + `x[idx].shape`
            if args.verbose > 1:
                print x[idx]
    decimated = np.vstack(x)
    return decimated

def polyphase_analysis(data):
    num_filters = DECIMATE_BY
    num_taps = DECIMATE_BY*FILT_CONST
    if len(data) % num_filters != 0:
        data = data[:len(data)-len(data)%num_filters]

    if num_taps%num_filters != 0:
        num_taps += num_filters-num_taps%num_filters
        print "Changing num_taps to " + `num_taps`

    #decimate prototype filter
    b = sg.firwin(num_taps,1./(2*num_filters))
    polyphase_filts = np.zeros((num_filters,num_taps/num_filters),dtype=np.complex64)
    for i in range(num_filters):
        polyphase_filts[i,:] = np.asarray(b[0+i::num_filters])

    if not args.noplots:
        w,h = sg.freqz(b)
        plot.plot(w/max(w), np.abs(h))
        plot.show()

    filtered = decimate(sg.lfilter(b, 1, data))
    out = np.fft.ifft(filtered, n=num_filters, axis=0)
    if not args.noplots:
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
