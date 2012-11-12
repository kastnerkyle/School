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
from multiprocessing import Pool, cpu_count

parser = argparse.ArgumentParser(description="Apply vector quantization using k-means clustering to a linearly encoded WAV file")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-b", "--bits", dest="bits", action="store", default=4, type=int, help="Integer number of bits used in quantized output, default is 4")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")
parser.add_argument("-s", "--single", dest="single", action="store_true", help="Single core mode")
group = parser.add_mutually_exclusive_group()
group.add_argument("-z", "--zeroes", dest="zeroes", action="store_true", help="Use all zeroes for centroid initialization instead of Metropolis-Hastings")
group.add_argument("-m", "--median", dest="median", action="store_true", help="Use data median for centroid initialization instead of Metropolis-Hastings")
group.add_argument("-u", "--uniform", dest="uniform", action="store_true", help="Use uniform random algorithm for centroid initialization instead of Metropolis-Hastings")
group.add_argument("-r", "--rejection", dest="rejection", action="store_true", help="Use rejection sampling for centroid initialization instead of Metropolis-Hastings")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

sr, data = wavfile.read(args.filename)
centroid_count = 2**args.bits

if args.verbose > 0:
    print "File has a sample rate of " + `sr` + " samples per second"
    print "File has " + `len(data)` + " values, " + `len(data)/float(sr)` + " seconds"
    print "Vector quantization will use " + `centroid_count` + " centroids for k-means calculations"

if args.uniform:
    centroid_type = "uniform"
    if args.verbose > 0:
        print "Using uniform random algorithm for initial centroid distribution"
    means = [random.choice(data) for i in range(centroid_count)]
    if args.verbose > 1:
        print "Means initialized at:"
        print means

    if args.verbose > 0:
        print "Centroid calculations complete"

elif args.zeroes:
    centroid_type = "zeroes"
    if args.verbose > 0:
        print "Using all zeroes for initial centroid distribution"
    means = [0]*centroid_count
    if args.verbose > 1:
        print "Means initialized at:"
        print means

    if args.verbose > 0:
        print "Centroid calculations complete"

elif args.median:
    centroid_type = "median"
    if args.verbose > 0:
        print "Using all zeroes for initial centroid distribution"
    means = [np.median(data)]*centroid_count
    if args.verbose > 1:
        print "Means initialized at:"
        print means

    if args.verbose > 0:
        print "Centroid calculations complete"

elif args.rejection:
    centroid_type = "rejection"
    if args.verbose > 0:
        print "Using rejection sampling algorithm for initial centroid distribution"
    if args.single:
        split = 1
    else:
        split = cpu_count()

    def rejection_run(data):
        means = []
        while len(means) < centroid_count/split:
            candidate = random.choice(data)
            prob_candidate = len(filter(lambda x: x < candidate, data))/float(len(data))
            if random.random() < prob_candidate:
                means.append(candidate)
        return means

    p = Pool(split)
    centroids = p.map_async(rejection_run, [data]*split)
    p.close()
    means = []
    for group in centroids.get():
        means.extend(group)

    if args.verbose > 0:
        print "Centroid calculations complete"

    if len(means) != centroid_count:
        print "Split value (number of available cores) must be evenly divisible into 2^bits. Use the --single or -s option!"
        sys.exit()

    if args.verbose > 1:
        print "Means initialized at: "
        print means

    if args.verbose > 0:
        print "Centroid calculation complete"

else:
    centroid_type = "metropolis_hastings"
    if args.verbose > 0:
        print "Using Metropolis-Hastings algorithm for initial centroid distribution"

    if args.single:
        split = 1
    else:
        split = cpu_count()

    if args.verbose > 0:
        print "Using " + `split` + " cores for the Metropolis Hastings calculations"

    def metropolis_run(data):
        start = random.choice(data)
        std_dev = np.std(data) #arbitrary std_dev, larger value will give better centroid spread, but too large will break the sampling
        means = []
        prev = start
        while len(means) < centroid_count/split:
            if args.verbose > 1:
                print "Currently " + `len(means)` + " centroids calculated"
            #Random walk for next candidate
            candidate = prev + std_dev * np.random.randn()
            #Don't need conditional here because the probabilities are not dependent i.e. P(B|A) = P(B)
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
        return means

    p = Pool(split)
    centroids = p.map_async(metropolis_run, [data]*split)
    p.close()
    means = []
    for group in centroids.get():
        means.extend(group)

    if len(means) != centroid_count:
        print "Split value (number of available cores) must be evenly divisible into 2^bits. Use the --single or -s option!"
        sys.exit()

    if args.verbose > 1:
        print "Means initialized at: "
        print means

    if args.verbose > 0:
        print "Centroid calculation complete"

bound = 0.1 #arbitrary bound for mean movement, must be between 0 and 1, higher values allow centroids to move more

#Assignment dictionary which shows what centroid each data point is beholden to
data_to_quant = {}
for i,d in enumerate(data):
    if args.verbose > 1 and i%10000 == 0:
        print "Processing sample " + `i` + " of " + `len(data)`
    smallest_error = None
    for n,v in enumerate(means):
        error = abs(d-v)
        if error < smallest_error or smallest_error == None:
            smallest_error = error
            closest_k = n
    data_to_quant[i] = closest_k
    means[closest_k] = means[closest_k]*(1-bound) + d*bound

#Actually quantize each value
out = np.zeros(len(data))
for k in data_to_quant.keys():
    out[k] = int(means[data_to_quant[k]])

wavfile.write("vector_quantized_" + `args.bits` + "bit_" + centroid_type + "_" + args.filename, sr, np.asarray(out).astype("int16"))

print "Processing complete for " + args.filename
