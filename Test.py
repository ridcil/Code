import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import statistics as sts
from lmfit import Model
from scipy.stats import sem

# Variables for names and files
mask = 'IDEA2 '
metal = 'Al'
resist = 'LMO_IX'
sample = '0G_11 '
folder = 'C4_P08'
name = mask + metal + ' on LMO ' + sample + folder
file = folder + '.txt'
path = os.path.join(Path.cwd().parent.parent, 'Contact Resistance', 'LSB_07', 'LCR', 'csv', mask + metal, resist)
dir = os.listdir(path)

# Get dictionary of data DC, Idc and Vds
dict = {}
for i in dir:
    data = pd.read_csv(os.path.join(path,i))
    dict[i] = (data['DC'], data['Idc'], data['Vds'])

# Linear Fit
def line(x, m, b):
    return x * m + b
gmodel = Model(line)
param = gmodel.make_params()

# Result of fit. Get resistance, inverse of slope. get r^2
result = gmodel.fit(dict[file][1], param, m = 1, b = 1, x = dict[file][2])
slope = result.values['m']
resistance = 1/slope
r_square = 1 - result.residual.var() / np.var(dict[file][1])

# Plot
fig, ax = plt.subplots(dpi = 400, facecolor = 'white')
ax.set_title(name)
ax.set_xlabel('Potential Vds (V)')
ax.set_ylabel('Current Ids (A)')
ax.scatter(dict[file][0], dict[file][1], s = 1, label = 'Measurement')


# Fit line and extra info to add in the legend
# ax.plot(dict[file][0], result.best_fit, 'k', alpha = 0.5, label = 'Linear Fit')
# ax.plot([],[], ' ', label = '{:.2f}'.format(resistance) + ' $\Omega$')
# ax.plot([],[], ' ', label = 'r$^2$ = ' + '{:.5f}'.format(r_square))

# To plot all files in folder
# mark = ['.', 'v', 's', '*', 'x', 'D'] 
# dir.sort(reverse = True)
# count = 1
# for i in dir:
    # res = gmodel.fit(dict[i][1], param, m = 1, b = 1, x = dict[i][2])
    # ax.scatter(dict[i][2], dict[i][1], s = 5)#, label = i[:-4])
    # ax.plot(dict[i][2], dict[i][1])#, label = i[:-4])
    # ax.plot(dict[i][2], res.best_fit, 'k', alpha = 0.5, lw = 0.8)
    
ax.legend(markerscale = 5)

#Save plot
# plt.savefig(os.path.join(Path.cwd().parent.parent, 'Contact Resistance', 'LSB_07', 'LCR', 'Plots', mask + metal, 'IX', name) + '.png', facecolor = 'white',  bbox_inches='tight')
