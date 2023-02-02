import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from lmfit import Model

from scipy.stats import linregress

# MODEL
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

col_aut = ['Potential (V)', 'Current (A)', 'Time (s)']
col_r = ['Spacing ($\mu$m)', 'Resistance (M$\Omega$)']
col_v = ['Sheet resistance ($\Omega$/sq)', 'Contact resistance ($\Omega$/sq)', 'Conductivity (S/cm)']
        
class idea():
    def fit(files, thickness):
        df_aut = pd.DataFrame()
        r_aut = pd.DataFrame(columns = col_r)
        values = pd.DataFrame(columns = col_v)
        n = 0
        for i in files:         # files.sort(key = (lambda x: x[-6:-4])) # sort files by last part of string
            df = pd.read_csv(i, sep = ';', names = col_aut, skiprows = 1)
            slope, intercept, rvalue, pvalue, stderr = linregress(df[col_aut[0]], df[col_aut[1]])
            df['Structure'] = i[-7:-4]
            if i[-5:-4] == '1':
                df['Spacing ($\mu$)'] = 2e-4
                r_aut.loc[n] = [2e-4, 1/slope]
            elif i[-5:-4] == '2':
                df['Spacing ($\mu$)'] = 5e-4
                r_aut.loc[n] = [5e-4, 1/slope]
            elif i[-5:-4] == '3':
                df['Spacing ($\mu$)'] = 10e-4
                r_aut.loc[n] = [10e-4, 1/slope]
            elif i[-5:-4] == '4':
                df['Spacing ($\mu$)'] = 20e-4
                r_aut.loc[n] = [20e-4, 1/slope]
            df_aut = pd.concat([df_aut, df])
            n += 1

        result = gmodel5.fit(r_aut[col_r[1]], param5, s = r_aut[col_r[0]])
        rc2 = gmodel5.eval(result.params, s = 0)
        rs = result.values['r_s']
        sigma = 1/  (rs * thickness * 1e-7)
        values.loc[0] = [rs, rc2 / 2, sigma]
        # Plots
        fig, ax = plt.subplots(dpi = 100)
        sns.scatterplot(data = r_aut, x = col_r[0], y = col_r[1])
        ax.plot(r_aut[col_r[0]], result.best_fit)
        ax.xaxis.set_major_formatter(lambda x, pos: '{:.0f}'.format(x * 1e4))
        ax.yaxis.set_major_formatter(lambda x, pos: '{:.0f}'.format(x / 1e6))
        
        return df_aut, r_aut, values