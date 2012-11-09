#!/usr/bin/python
#sudo apt-get install python-scipy python-numpy
#http://www.voiptroubleshooter.com/open_speech/american.html
#http://stackoverflow.com/questions/1545606/python-k-means-algorithm
import scipy.io.wavfile as wavfile
import sys

sr, data = wavfile.read(sys.argv[1])
print sr
print len(data)
