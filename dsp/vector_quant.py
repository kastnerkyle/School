#!/usr/bin/python
#sudo apt-get install python-scipy python-numpy sndfile-programs sndfile-tools
#http://www.voiptroubleshooter.com/open_speech/american.html
#http://stackoverflow.com/questions/1545606/python-k-means-algorithm
#play the resulting file with sndfile-play
import scipy.io.wavfile as wavfile
import numpy as np
import sys
import random
import argparse

parser = argparse.ArgumentParser(description="Apply vector quantization using k-means clustering to a linearly encoded WAV file")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-b", "--bits", dest="bits", action="store", default=8, type=int, help="Integer number of bits used in quantized output, default is 8")
parser.add_argument("-r", "--random", dest="random", action="store_true", help="Use uniform random algorithm for centroid initialization instead of Metropolis-Hastings")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

sr, data = wavfile.read(args.filename)
centroid_count = 2**args.bits

if args.random or True:
    centroid_type = "random"
    means = [random.randrange(min(data),max(data),1) for i in range(centroid_count)]
else:
    centroid_type = "metropolis_hastings"
    means = []

bound = 0.1

data_to_quant = {}
for i,d in enumerate(data):
    smallest_error = None
    for n,v in enumerate(means):
        error = abs(d-v)
        if error < smallest_error or smallest_error == None:
            smallest_error = error
            closest_k = n
    data_to_quant[i] = closest_k
    means[closest_k] = means[closest_k]*(1-bound) + d*bound

out = np.zeros(len(data))
for k in data_to_quant.keys():
    out[k] = int(means[data_to_quant[k]])

wavfile.write("quantized_" + centroid_type + "_" + args.filename, sr, np.asarray(out).astype("int16"))

print "Processing complete for " + args.filename
