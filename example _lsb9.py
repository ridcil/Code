import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns
from pathlib import Path
from matplotlib.ticker import MaxNLocator

from cv_charge_discharge import Ec # Make sure to have the file 'cv_charge_discharge.py' in the same directory

# The key in this dictionary is the name of the sample and the string to be displayed in the legend of the final plot
paths = {'700°C 60 min ramp2' : r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_08',
         '700°C 100 sccm 20 min ramp2' : r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_09',
         '800°C 100 sccm 20 min' : r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_10',
         '800°C 1000 sccm 20 min' : r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_11',
         '800°C 100 sccm 60 min' : r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_12',
         '750°C 100 sccm 20 min ramp2' : r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_13'
         }
save_path = r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09'
lsb_09 = pd.DataFrame()
for i in paths.keys():
    capacity = Ec.Electrochem(paths[i], 80)
    capacity['Sample'] = i
    lsb_09 = pd.concat([lsb_09, capacity], ignore_index = True)
    
fig, ax = plt.subplots(facecolor = 'white', dpi = 200)
ax = sns.scatterplot(data = lsb_09, x = 'Cycle', y = 'Capacity (mAh/cm$^3$)', hue = 'Sample', style = 'Sample', s = 150)
sns.move_legend(ax, "lower center", ncol = 2, bbox_to_anchor=(0.5, 1), frameon = False, title = None)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.xlim(0,15.5)
plt.show()
lsb_09.to_csv(r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\lsb_09.txt', index = False)