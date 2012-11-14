import scipy.io.wavfile as wavfile
import numpy as np
import sys
import math
freq = 1000
sample_rate = 8000

out = range(-2**15+1, 2**15-1)

wavfile.write("ramp.wav", sample_rate, np.asarray(out).astype("int16"))
