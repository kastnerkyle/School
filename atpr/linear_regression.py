#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
import math
import sys

def gen_dft(m,n,N):
    return np.exp(-1j*2*math.pi*m*n/N)

N = 10
data = w = np.matrix(np.random.randn(N,1))
basis = np.matrix(np.zeros((N,N)))
for m in range(N):
    for n in range(N):
        basis[m,n] = gen_dft(m,n,N)
output = t = basis*w
maximum_likelihood = wml = np.linalg.inv(basis)*t
#maximum_likelihood = wml = np.linalg.inv(basis.conj().T*basis)*basis.conj().T*t
plot.plot(np.real(w))
plot.plot(np.real(wml))
plot.show()
