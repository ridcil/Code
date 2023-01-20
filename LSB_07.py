import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

# Linear Fit
def line(x, m, b):
    return x * m + b

gmodel = Model(line)
param1 = gmodel.make_params(m = 1, b = 1)
param1['m'].set(min = 0)

# Function
def r_t(s, r_s, l_t, N, W, L):
    return (r_s * s / (N * W + (N-1) * (2 *s + L))) + (2 * r_s * l_t / (N * W + (N-1) * (2 *s + L)))

#Create model and parameters
gmodel5 = Model(r_t)
param5 = gmodel5.make_params()
param5['r_s'].set(value = 1e10, min = 0)
param5['l_t'].set(value = 1, min = 0)
param5['L'].set(value = 3200e-4, vary = False)
param5['W'].set(value = 5e-4, vary = False)
param5['N'].set(value = 60, vary = False)

class contact_resistance():

    def resistance(path, thickness, name):
        col = ['Potential (V)', 'Current (A)']
        col2 = ['Spacing (cm)', 'Resistance ($\Omega$)', 'Structure', 'Sample']
        spacing = [2e-4, 5e-4, 10e-4, 20e-4]
        files = [os.path.join(path, i) for i in os.listdir(path)  if 'README.txt' != i]
        # sample = path[-5:]
        resistance = pd.DataFrame(columns = col2)
        files.sort(key = (lambda x: x[-6:-4])) # sort files by last part of string
        n = 0
        for i in files:
            df = pd.read_csv(i, names = col, sep = ';', skiprows = 1, usecols=[0,1])
            r = gmodel.fit(df[col[1]], param1, x = df[col[0]])
            slope = r.best_values['m']
            resistance.loc[n] = [spacing[n], 1/ slope, i[-10:-4], name]
            n += 1 
        
        result = gmodel5.fit(resistance[col2[1]], param5, s = resistance[col2[0]])
        rc2 = gmodel5.eval(result.params, s = 0)
        rs = result.values['r_s']
        sigma = 1/  (rs * thickness * 1e-7)

        plt.plot(resistance[col2[0]], result.best_fit)
        return resistance, (rs, rc2/2, sigma, name)


