#!/usr/bin/python

import sys
import numpy as np
import scipy.signal as sig
import scipy.stats as st
import matplotlib.pyplot as plot 
import random  
from multiprocessing import Pool

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
    return ("ESTIMATED MEAN: " + `mean_est`, "ESTIMATED VAR:  " + `var_est`)

#means spaced from 1 to 100
sample_count = 1000
true_means = np.arange(180,1000,2*60)

#variances randomly distributed around 40
true_vars = 40+np.random.randn(np.size(true_means))
samples_list = [x[0]+ np.sqrt(x[1])*np.random.randn(sample_count)
                for x in zip(true_means, true_vars)]

actuals = [("TRUE MEAN: " + `x[0]`, "TRUE VAR: " + `x[1]`)
           for x in zip(true_means, true_vars)] 

p = Pool()
estimates = p.map(estimate, samples_list)
for i,j in zip(estimates, actuals):
   print i
   print j
