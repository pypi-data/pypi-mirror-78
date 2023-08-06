import matplotlib.pyplot as ppl
from numpy.random import randn
import numpy as np
from numpy import pi

from pyboat import WAnalyzer, ssg

ppl.ion()

periods = np.linspace(6,90,150)
dt = 3 # the sampling interval
T_cut_off = 65 # cut off period
time_unit = 's'

# --- create a synthetic signal ---

eps = 0.5 # noise intensity
alpha = 0.4 # AR1 parameter
Nt = 400 # number of samples

signal1 = ssg.create_noisy_chirp(T1 = 30 / dt, T2 = 50 / dt, Nt = Nt, eps = eps, alpha = alpha)

# add slower oscillatory trend
signal2 = ssg.create_chirp(T1 = 70 / dt, T2 = 70 / dt, Nt = Nt)

# linear superposition
signal = signal1 + 1.5 * signal2

# set up analyzing instance
wAn = WAnalyzer(periods, dt, T_cut_off, time_unit_label = time_unit)

# plot signal and trend
wAn.plot_signal(signal)
wAn.plot_trend(signal)
ppl.legend(ncol = 2)
# wAn.plot_detrended(signal1)

# compute the spectrum without detrending
wAn.compute_spectrum(signal, sinc_detrend = False)

# compute the spectrum with detrending (sinc_detrend = True is the default)
wAn.compute_spectrum(signal)

wAn.get_maxRidge(power_thresh = 5)
wAn.draw_Ridge()
ppl.savefig('detr_signal_spec.png')

wAn.plot_readout(draw_coi = True)
ppl.savefig('detr_signal_readout.png')

rd = wAn.ridge_data # this is a pandas DataFrame holding the ridge results

