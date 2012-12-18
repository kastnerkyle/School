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
