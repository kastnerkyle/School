#!/usr/bin/python
#sudo apt-get install python-scipy python-numpy sndfile-programs sndfile-tools
#http://www.voiptroubleshooter.com/open_speech/american.html
#http://stackoverflow.com/questions/1545606/python-k-means-algorithm
#play the resulting file with sndfile-play
import scipy.io.wavfile as wavfile
import numpy as np
import sys
import argparse
import math
import pylab
parser = argparse.ArgumentParser(description="Apply vector quantization using k-means clustering to a linearly encoded WAV file")

parser.add_argument(dest="original_file", help="Path to original WAV file")
parser.add_argument(dest="quantized_file", help="Quantized version of original, WAV format")
parser.add_argument("-b", "--bits", dest="bits", action="store", type=int, default=4, help="Integer number of bits used in quantized output, should be same for all files")

parser.add_argument("-s", "--start", dest="start", action="store", type=int, default=0, help="Integer number to start plot")

parser.add_argument("-e", "--end", dest="end", action="store", type=int, default=500, help="Integer number to end plot")

parser.add_argument("-m", "--mu", dest="mu",  help="Mu quantizedd wav file")
parser.add_argument("-a", "--adapive-mu", dest="a",  help="Adaptive Mu quantized wav file")
parser.add_argument("-l", "--linear",  dest="l", help="Linear quantized wav file")
parser.add_argument("-v", "--vector", dest="v", help="Vector quantized wav file")

parser.add_argument("-t", "--text", dest="t", default="", help="Text to add to title")

pylab.xlabel("t")
pylab.ylabel("V")

pylab.xlabel("Time (samples)")
pylab.ylabel("Amplitude")
try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

s = args.start
e = args.end
pylab.title("%s at %i bits, %i:%i, %s" %(args.source, args.bits, s, e, args.t))
sr, source = wavfile.read(args.source)
pylab.plot(source[s:e], 'k', label="source")

sr1, quant = wavfile.read(args.quantized_file)
if args.mu:
    pylab.plot(quant[s:e], 'g', label="mu")
if args.a:
    pylab.plot(quant[s:e], 'y', label="adaptive mu")
if args.l:
    pylab.plot(quant[s:e], 'b', label="linear")
if args.v:
    pylab.plot(quant[s:e], 'r', label="vector")

pylab.legend(loc=1, ncol=4, mode="expand", borderaxespad=0) # bbox_transform=pylab.gcf().transFigure )

pylab.savefig("%s.png" %args.source[:-4]) 
pylab.show()

