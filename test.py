import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

import powerxrd as xrd

sns.set_theme(style="darkgrid")

path = r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\XRD\LSB_07\HS33_02\Data\HS33_02.csv'
cols = ['Angle', 'Intensity']
print(cols)
# df = pd.read_csv(path, skiprows = 30, usecols=[0, 2])

# x, y = np.array(df[cols[0]]), np.array(df[cols[1]])
# data = xrd.Chart(x, y)
# plt.plot(data)
# print(df)