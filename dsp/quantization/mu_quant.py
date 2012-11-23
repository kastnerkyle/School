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
parser = argparse.ArgumentParser(description="Apply vector quantization using k-means clustering to a linearly encoded WAV file")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-b", "--bits", dest="bits", action="store", default=4, type=int, help="Integer number of bits used in quantized output, default is 4")
parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="Show verbose output")
parser.add_argument("-m", "--mu", dest="mu", action="store", default=0, type=int,  help="mu-law quantization, enter mu value")
parser.add_argument("-l", "--linear", dest="linear", action="store_true", help="linear quanitzation")
parser.add_argument("-am", "--adaptive_mu", dest="adaptive_mu", action="store", default=0, type=int, help="adaptive mu quanitzation, enter sample size for adaptive range")

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

sr, data = wavfile.read(args.filename)
bit_range = 2**args.bits

min_val = min(data)
max_val =  max(data)

def apply_linear(data):
    base = (2**16)/(2**args.bits)
    out = [int(x/base)*base for x in data]
    return out

if args.verbose:
    print "File has a sample rate of " + `sr` + " samples per second"
    print "File has " + `len(data)` + " values, " + `len(data)/float(sr)` + " seconds"
    print "min", min_val, "max", max_val
wav_bit_range = 2**16

if args.mu:
    if args.verbose:
        print "Quantizing using mu-law algorithm"

    Xmax = 2**15
    u = args.mu
    data = [ x/float(Xmax) if x !=0 else .01 for x in data]
    d = [math.log(1+u*(abs(x)))/(math.log(1+u))*(x/float(abs(x))) for x in data]
    d = [Xmax*x for x in d]
    mu_q = apply_linear(d)
    mu_q = [ x/float(Xmax) for x in mu_q ]
    mu_q = [ x if x !=0 else .01 for x in mu_q]
    out = [(1/float(u))*((1+u)**float(abs(x))-1)*(x/float(abs(x))) for x in mu_q]
    out = [Xmax*x for x in out]
    wavfile.write("mu_quantized_%sbit_%imu_"%(args.bits, u) + args.filename, sr, np.asarray(out).astype("int16"))

if args.adaptive_mu:
    if args.verbose:
        print "Quantizing using mu-law algorithm"

    #mu-law = (Xmax/u) * (log(1+u(|x|/Xmax)))/(log(1+u)) * sin(x)
    #indirect method
    if abs(max_val) > abs(min_val):
        Xmax = abs(max_val)
    else:
        Xmax = abs(min_val)
    base = (max_val - min_val)/(args.bits) + 1
    lin_level_values = []
    mu_level_values = []
    ar = args.adaptive_mu
    for  x in (range((args.bits))):
       lin_level_values.append(min_val + base*x)
    lin_level_values.append(max_val+1)

    #if mean is closer to zero, mu --> 255
    #if mean is closer to Xmax, mu --> 0
    lookup = []
    if args.verbose:
        print 'Linear levels:'
        print lin_level_values
    out = []
    for d in range(0, len(data)-ar, ar) :
        mu_mean = abs(np.mean(data[d:(d+ar)]))
        arsum = 0
        for x in range(ar):
            arsum = arsum + abs(data[d+x])
        mu_mean = arsum/ar
        mu =((1- (float(mu_mean)/float(Xmax)) )*254)
        if args.verbose:
            print 'mean', mu_mean, 'mu', mu

        mu_level_values.append(min_val)
        for i in range(1, len(lin_level_values)-1):
            if lin_level_values[i] != 0:
                mu_level_values.append(int((abs(lin_level_values[i])/lin_level_values[i])*(Xmax/mu)*(10**((math.log((1+mu), 10)*abs(lin_level_values[i]))/(Xmax)) - 1)))
            else:
                print "lin == 0"
                mu_level_values.append(0)
        mu_level_values.append(max_val+1)
        for x in range(ar):
            for i in range(len(mu_level_values)-1):
                if mu_level_values[i]<= data[d+x] < mu_level_values[i+1]:
                    out.append(mu_level_values[i])
        if args.verbose:
            print mu_level_values
        mu_level_values = []
    wavfile.write("adaptive_mu_quantized_%sbit_%isamples_"%(args.bits, args.adaptive_mu) + args.filename, sr, np.asarray(out).astype("int16"))


if args.linear:
    out = apply_linear(data)

    if args.verbose:
       print 'Used values:'
       print  sorted(set(out))

    wavfile.write("linear_quantized_%ibits_" %args.bits + args.filename, sr, np.asarray(out).astype("int16"))
############
print "output length", len(out)
print "Processing complete for " + args.filename
