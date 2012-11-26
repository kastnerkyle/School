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


parser.add_argument("-o", "--original", dest="source", help="Original wav file")
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


if args.mu:
    sr1, mu = wavfile.read(args.mu)
    pylab.plot(mu[s:e], 'g', label="mu")
if args.a:
    sr2, am = wavfile.read(args.a)
    pylab.plot(am[s:e], 'y', label="adaptive mu")
if args.l:
    sr3, lin = wavfile.read(args.l)
    pylab.plot(lin[s:e], 'b', label="linear")
if args.v:
    sr4, vec = wavfile.read(args.v)
    pylab.plot(vec[s:e], 'r', label="vector")

pylab.legend(loc=1, ncol=4, mode="expand", borderaxespad=0) # bbox_transform=pylab.gcf().transFigure )

pylab.savefig("%s.png" %args.source[:-4]) 
pylab.show()

