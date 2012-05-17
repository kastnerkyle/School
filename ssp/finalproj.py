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
    return st.norm.rvs(np.mean(samp_vec),
                       scale=np.sqrt(var_est/n))

def update_height_est(samp_vec, mean_est, var_est):
    def update_height_mean(height_vec, height_var_est):
        return update_mean_est(height_vec, height_var_est) 

    def update_height_var(height_vec, height_mean_est):
        return update_var_est(height_vec, height_mean_est)

    height_mean_est = random.random()
    height_var_est = random.random() 
    run = 10
    for i in range(run):
        height_vec = [st.norm.pdf(x, height_mean_est, np.sqrt(height_var_est)) 
                      for x in samp_vec]
        height_mean_est = update_height_mean(height_vec, height_var_est)
        height_var_est = update_var_est(height_vec, height_mean_est)
    return height_mean_est

def estimate(samp_vec):
    mean_est = random.random()
    var_est = random.random()
    height_est = random.random()
    run = 1
    for i in range(run):
        var_est = update_var_est(samp_vec, mean_est)
        mean_est = update_mean_est(samp_vec, var_est)
        height_est = update_height_est(samp_vec, mean_est, var_est)
        print "Iteration " + `i` + " complete"
    return [("ESTIMATED MEAN: " + `mean_est`, "ESTIMATED VAR:  " + `var_est`, "ESTIMATED HEIGHT: " + `height_est`)]

#means spaced from 1 to 100
sample_count = 1000
true_mean = 25
true_var = 5
true_height = 10
samples_list = st.norm.rvs(true_mean,
                           np.sqrt(true_var),
                           size=sample_count)

actuals = [("TRUE MEAN: " + `x[0]`,
            "TRUE VAR: " + `x[1]`,
            "TRUE HEIGHT: " + `x[2]`)
            for x in [(true_mean, true_var, true_height)]] 

estimates = estimate(samples_list)
for i,j in zip(estimates, actuals):
   print i
   print j

plot.hist(samples_list)
plot.show()
