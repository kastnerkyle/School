#!/usr/bin/python

import sys
import numpy as np
import scipy.stats as st
import operator
import matplotlib.pyplot as plot 
import random

class gaussian_peak:
    def __init__(self, height, mean, var):
        self.height = height
        self.mean = mean
        self.var = var

    def func(self, x):
        return self.height * np.exp(-np.square(x-self.mean)/(2*self.var))

def update_height_est(data, components):
    #Get values for linear regression estimation 
    ys = np.matrix(samp_vec).transpose()
    xs = np.matrix(samp_scaled).transpose()
    vbeta = 1./(xs.transpose()*xs)
    beta = vbeta*xs.transpose()*ys

    s_2 = (ys-xs*beta).transpose()*(ys-xs*beta)
    var = s_2/st.chi2.rvs(1)   
    return st.norm.rvs(beta, scale=np.sqrt(vbeta*var))

def estimate(m, v, r, data, *vecs):
    print data 
#update_height_est(data,  
    return 0


#means spaced from 1 to 100
sample_count = 1000
h = [20., 12., 5.]
m = [11., 7., 9.]
v = [.5, .5, .5]

lb = min(m) - 6*max(v)
ub = max(m) + 6*max(v)
r = np.arange(lb, ub, (ub-lb)/100)
gaussians = [gaussian_peak(x[0], x[1], x[2]) for x in zip(h, m, v)]
vecs = [np.asarray([ g.func(x) for x in r]) for g in gaussians]
data = reduce(operator.add, vecs)
estimate(m, v, data, vecs)
plot.plot(r, np.ravel(vecs[0]), "b",
          r, np.ravel(vecs[1]), "r",
          r, np.ravel(vecs[2]), "g",
          r, np.ravel(data), "k")
plot.show()

