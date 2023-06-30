import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

palette = 'BuPu' # Theme for plot
dpi = 200 
linewidth = 1
figsize = [20,5]
cols = ['Potential vs Li$^+$/Li (V)', 'Current (A)', 'Current Density ($\mu$A/cm$^2$)', 'Scan']
cols2 = ['Time (s)', cols[0], 'Current (A)', 'Charge (C)', 'Capacity (mAh cm$^{-3}$)']
_cap = 'Capacity (mAh/cm$^3$)'

def ec(path, thickness, area, sample_name):
    delith = pd.DataFrame()
    lith = pd.DataFrame()
    cv_df = pd.DataFrame()
    capacity = pd.DataFrame(columns = [_cap, 'Cycle', 'Sample', 'Average Current Density ($\mu$A/cm$^3$)', 'Charge/Discharge'])
    capacity_d = pd.DataFrame(columns = [_cap, 'Cycle', 'Sample', 'Average Current Density ($\mu$A/cm$^3$)', 'Charge/Discharge'])
    final_file = pd.DataFrame()
    efficiency = pd.DataFrame()
    for i in os.listdir(path):                          # make folders in path: CV, delith, lith to separate files
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
    files = [os.path.join(path, i)  for i in os.listdir(path) if i != 'README.txt']
    
    # Plot CV, actiation and final together if both are available
    for i in files:                             
        if '\CV' in i[-3:]:
            cv_files = [os.path.join(i, j) for j in os.listdir(i)] 
            cv_files.sort(reverse = True)
            fig, ax = plt.subplots(facecolor = 'white', dpi = dpi)
            for x in cv_files:
                cv = pd.read_csv(x, names = cols, sep = ';', skiprows=1, usecols=[0, 1, 4,5])
                cv[cols[2]] = cv[cols[1]] / area * 1e6 
                if '_Initial_' in x:
                    label = 'Activation CV'
                else:
                    label = 'Final CV'
                cv['CV'] = label
                cv_df = pd.concat([cv_df, cv])
                sns.scatterplot(data = cv, x = cols[0], y = cols[2], edgecolor = None, s = 3, ax = ax)
                            
    # Plot delith profiles
        elif 'delith' in i:
            delith_files = [os.path.join(i, j) for j in os.listdir(i)]
            if len(delith_files) < 1:
                pass
            else:
                Z = [[0,0],[0,0]]                                                                       # Creates color bar
                cbar = plt.contourf(Z, levels = np.arange(0, len(delith_files) + 1, 1), cmap=palette)
                plt.clf()
                n = 0
                for x in delith_files:
                    dl = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
                    dl['Cycle'] = int(x[-6:-4])
                    delith = pd.concat([delith, dl], ignore_index=True) # appending to data frame
                    c_d = max(dl[cols2[3]]) /3.6 / (area * 1e-7 * thickness)
                    capacity_d.loc[n] = [c_d, int(x[-6:-4]), sample_name, dl[cols2[2]].mean() * 1e6 / area, ''] # calculated capacity
                    capacity_d['Charge/Discharge'] = 'Charge'
        
                    n += 1
                
                delith[_cap] = delith[cols2[3]] /3.6 / (area * 1e-7 * thickness)

        # Same as above but for lithiation profiles
        elif '\lith' in i:
            lith_files = [os.path.join(i, j) for j in os.listdir(i)]
            if len(lith_files) < 1:
                pass
            else:
                Z = [[0,0],[0,0]]
                cbar = plt.contourf(Z, levels = np.arange(0, len(lith_files) + 1, 1), cmap=palette)
                plt.clf()
                n = 0
                for x in lith_files:
                    l = pd.read_csv(x, sep = ';', names = cols2, usecols=[1,2,3,4,5], skiprows = 1)
                    l['Cycle'] = int(x[-6:-4])
                    lith = pd.concat([lith, l], ignore_index = True)
                    capacity.loc[n] = [-1 * min(l[cols2[3]]) / 3.6 / (area * 1e-7 * thickness), int(x[-6:-4]), sample_name, l[cols2[2]].mean() * 1e6 / area, ''] # capacity equation. capacity = charge / 3.6 / area * thickness (cm)
                    capacity['Charge/Discharge'] = 'Discharge'
                    n += 1
                lith[_cap] = -1 * lith[cols2[3]] /3.6 / (area * 1e-7 * thickness)
                
    efficiency['Efficiency (%)'] = capacity[_cap] / capacity_d[_cap] * 100
    efficiency['Cycle'] = capacity['Cycle']
    efficiency['Sample'] = sample_name
    final_file = pd.concat([capacity_d, capacity], ignore_index=True)     

    data = [cv_df, final_file, lith, delith]
    for i in data:
        i['Sample'] = sample_name
    
    fig, ax = plt.subplots(1, 4, dpi = 100, figsize = (25, 5))
    sns.scatterplot(data = cv_df, x = 'Potential vs Li$^+$/Li (V)', y = 'Current Density ($\mu$A/cm$^2$)', hue = 'CV', ax = ax[0], edgecolor = None, s = 3)
    sns.lineplot(data = lith, x = 'Capacity (mAh/cm$^3$)', y = 'Potential vs Li$^+$/Li (V)', ax = ax[1], hue = 'Cycle', palette = 'BuPu')
    sns.lineplot(data = delith, x = 'Capacity (mAh/cm$^3$)', y = 'Potential vs Li$^+$/Li (V)', ax = ax[1], hue = 'Cycle', palette = 'BuPu', legend = False)
    sns.scatterplot(data = efficiency[1:], x = 'Cycle' , y = 'Efficiency (%)', ax = ax[3],  c = 'tab:red', s = 100)
    sns.scatterplot(data = final_file[1:], x = 'Cycle', y = 'Capacity (mAh/cm$^3$)', hue = 'Charge/Discharge', style = 'Charge/Discharge', ax = ax[2], legend = True, markers = ['s', '^' ], s = 100)
    plt.suptitle(sample_name)
 
    return cv_df, final_file, lith, delith, efficiency     # Returns Data frame with data (cv, capacity, lithiation, delithiation, efficiency)
