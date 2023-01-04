import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

class Fit():
    def files(path):
        return [os.path.join(path, i) for i in os.listdir(path)]
    
    def r_fit(path, columns, sample_name):
        files = [os.path.join(path, i) for i in os.listdir(path)]
        cols = ['Spacing (cm)', 'Resistance ($\Omega$)']
        cols_r = ['Contact Resistance', 'Sheet resistance', 'Conductivity ($\sigma$)', 'Sample']
        c = pd.DataFrame(columns = cols)
        results = pd.DataFrame(columns = cols_r)
        
        n = 0
        for i in files:
            df = pd.read_csv(i, names = columns, skiprows = 1, sep = ';')
            slope, intercept, r_value, p_value, std_err = linregress(df[columns[0]], df[columns[1]])
            if i[-5:-4] == '1':
                c.loc[n] = [2e-4,  1 / slope]
            elif i[-5:-4] == '2':
                c.loc[n] = [5e-4,  1 / slope]
            elif i[-5:-4] == '3':
                c.loc[n] = [10e-4,  1 / slope]
            elif i[-5:-4] == '4':
                c.loc[n] = [20e-4,  1 / slope]
            n += 1
        c.sort_values(by = ['Resistance ($\Omega$)'], inplace=True)
        c['Sample'] = sample_name
        r = Fit.gmodel5.fit(c[cols[1]], Fit.param5, s = c[cols[0]])
        rc = Fit.gmodel5.eval(r.params, s = 0) # 2 times contact resistance
        l_t = r.best_values['l_t'] # transfer length
        r_s = r.best_values['r_s'] # sheet resistance
        sigma = 1 / (r_s * 0.2e-4)
        results.loc[sample_name] = [rc/2, r_s, sigma, 0]
        results.at[sample_name, 'Sample'] = sample_name
        plt.plot(c[cols[0]], r.best_fit)
        sns.lineplot(data = c, x = cols[0], y = cols[1], marker = 'o', linestyle = '')
        plt.xticks(np.arange(0,21,5) * 1e-4)
        return c, results

    def r_t(s, r_s, l_t, N, W, L):
        return (r_s * s / (N * W + (N-1) * (2 *s + L))) + (2 * r_s * l_t / (N * W + (N-1) * (2 *s + L)))
    gmodel5 = Model(r_t)
    param5 = gmodel5.make_params()
    param5['r_s'].set(value = 1e8, min = 0)
    param5['l_t'].set(value = 1e-5, min = 1e-9)
    param5['L'].set(value = 3200e-4, vary = False)
    param5['W'].set(value = 5e-4, vary = False)
    param5['N'].set(value = 60, vary = False)