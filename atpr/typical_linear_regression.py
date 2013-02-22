#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
import math

def gen_dft(m,n,N):
    return np.exp(-1j*2*math.pi*m*n/N)

def gen_polynomial(x, m):
    return x**m

N = 100
#N_basis works well at low values for polynomial regression but dft regression needs more...
N_basis = 6
noise_var = B = .2

basis = np.matrix(np.zeros((N,N)), dtype=np.complex64)
xs = np.matrix(np.arange(N)/float(N)).T
num_cycles = 6
ys = np.sin(num_cycles*2*np.pi*xs)
w = ys + np.sqrt(B)*np.random.randn(N,1)
#Trained on model data rather than measured...
for m in range(N_basis):
    for n in range(N):
        if n == 0:
            basis[m,n] = 1.0
        else:
            #basis[m,n] = gen_dft(m,n,N)
            basis[m,n] = gen_polynomial(w[n], m)

test_data = t = basis*w #+ np.sqrt(B)*np.random.randn(N,1))

#Calculate using the Moore-Penrose pseudoinverse using the following formula
#maximum_likelihood = wml = np.linalg.inv(basis.T*basis)*basis.T*t
#Direct calculation appears to have numerical instability issues...
#Luckily the pinv method calculates Moore-Penrose pseudo inverse using SVD, which largely avoids the numerical issues
maximum_likelihood = wml = np.linalg.pinv(basis)*t

plot.figure()
plot.plot(ys, 'k')
plot.plot(w, 'b')
plot.plot(np.real(wml), 'g')
plot.show()
