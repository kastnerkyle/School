#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plot 
from multiprocessing import Pool

class gaussian_peak:
    def __init__(self, height, mean, var):
        self.height = height
        self.mean = mean
        self.var = var

    def func(self, x):
        return self.height * np.exp(-np.square(x-self.mean)/(2*self.var))

def update_h_est(prev_est, *knowns ):
    b = prev_est
    a = -2*(knowns[0]*np.exp(
    return 

def estimate(samp_vec,n1,n2,n3):
    est = update_h_est()
    return est

#means spaced from 1 to 100
sample_count = 1000
true_heights = [5., 12., 6.]
true_means = [10., 22., 6.]
true_vars = [.5, .5, .5]

[n1, n2, n3] = [gaussian_peak(h, m, v) 
                for h, m, v in zip(true_heights, true_means, true_vars)]
lb = min(true_means) - 6*max(true_vars) 
ub = max(true_means) + 6*max(true_vars)
r = np.arange(lb, ub, (ub-lb)/100)

[n1_vec, n2_vec, n3_vec] = [[c.func(x) for x in r] for c in [n1, n2, n3]]
samp_vec = sum([n1_vec, n2_vec, n3_vec], [])
print samp_vec
plot.plot(r, n1_vec, "b",
          r, n2_vec, "g",
          r, n3_vec, "r")
plot.show()

