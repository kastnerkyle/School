#!/usr/bin/python
#sudo apt-get install python-scipy python-numpy python-matplotlib
import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plot
import sys
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description="Measure error stats for each quantized file")
parser.add_argument(dest="original", help="Original wavfile")
parser.add_argument(dest="quantized", nargs="+", help="Quantized version(s) of original file")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

orig_sr, orig = wavfile.read(args.original)
stats = {}

for f in args.quantized:
    stats[f] = {}
    quant_sr, quant = wavfile.read(f)

    if len(orig) != len(quant) and orig_sr != quant_sr:
        print "Quantized file " + f + " does not match original"
        print "Original file has " + `len(orig)` + " and sample rate " + `orig_sr`
        print "Quantized file has " + `len(quant)` + " and sample rate " + `quant_sr`
        print "Exiting now!"
        sys.exit()

    mse = sum([(o-q)**2 for o,q in zip(orig,quant)])/len(orig)
    rmse = np.sqrt(mse)
    snr = 10*np.log(np.var(orig)/np.var(quant))

    stats[f]["Mean Square Error"] = mse
    stats[f]["Root Mean Square Error"] = rmse
    stats[f]["Signal to Noise Ratio"] = snr
    if args.verbose > 0:
        print "Quantized filename: " + f
        pprint(stats[f])
