import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

palette = 'Blues'
cols = ['Potential vs Li$^+$/Li (V)','Current Density (A/cm$^2$)']
cols2 = ['Time (s)', cols[0], 'Current (A)', 'Charge (C)', 'Capacity (mAh/cm$^3$)']
class Ec():
    def Electrochem(path):
        files = [os.path.join(path, i)  for i in os.listdir(path) if i != 'README.txt']
        for i in files:
            if 'CV' in i:
                cv_files = [os.path.join(i, j) for j in os.listdir(i)] 
                for x in cv_files:
                    cv = pd.read_csv(x, names = cols, sep = ';', skiprows=1, usecols=[0, 4])
                    sns.scatterplot(data = cv, x = cols[0], y = cols[1], edgecolor = None, s = 3, color = 'tab:blue')
                    plt.show()
                    plt.clf()
            elif 'delith' in i:
                delith_files = [os.path.join(i, j) for j in os.listdir(i)]
                Z = [[0,0],[0,0]]
                cbar = plt.contourf(Z, levels = np.arange(0, len(delith_files) + 1, 1), cmap=palette)
                plt.clf()
                n = 0
                delith = pd.DataFrame()
                for x in delith_files:
                    dl = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
                    dl['Cycle'] = int(x[-6:-4])
                    delith = pd.concat([delith, dl])
                    n += 1
                sns.lineplot(data = delith, x = cols2[4], y = cols2[1], hue = 'Cycle', palette=palette, legend = False)
                plt.colorbar(cbar).set_label('Cycle')
                plt.show()
                plt.clf()
                
            elif '\lith' in i:
                lith_files = [os.path.join(i, j) for j in os.listdir(i)]
                Z = [[0,0],[0,0]]
                cbar = plt.contourf(Z, levels = np.arange(0, len(delith_files) + 1, 1), cmap=palette)
                plt.clf()
                n = 0
                lith = pd.DataFrame()
                for x in lith_files:
                    l = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
                    l['Cycle'] = int(x[-6:-4])
                    lith = pd.concat([lith, l])
                    n += 1
                sns.lineplot(data = lith, x = cols2[4], y = cols2[1], hue = 'Cycle', palette=palette, legend = False)
                plt.colorbar(cbar).set_label('Cycle')
                plt.show()
                plt.clf()
