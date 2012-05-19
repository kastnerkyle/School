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
    return st.norm.rvs(np.mean(samp_vec), scale=np.sqrt(var_est/n))

def update_height_est(samp_vec, samp_scaled):
    #Get values for linear regression estimation 
    ys = np.matrix(samp_vec).transpose()
    xs = np.matrix(samp_scaled).transpose()
    vbeta = 1./(xs.transpose()*xs)
    beta = vbeta*xs.transpose()*ys

    s_2 = (ys-xs*beta).transpose()*(ys-xs*beta)
    var = s_2/st.chi2.rvs(1)   
    return st.norm.rvs(beta, scale=np.sqrt(vbeta*var))

def estimate(rand_vec, samp_vec, samp_scaled):
    mean_est = random.random()
    var_est = random.random()
    run = 100
    height_est = update_height_est(samp_vec, samp_scaled)
    for i in range(run):
        var_est = update_var_est(rand_vec, mean_est)
        mean_est = update_mean_est(rand_vec, var_est)
    print height_est
    print mean_est     
    print var_est

#means spaced from 1 to 100
sample_count = 1000
h = 20.
m = 11.
v = 3.

n1 = gaussian_peak(h, m, v)
n2 = gaussian_peak(1, m, v)
r = st.norm.rvs(m, v, size=sample_count)
n1_vec = [n1.func(x) for x in r]
n2_vec = [n2.func(x) for x in r]
rand_vec = m + np.sqrt(v)*np.random.randn(sample_count)
estimate(rand_vec, n1_vec, n2_vec)
plot.plot(np.ravel(n1_vec), "bo",
          np.ravel(n2_vec), "ro")
plot.show()

