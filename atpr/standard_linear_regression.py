#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
import math

def gen_dft(m, n, N):
    return np.exp(1j*-2*m*n/N)

def gen_polynomial(x, m):
    return x**m

N = 10
N_basis = 3
noise_var = B = 5
basis = np.matrix(np.zeros((N_basis,N)), dtype=np.complex64)
xs = np.matrix(range(N)).T
ys = np.square(xs) - 4*xs + 1
wm = ys + np.sqrt(B)*np.random.randn(N,1)
for m in range(N_basis):
    for n in range(N):
        if m == 0:
            basis[m,n] = 1.0
        else:
            basis[m,n] = gen_polynomial(xs[n], m)
            #To use the gen_dft basis, make sure to set N_basis = N
            #basis[m,n] = gen_dft(m, n, N)

test_data = t = basis*wm
#Calculate using the Moore-Penrose pseudoinverse using the following formula
#maximum_likelihood = wml = np.linalg.inv(basis.T*basis)*basis.T*t
#Direct calculation appears to have numerical instability issues...
#Luckily the pinv method calculates Moore-Penrose pseudo inverse using SVD, which largely avoids the numerical issues
maximum_likelihood = wml = np.linalg.pinv(basis)*t

plot.figure()
plot.title("Regression fit using polynomial basis function, number of basis functions = $" + `N_basis` + "$")
plot.plot(ys, 'b')
plot.plot(wm, 'ro')
plot.plot(np.real(wml), 'g')
plot.show()
