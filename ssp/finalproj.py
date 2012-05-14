#!/usr/bin/python

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plot 
import random  

#Scipy.stats implementation is a one parameter, need to feed second value as scale
def update_var_est(samp_vec,mean_est):
     n = float(len(samp_vec))
     v = sum([np.square(x-mean_est)/n for x in samp_vec]) 
     return st.invgamma.rvs(n/2, scale=n*v/2)

def update_mean_est(samp_vec,var_est):
     n = float(len(samp_vec))
     samp_mean = np.mean(samp_vec)
     return st.norm.rvs(samp_mean, var_est/n)

true_mean = 25
true_var = 3

#There is a square somewhere that is making things weird
samples = st.norm.rvs(25, np.sqrt(3), size=1000)

mean_est = random.random()
var_est = random.random()

run = 5000

for i in range(run):
    mean_est = update_mean_est(samples, var_est)
    var_est = update_var_est(samples, mean_est)

print mean_est
print var_est
plot.hist(samples)
plot.show()
