#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
import math

def gen_dft(m,n,N):
    return np.exp(-1j*2*math.pi*m*n/N)

def gen_gaussian(x,m,n):
    if n == 0:
        return 1.0
    else:
        return np.exp(-(np.abs(x-m)**2)/(2*float(n)**2))

N = 50
noise_var = B = 1
#Calculate using the Moore-Penrose pseudoinverse
MPSI = True
#data = np.matrix([np.sin(x)+2 for x in np.linspace(-np.pi,np.pi,N)]).T
data = np.matrix(np.random.randn(N,1))
w = data + np.sqrt(B)*np.random.randn(N,1)
basis = np.matrix(np.zeros((N,N)))
for m in range(N):
    for n in range(N):
        basis[m,n] = gen_gaussian(w[n],m,n)
        #basis[m,n] = gen_dft(m,n,N)
test_data = q = data + np.sqrt(B)*np.random.randn(N,1)
t = basis*q
use_MPSI = basis.shape[0] != basis.shape[1] or MPSI == True
if use_MPSI:
    #Direct calculation appears to have numerical instability issues...
    #maximum_likelihood = wml = np.linalg.inv(basis.T*basis)*basis.T*t
    maximum_likelihood = wml = np.linalg.pinv(basis)*t
else:
    maximum_likelihood = wml = np.linalg.inv(basis)*t
plot.plot(np.real(w), 'b')
plot.plot(np.real(q), 'r--')
plot.plot(np.real(wml), 'g:')
plot.show()
