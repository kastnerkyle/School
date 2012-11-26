#!/usr/bin/python
#sudo apt-get install python-scipy python-numpy python-matplotlib
import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plot
import sys
import argparse

parser = argparse.ArgumentParser(description="Measure error stats for each quantized file")
parser.add_argument(dest="original", help="Original wavfile")
parser.add_argument(dest="quantized", help="Quantized version of original file")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

orig_sr, orig = wavfile.read(args.original)
orig_plot, = plot.plot(orig, 'r--')

quant_sr, quant = wavfile.read(args.quantized)
quant_plot, = plot.plot(quant, 'b')
n = args.quantized.split("/")[-1].split("_")
title = n[0]
qtype = n[1]
bit = n[2]
technique = n[3]

if args.verbose > 0:
    print "Title: " + title
    print "Quantization type: " + qtype
    print "Number of bits: " + bit
    if technique in ["metropolishastings", "uniform", "rejection", "zeroes", "median"]:
        print "Technique: " + technique

if technique in ["metropolishastings", "uniform", "rejection", "zeroes", "median"]:
    plot.legend([orig_plot, quant_plot], ["Original 16bit wavfile",  title.title() + ", " + technique + " " + qtype + " " + bit + " file"])
else:
    plot.legend([orig_plot, quant_plot], ["Original 16bit wavfile",  title.title() + ", " + qtype + " " + bit + " file"])
plot.show()
