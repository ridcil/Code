import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_fit(path, sample):
    spectra = [os.path.join(path, i) for i in os.listdir(path) if 'Spectra' in i]
    fit = [os.path.join(path, i) for i in os.listdir(path) if 'Fit' in i]
    col = ["Frequency Hz",	"Z' ($\Omega$)",	"-Z'' ($\Omega$)",	"Fit Frequency (Hz)",	"Fit Z' ($\Omega$)",	"Fit -Z'' ($\Omega$)"]
    df = pd.read_csv(spectra[0], sep = '\t', skiprows = 4, names = col)
    df[col[2]] = -df[col[2]]
    df[col[5]] = -df[col[5]]
    fig, ax = plt.subplots(dpi = 100)
    sns.scatterplot(data = df, x =col[1], y = col[2])
    sns.lineplot(data = df, x = col[4], y = col[5])
    plt.show()
    fit_values = pd.read_csv(fit[0], sep = '\t', skiprows = 2) 
    return df, fit_values
    
sample = 'Li TFSI:BMP TFSI  2:1'
thickness = 0.035 # cm
area = np.pi * 1**2 # cm2
path = r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Impedance\Solid Electrolyte\Comeback\BMP LiTFSI\1_2\Good signal'
fit, values = data_fit(path, sample)
electrolyte_r = values['Resistance 1: value']
conductivity = thickness / (electrolyte_r *area)  #thickness/area*resistance
conductivity