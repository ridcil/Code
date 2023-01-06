import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns
from pathlib import Path

palette = 'Blues_r'
dpi = 100
figsize = [10,3]
cols = ['Potential vs Li$^+$/Li (V)','Current Density (A/cm$^2$)']
cols2 = ['Time (s)', cols[0], 'Current (A)', 'Charge (C)', 'Capacity (mAh/cm$^3$)']

class Ec():
    def Electrochem(path):
        delith = pd.DataFrame()
        lith = pd.DataFrame()
        for i in os.listdir(path):
            if 'CV' not in os.listdir(path):
                os.mkdir(os.path.join(path, 'CV'))
                os.mkdir(os.path.join(path, 'delith'))
                os.mkdir(os.path.join(path, 'lith'))
            if '_CV_' in i:
                os.rename(os.path.join(path, i), os.path.join(path, 'CV', i))
            elif '_delith_' in i:
                os.rename(os.path.join(path, i), os.path.join(path, 'delith', i))
            elif '_lith_' in i:
                os.rename(os.path.join(path, i), os.path.join(path, 'lith', i))

        f_delith = [os.path.join(path, 'delith', i)  for i in os.listdir(os.path.join(path, 'delith')) if i != 'README.txt']
        f_lith = [os.path.join(path, 'lith', i)  for i in os.listdir(os.path.join(path, 'lith')) if i != 'README.txt']
        m = 1
        for i in f_delith:
            if '_' in  i[-6]:
                os.renames(i, i[:-5] + '0' + str(m) + '.txt')
                m += 1 
        m = 1
        for i in f_lith:
            if '_' in  i[-6]:
                os.renames(i, i[:-5] + '0' + str(m) + '.txt')
                m += 1 
##############
        files = [os.path.join(path, i)  for i in os.listdir(path) if i != 'README.txt']

        for i in files:
            if 'CV' in i:
                cv_files = [os.path.join(i, j) for j in os.listdir(i)] 
                for x in cv_files:
                    cv = pd.read_csv(x, names = cols, sep = ';', skiprows=1, usecols=[0, 4])
                fig, ax = plt.subplots(facecolor = 'white', dpi = dpi)
                sns.scatterplot(data = cv, x = cols[0], y = cols[1], edgecolor = None, s = 3, color = 'tab:purple', ax = ax)
                plt.show()
                plt.clf()
            elif 'delith' in i:
                delith_files = [os.path.join(i, j) for j in os.listdir(i)]
                Z = [[0,0],[0,0]]
                cbar = plt.contourf(Z, levels = np.arange(0, len(delith_files) + 1, 1), cmap=palette)
                plt.clf()
                n = 0
                
                capacity_d = pd.DataFrame(columns = [cols2[4], 'Cycle'])
                for x in delith_files:
                    dl = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
                    dl['Cycle'] = int(x[-6:-4])
                    delith = pd.concat([delith, dl])
                    capacity_d.loc[n] = [max(dl[cols2[4]]), int(x[-6:-4])]
                    n += 1
                fig, ax = plt.subplots(1, 2, facecolor = 'white', dpi = dpi, figsize = figsize, gridspec_kw={'width_ratios': [3, 2]})
                sns.lineplot(data = delith, x = cols2[4], y = cols2[1], hue = 'Cycle', palette=palette, legend = False, ax = ax[0])
                plt.colorbar(cbar, ax = ax[0]).set_label('Cycle')
                sns.scatterplot(data = capacity_d, x = 'Cycle', y = cols2[4], ax = ax[1])
                plt.show()
                plt.clf()
                # plt.suptitle('Main title')
                
            elif '\lith' in i:
                lith_files = [os.path.join(i, j) for j in os.listdir(i)]
                Z = [[0,0],[0,0]]
                cbar = plt.contourf(Z, levels = np.arange(0, len(delith_files) + 1, 1), cmap=palette)
                plt.clf()
                n = 0
                
                capacity = pd.DataFrame(columns = [cols2[4], 'Cycle'])
                for x in lith_files:
                    l = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
                    l['Cycle'] = int(x[-6:-4])
                    lith = pd.concat([lith, l])
                    capacity.loc[n] = [max(l[cols2[4]]), int(x[-6:-4])]
                    n += 1
                fig, ax = plt.subplots(1, 2, facecolor = 'white', dpi = dpi, figsize = figsize, gridspec_kw={'width_ratios': [3, 2]})
                sns.lineplot(data = lith, x = cols2[4], y = cols2[1], hue = 'Cycle', palette=palette, legend = False, ax = ax[0])
                plt.colorbar(cbar, ax = ax[0]).set_label('Cycle')
                sns.scatterplot(data = capacity, x = 'Cycle', y = cols2[4], ax = ax[1])
                plt.show()
                plt.clf()
            
        return delith, lith

    def fix_name(path):
        files = [os.path.join(path, i)  for i in os.listdir(path) if i != 'README.txt']
        n = 1
        for i in files:
            if '_' in  i[-6]:
                os.renames(i, i[:-5] + '0' + str(n) + '.txt')
                n += 1             