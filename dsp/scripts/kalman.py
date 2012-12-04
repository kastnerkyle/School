#!/usr/bin/python
#Attempt to apply spectral correlation function to data and plot 3D
#http://www.johnvinyard.com/blog/?p=268
import scipy.io.wavfile as wavfile
from scipy.io import loadmat
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plot
from matplotlib import cm
from numpy.lib.stride_tricks import as_strided as ast
import copy
from mpl_toolkits.mplot3d import Axes3D
import random
import scipy.stats as st
import time
import pandas

parser = argparse.ArgumentParser(description="Apply Kalman filter technique to input data")
parser.add_argument(dest="filename", help="WAV file to be processed")
parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="Show verbose output, use -vv for highest verbosity")

def pred_mean(source_scale, prev_mean):
    return source_scale*prev_mean

def pred_sigma(source_scale, prev_sigma, source_sigma):
    return np.sqrt((source_scale**2)*(prev_sigma**2)+source_sigma**2)

def update_mean(pred_mean, pred_sigma, meas_val, meas_sigma):
    pred_mean = float(pred_mean)
    pred_sigma = float(pred_sigma)
    meas_val = float(meas_val)
    meas_sigma = float(meas_sigma)
    numerator = (pred_mean/(pred_sigma**2))+(meas_val/(meas_sigma**2))
    denominator = (1./(pred_sigma**2))+(1./(meas_sigma**2))
    return numerator/denominator

def update_sigma (pred_sigma, meas_sigma):
    r = (1./(pred_sigma**2))+(1./(meas_sigma**2))
    return 1./np.sqrt(r)

def lkfilt(y, source_scale, source_sigma, meas_sigma):
    last_mean = 0
    last_sigma = source_sigma
    k = range(len(y))
    for i in range(len(y)):
        est_mean = pred_mean(source_scale, last_mean)
        est_sigma = pred_sigma(source_scale, last_sigma, source_sigma)
        k[i] = est_mean+st.norm.rvs(scale=est_sigma)
        last_mean = update_mean(est_mean, est_sigma, y[i], meas_sigma)
        last_sigma = update_sigma(est_sigma, meas_sigma)
    return k

def basic_kalman(data):
    source_sigma = .4
    source_scale = np.sqrt(1-source_sigma**2)
    meas_sigma = source_sigma #measurement error?
    k = lkfilt(data, source_scale, source_sigma, meas_sigma)
    plot.plot(k, label="Kalman Filt")
    plot.plot(data, label="Original")
    plot.title("Stock Value over 1998-2012")
    plot.legend(loc=1)
    plot.show()

try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    sys.exit()

if args.filename[-4:] == ".mat":
    mat = loadmat(args.filename)
    data = mat["x"].flatten()
    data = np.asarray(data, dtype=np.complex64)[5000:6000]
    sr = -1
elif args.filename[-4:] == ".wav":
    sr, data = wavfile.read(args.filename)
    data = np.asarray(data, dtype=np.complex64)[5000:6000]
elif args.filename[-4:] == ".txt":
    df = pandas.read_csv(args.filename)
    rm = pandas.rolling_mean(df.Close, len(df.Close)/10000)
    vstd = pandas.rolling_std(df.Close, len(df.Close)/10000)
    vmed = pandas.rolling_median(df.Close, len(df.Close)/10000)
    df['rm'] = rm
    df['vstd'] = vstd
    df['vmed'] = vmed
    df.ix[abs(df.Close - df.rm) > 5*df.vstd, "Close"] = df.ix[abs(df.Close - df.rm) > 5*df.vstd, "vmed"]
    data = np.asarray(df["Close"])
    #data = data[::]
    sr = -1

basic_kalman(data)
