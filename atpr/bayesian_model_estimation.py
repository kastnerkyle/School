#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot

N = 10.
noise_var = B = .2**2
lower_bound = lb = 0.
upper_bound = ub = 5.
xs = np.matrix(sorted((ub-lb)*np.random.rand(N)+lb)).T
xaxis = np.matrix(np.linspace(lb,ub,num=N)).T
w = np.array([1, -4, 1])
ys = w[0] + w[1]*xaxis + w[2]*np.square(xaxis)
t = w[0] + w[1]*xs + +w[2]*np.square(xs) + np.sqrt(B)*np.random.randn(N,1);

prior_alpha = 0.01 #Low precision initially
prior_beta = 0.01 #Low guess for noise var
max_N = 7 #Upper limit on model order
evidence = E = np.zeros(max_N)
plot.figure()
def gen_polynomial(x, p):
    return x**p
for order in range(1, max_N+1):
    m = np.zeros((order, 1))
    s = np.zeros((order, order))
    poly = np.vectorize(gen_polynomial)
    xs = np.matrix(np.arange(10)).T
    basis = poly(xs, np.tile(np.arange(order), N).reshape(N, order))
    alpha = a = prior_alpha
    beta = b = prior_beta
    itr = 0
    end_while = False
    while end_while and itr < 100:
        itr += 1
        s_inv = a*np.eye(order)+b*(basis.T*basis)
        m = b*(s_inv.I*(basis.T*t))
        posterior_alpha = pa = np.matrix(order/(2*(m.T*m)))
        posterior_beta = pb = np.matrix(N/(2*(t.T-m.T*basis.T)*(t.T-m.T*basis.T).T))
        if abs(pa-a)/abs(a) < .01 and abs(pb-b)/abs(b)<0.01:
            end_while = True
        a = pa
        b = pb
    A = a*np.eye(order)+b*(basis.T)*basis
    mn = b*(A.I*(basis.T*t))
    penalty = emn = b/2.*(t.T-mn.T*basis.T)*(t.T-mn.T*basis.T).T+a/2.*mn.T*mn
    E[order-1] = order/2.*np.log(a)+N/2.*np.log(b)-emn-1./(2*np.log(np.linalg.det(A)))-N/2.*np.log(2*np.pi)
    y = (mn.T*basis.T).T
    plot.plot(xs, y)

plot.title("Bayesian regression using polynomial basis function, number of basis functions") #= $" + `N_basis` + "$")
plot.plot(xaxis, ys, "b")
plot.plot(xs, t, "ro")
plot.figure()
plot.plot(E, "k")
plot.show()
