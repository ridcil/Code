import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lmfit import Model
from scipy.stats import linregress
import seaborn as sns

class Ec():
    cols = ['Potential vs Li$^+$/Li (V)','', '', '','', '','Current Density (A/cm$^2$)']
    def Electrochem(path):
        files = [os.path.join(path, i)  for i in os.listdir(path) if i != 'README.txt']
        for i in files:
            if 'CV' in i:
                cv = [os.path.join(i, j) for j in os.listdir(i)] 
                for x in cv:
                    df = pd.read_csv(x, names = cols, skiprows=1)
                    print(df)
                

path = r'C:\Users\lopezb41\OneDrive - imec\Documents\Experiments\Data\Electrochemical\LSB_09\0I_07'
Ec.Electrochem(path)