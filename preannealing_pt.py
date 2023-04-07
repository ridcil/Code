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
# label = ''

class Ec():
    def Electrochem(path, thickness, area, sample_name):
        delith = pd.DataFrame()
        lith = pd.DataFrame()
        cv_df = pd.DataFrame()
        capacity = pd.DataFrame(columns = [_cap, 'Cycle', 'Sample', 'Average Current Density ($\mu$A/cm$^3$)', 'Charge/Discharge'])
        capacity_d = pd.DataFrame(columns = [_cap, 'Cycle', 'Sample', 'Average Current Density ($\mu$A/cm$^3$)', 'Charge/Discharge'])
        final_file = pd.DataFrame()
        for i in os.listdir(path):                          # make 3 folders in path: CV, delith, lith to separate files
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
                    cv_df = cv
                    # cv_df['CV'] = label
                    sns.scatterplot(data = cv, x = cols[0], y = cols[2], edgecolor = None, s = 3, ax = ax)#, palette=palette) #, label = label)         
                # ax.legend(markerscale = 5)
                plt.title(sample_name)
                # plt.xlim(3.3,4.5)
                plt.show()                      # You can skip this line if you dont want thge Cv plot
                plt.close()
                                
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
                        capacity_d.loc[n] = [max(dl[cols2[3]]) /3.6 / (area * 1e-7 * thickness), int(x[-6:-4]), sample_name, dl[cols2[2]].mean() * 1e6 / area, ''] # calculated capacity
                        capacity_d['Charge/Discharge'] = 'Charge'
                        final_file = pd.concat([final_file, capacity_d])
                        n += 1
                    delith[_cap] = delith[cols2[3]] /3.6 / (area * 1e-7 * thickness)
                    # fig, ax = plt.subplots(1, 2, facecolor = 'white', dpi = dpi, figsize = figsize, gridspec_kw={'width_ratios': [3, 2]})
                    # sns.lineplot(data = delith, x = _cap, y = cols2[1], hue = 'Cycle', palette=palette, legend = False, ax = ax[0], lw = linewidth)
                    # plt.colorbar(cbar, ax = ax[0]).set_label('Cycle')
                    # sns.scatterplot(data = capacity_d, x = 'Cycle', y = _cap, ax = ax[1])
                    # plt.suptitle(path[-5:])
                    # plt.show()                      # You can skip this line if you dont want thge Cv plot
                    # plt.close()
            
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
                        final_file = pd.concat([final_file, capacity])
                        n += 1
                    lith[_cap] = -1 * lith[cols2[3]] /3.6 / (area * 1e-7 * thickness)
                    
                    
                    
                    fig, ax = plt.subplots(1, 3, facecolor = 'white', dpi = dpi, figsize = figsize) #, gridspec_kw={'width_ratios': [3, 2]})
                    sns.lineplot(data = lith, x = _cap, y = cols2[1], hue = 'Cycle', palette=palette, legend = False, ax = ax[0], lw = linewidth)
                    #
                    sns.lineplot(data = delith, x = _cap, y = cols2[1], hue = 'Cycle', palette=palette, legend = False, ax = ax[0], lw = linewidth)
                    #                
                    plt.colorbar(cbar, ax = ax[0]).set_label('Cycle')
                    # ax2 = ax[1].twinx()
                    sns.scatterplot(data = final_file, x = 'Cycle', y = _cap, ax = ax[1], hue = 'Charge/Discharge')
                    
                    
                    # sns.scatterplot(data = capacity, x = 'Cycle', y = 'Average Current ($\mu$A)', markers = '^', ax = ax2, c = 'navy', label = 'Current')
                    # ax2.scatter(capacity['Cycle'], capacity['Average Current Density ($\mu$A/cm$^3$)'], marker = '^', c = 'navy', label = 'Current')
                    # ax2.set_ylim(min(capacity['Average Current Density ($\mu$A/cm$^3$)']) - 0.5, max(capacity['Average Current Density ($\mu$A/cm$^3$)']) + 0.5)
                    # ax2.set_ylabel('Average Current Density ($\mu$A/cm$^3$)')
                    # ax[1].legend(bbox_to_anchor=(0.3, 1.1), fontsize = 8, frameon = False)
                    # ax2.legend(bbox_to_anchor=(0.95,1.1), fontsize = 8, frameon = False)
                    plt.suptitle(sample_name)
                    plt.show()
                    plt.close()
                    
                    # fig, ax = plt.subplots(dpi = dpi)
                    # sns.lineplot(data = lith, x = cols2[0], y = cols2[1], hue = 'Cycle', palette=palette)
                    # plt.suptitle(path[-5:])
                    # plt.show()
                    # plt.close()
                    
                    # fig, ax = plt.subplots(dpi = dpi)
                    # sns.lineplot(data = lith, x = cols2[0], y = cols2[2])
                    # plt.suptitle(path[-5:])
                    # plt.show()
                    # plt.close()
                
        return cv_df, final_file, lith, delith     # Returns Data frame with lithiation data (capacity, cycle, sample)