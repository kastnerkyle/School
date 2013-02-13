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

N = 10
noise_var = B = .1
#Calculate using the Penrose-Moore Pseudo Inverse - direct calculation seems to have some numerical instability
MPSI = False
data = w = np.matrix(np.random.randn(N,1))
w += np.sqrt(B)*np.random.randn(N,1)
basis = np.matrix(np.zeros((N,N)))
for m in range(N):
    for n in range(N):
        basis[m,n] = gen_gaussian(w[n],m,n)
        #basis[m,n] = gen_dft(m,n,N)
test_data = q = w + np.sqrt(B)*np.random.randn(N,1)
t = basis*(q)
use_MPSI = basis.shape[0] != basis.shape[1] or MPSI == True
if use_MPSI:
    maximum_likelihood = wml = np.linalg.inv(basis.conj().T*basis)*basis.conj().T*t
else:
    maximum_likelihood = wml = np.linalg.inv(basis)*t
f, axarr = plot.subplots(3)
axarr[0].plot(np.real(w))
axarr[0].set_title("Training data with $\\beta=$"+`noise_var`+" variance additive noise")
axarr[1].plot(np.real(q))
axarr[1].set_title("Test data with $\\beta=$"+`noise_var`+" variance additive noise")
axarr[2].plot(np.real(wml))
axarr[2].set_title("Recovered data using " + ("Penrose-Moore pseudoinverse" if use_MPSI else "matrix inverse"))
plot.show()
