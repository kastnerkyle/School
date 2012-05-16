#!/usr/bin/python

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plot 
import random  

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
    run = 10000
    for i in range(run):
        var_est = update_var_est(samp_vec, mean_est)
        mean_est = update_mean_est(samp_vec, var_est)
    print mean_est
    print var_est

#means spaced from 1 to 100
sample_count = 1000
n = 5
true_means = np.linspace(1,100, num=n)

#variances randomly distributed around 5
true_vars = 2+np.random.randn(np.size(true_means))
samples_list = [x[0] + x[1]*np.random.randn(sample_count/n) for x in zip(true_means, true_vars)]
samples = np.concatenate(samples_list)
(count, bins) = np.histogram(samples, 1000)
a = np.correlate(count, count, mode='full')
len(samples)
#plot.plot(.5*(bins[1:]+bins[:-1]), count)
plot.plot(a)
plot.show()
#samples = st.norm.rvs(true_mean, np.sqrt(true_var), size=1000)
#estimate(samples)
