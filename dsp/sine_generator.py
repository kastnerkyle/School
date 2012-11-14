import scipy.io.wavfile as wavfile
import numpy as np
import sys
import math
freq = 1000
sample_rate = 8000
out = []
for x in range(16000):
    out.append( math.sin((2*math.pi*x*freq)/sample_rate))


out = map(lambda x: x*(2**16)/2, out)

wavfile.write("full_sin.wav", sample_rate, np.asarray(out).astype("int16"))
