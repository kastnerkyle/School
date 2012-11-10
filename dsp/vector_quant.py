#!/usr/bin/python
#sudo apt-get install python-scipy python-numpy sndfile-programs sndfile-tools
#http://www.voiptroubleshooter.com/open_speech/american.html
#http://stackoverflow.com/questions/1545606/python-k-means-algorithm
import scipy.io.wavfile as wavfile
import numpy as np
import sys
import random
sr, data = wavfile.read(sys.argv[1])

means = [random.randrange(min(data),max(data),1) for i in range(256)]
bound = 0.2

data_to_quant = {}
for p,d in enumerate(data):
    smallest_error = None
    for i,val in enumerate(means):
        error = abs(d-val)
        if error < smallest_error or smallest_error == None:
            smallest_error = error
            closest_k = i
    data_to_quant[p] = closest_k
    means[closest_k] = means[closest_k]*(1-bound) + d*bound

out = []
for i in data_to_quant.keys():
    out.append(int(means[data_to_quant[i]]))

wavfile.write("quantized.wav", sr, np.asarray(out).astype("int16"))
