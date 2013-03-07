#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot

N = 10
noise_var = B = .2**2
lower_bound = lb = -1.
upper_bound = ub = 1.
xs = np.matrix((ub-lb)*np.random.rand(N)+lb).T
xaxis = np.matrix(np.linspace(lb,ub,num=N)).T
w = np.array([1, -4, 1])
#w = np.array([-.3, .5])
ys = w[0] + w[1]*xaxis# + w[2]*np.square(xs)
t = w[0] + w[1]*xs + np.sqrt(B)*np.random.randn(N,1);
plot.plot(xaxis, ys, "b")
plot.plot(xaxis, t, "ro")

def gen_polynomial(x, p):
    return x**p
N_basis = 2
alpha = a = 1.
beta = b = 1./B;
prior_m = np.zeros((N_basis, 1))
m = np.zeros((N_basis, N))
prior_s = np.matrix(np.diag(np.array([a]*N_basis)))
s = np.zeros((N_basis, N_basis))
for n in range(N):
    #0. is important... otherwise matrix is set to int by default!
    basis = np.matrix([0.]*N_basis)
    for i in range(N_basis):
        basis[0,i] = gen_polynomial(xs[n], i)
    s_inv = prior_s.I*np.eye(N_basis)+b*(basis.T*basis)
    s = s_inv.I*np.eye(N_basis)
    tmp = s*(prior_s.I*prior_m+(b*basis.T*t[n]))
    for i in range(N_basis):
        m[i,n] = tmp[i,0]
    y = m[0,n]+m[1,n]*xaxis#+m[2,n]*np.square(xs)
    plot.plot(xaxis, y, "g")
    for i in range(N_basis):
        prior_m[i,0] = m[i,n]
    prior_s = s

plot.plot(xaxis, y, "k")
plot.show()
