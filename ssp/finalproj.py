#!/usr/bin/python

import sys
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plot 
import random

class gaussian_peak:
    def __init__(self, height, mean, var):
        self.height = height
        self.mean = mean
        self.var = var

    def func(self, x):
        return self.height * np.exp(-np.square(x-self.mean)/(2*self.var))

def update_var_est(samp_vec, mean_est):
    n = float(len(samp_vec))
    v = sum([np.square(x-mean_est)/n for x in samp_vec])
    #Scipy.stats implementation of inv gamma is a one parameter, need to feed second value as scale
    return st.invgamma.rvs(n/2, scale=n*v/2)

def update_mean_est(samp_vec, var_est):
    n = float(len(samp_vec))
    #Scale variable is standard deviation
    return st.norm.rvs(np.mean(samp_vec), np.sqrt(var_est/n))


def estimate(samp_vec):
    mean_est = random.random()
    var_est = random.random()
    run = 1000
    for i in range(run):
        var_est = update_var_est(samp_vec, mean_est)
        mean_est = update_mean_est(samp_vec, var_est)
    print var_est
    print mean_est     

#means spaced from 1 to 100
sample_count = 1000
h =  5.
m = 10.
v = .5

n1 = gaussian_peak(h, m, v)
lb = m - 6*v 
ub = m + 6*v
r = np.arange(lb, ub, (ub-lb)/100)

n1_vec = [n1.func(x) for x in r]
estimate(n1_vec)
plot.plot(r, n1_vec, "b")
plot.show()

