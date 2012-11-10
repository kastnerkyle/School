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
import operator

parser = argparse.ArgumentParser(description="Apply vector quantization using k-means clustering to a linearly encoded WAV file")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-b", "--bits", dest="bits", action="store", default=4, type=int, help="Integer number of bits used in quantized output, default is 4")
parser.add_argument("-r", "--random", dest="random", action="store_true", help="Use uniform random algorithm for centroid initialization instead of Metropolis-Hastings")
parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Show verbose output")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

sr, data = wavfile.read(args.filename)
centroid_count = 2**args.bits

if args.verbose:
    print "File has a sample rate of " + `sr` + " samples per second"
    print "File has " + `len(data)` + " values, " + `len(data)/float(sr)` " seconds"
    print "Vector quantization will use " + `centroid_count` + " centroids for k-means calculations"

if args.random:
    centroid_type = "random"
    if args.verbose:
        print
    means = [random.randrange(min(data),max(data),1) for i in range(centroid_count)]
    print "Centroid calculations complete"
else:
    centroid_type = "metropolis_hastings"
    start = data[random.randrange(0,len(data),1)]
    std_dev = np.std(data) #arbitrary std_dev
    means = []
    prev = start
    while len(means) < centroid_count:
        print "Currently " + `len(means)` + " centroids calculated"
        candidate = prev + std_dev * np.random.randn()
        prob_prev = len(filter(lambda x: x < prev, data))/float(len(data))
        prob_candidate = len(filter(lambda x: x < candidate, data))/float(len(data))
        acceptance = prob_candidate/prob_prev
        if acceptance >= 1:
            prev = candidate
            means.append(candidate)
        else:
            if random.random() <= acceptance:
                prev = candidate
                means.append(candidate)

bound = 0.1 #arbitrary bound for mean movement, must be between 0 and 1, higher values allow centroids to move more

data_to_quant = {}
for i,d in enumerate(data):
    print "Processing sample "
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
