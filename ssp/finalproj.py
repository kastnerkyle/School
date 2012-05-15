#!/usr/bin/python

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plot 
import random  

def update_var_est(samp_vec,mean_est):
    n = float(len(samp_vec))
    v = sum([np.square(x-mean_est)/n for x in samp_vec]) 
    #Scipy.stats implementation of inv gamma is a one parameter, need to feed second value as scale
    return st.invgamma.rvs(n/2, scale=n*v/2)

def update_mean_est(samp_vec,var_est):
    n = float(len(samp_vec))
    samp_mean = np.mean(samp_vec)
    #Scale variable is standard deviation
    return st.norm.rvs(samp_mean, scale=np.sqrt(var_est/n))

def estimate(samp_vec):
    mean_est = random.random()
    var_est = random.random()
    run = 10000
    for i in range(run):
        mean_est = update_mean_est(samp_vec, var_est)
        var_est = update_var_est(samp_vec, mean_est)
    print mean_est
    print var_est

true_mean = 25
true_var = 3
samples = st.norm.rvs(true_mean, np.sqrt(true_var), size=1000)

estimate(samples)
