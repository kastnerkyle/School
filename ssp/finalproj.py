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

#means spaced from 1 to 100
sample_count = 1000
true_heights = [5., 12., 6.]
true_means = [10., 22., 6.]
true_vars = [.5, .5, .5]

[n1, n2, n3] = [gaussian_peak(h, m, v) for h, m, v in zip(true_heights, true_means, true_vars)]
lb = min(true_means) - 6*max(true_vars) 
ub = max(true_means) + 6*max(true_vars)
r = np.arange(lb, ub, (ub-lb)/100)
plot.plot(r, [n1.func(x) for x in r], "b",
          r, [n2.func(x) for x in r], "g",
          r, [n3.func(x) for x in r], "r")
plot.show()

