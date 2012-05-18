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
true_height = 5.
true_mean = 10.
true_var = .5

n = gaussian_peak(true_height, true_mean, true_var)
lb = .6*true_mean
ub = 1.4*true_mean
r = np.arange(lb, ub, (ub-lb)/100)
plot.plot(r, [n.func(x) for x in r])
plot.show()

#plot.hist(samples_list)
#plot.show()
