#!/usr/bin/python

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plot 
import random  

def sigma_posterior(samp_vec):
    mag = np.vdot(samp_vec, samp_vec)
    return st.invgamma.pdf( len(samp_vec)/2, mag/2 )

rand = [10*(random.random()-.5) for y in range(1000)]
vec = [st.norm.pdf(x) for x in rand]

plot.plot(vec)
plot.show()
print sigma_posterior(vec)
