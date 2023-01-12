import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns
from pathlib import Path

palette = 'BuPu_r'
dpi = 200
linewidth = 3
figsize = [10,3]
cols = ['Potential vs Li$^+$/Li (V)','Current Density ($\mu$A/cm$^2$)']
cols2 = ['Time (s)', cols[0], 'Current (A)', 'Charge (C)', 'Capacity (mAh/cm$^3$)']
label = ''

path = r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_10\lith'
thickness = 90
lith = pd.DataFrame()
lith_files = [os.path.join(path, j) for j in os.listdir(path)]
Z = [[0,0],[0,0]]
cbar = plt.contourf(Z, levels = np.arange(0, len(lith_files) + 1, 1), cmap=palette)
plt.clf()
n = 0
capacity = pd.DataFrame(columns = [cols2[4], 'Cycle']) ##
for x in lith_files:
    l = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
    l['Cycle'] = int(x[-6:-4])
    lith = pd.concat([lith, l])
    #capacity.loc[n] = [max(l[cols2[4]]), int(x[-6:-4])]
    capacity.loc[n] = [-1 * min(l[cols2[3]]) /3.6 / (0.63 * 1e-7 * thickness), int(x[-6:-4])]
    n += 1
fig, ax = plt.subplots(1, 2, facecolor = 'white', dpi = dpi, figsize = figsize, gridspec_kw={'width_ratios': [3, 2]})
sns.lineplot(data = lith, x = cols2[4], y = cols2[1], hue = 'Cycle', palette=palette, legend = False, ax = ax[0], lw = linewidth)
plt.colorbar(cbar, ax = ax[0]).set_label('Cycle')
sns.scatterplot(data = capacity, x = 'Cycle', y = cols2[4], ax = ax[1])
plt.suptitle(path[-5:])
plt.show()
plt.clf()
#print(min(l[cols2[3]]))