#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
import math
import sys

def gen_dft(m,n,N):
    return np.exp(-1j*2*math.pi*m*n/N)

def gen_gaussian(m,n):
    if n == 0:
        return 1.0
    else:
        return np.exp(-(m**2)/(float(n)**2))

N = 10
#Calculate using the Penrose-Moore Pseudo Inverse
PMSI = False
data = w = np.matrix(np.random.randn(N,1))
basis = np.matrix(np.zeros((N,N)))
for m in range(N):
    for n in range(N):
        basis[m,n] = gen_gaussian(m,n)
        #basis[m,n] = gen_dft(m,n,N)
output = t = basis*w
if basis.shape[0] != basis.shape[1] or PMSI == True:
    maximum_likelihood = wml = np.linalg.inv(basis.conj().T*basis)*basis.conj().T*t
else:
    maximum_likelihood = wml = np.linalg.inv(basis)*t
plot.plot(np.real(w))
plot.plot(np.real(wml))
plot.show()
