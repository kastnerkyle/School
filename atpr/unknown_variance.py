#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plot
total_obs = 20000
obs_granularity = N = 10
primary_mean = 5
primary_var = 14
x = np.sqrt(primary_var)*np.random.randn(total_obs) + primary_mean
group = x[:N]
all_a = []
all_b = []
all_meanprec = []
all_varprec = []
prior_a=N/2.+1
prior_b=1/2.*np.sum((group-primary_mean)**2)
plot.figure()
plot.plot(x)
for i in range(1,int(float(total_obs)/N)-1):
    group=x[N*i:N*(i+1)]
    posterior_a=prior_a+N/2.
    posterior_b=prior_b+1/2.*np.sum((group-primary_mean)**2)
    all_a.append(posterior_a)
    all_b.append(posterior_b)
    all_meanprec.append(posterior_a/posterior_b)
    all_varprec.append(posterior_a/(posterior_b**2))
    prior_a=posterior_a
    prior_b=posterior_b

plot.figure()
print "Estimated variance is " + `1./all_meanprec[-1]`
print "Confidence in variance estimation is " + `1-all_varprec[-1]`
plot.plot(all_meanprec)
plot.figure()
plot.plot(all_varprec)
plot.show()
