# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:44:11 2022

@author: detaey21
"""


import tkinter as tk
from tkinter import filedialog
import pandas as pd
import glob
import os
from matplotlib import pyplot as plt
import numpy as np

class deposition():
    
    def __init__(self, file_name):
        self.file_name = file_name
        print(file_name + ' imported.\n')
        self.data = pd.read_csv(file_name,skiprows=3)
        self.convertTimestamp()
        self.targets = self.getTargets()
        self.material = self.getActiveSource()
    
    def getData(self):
        return self.data
    
    def getTargets(self):
        
        targets = []
        for i in range(0,4):
            targets += [self.data['PC Source '+str(i+1)+' Material'][0]]
        
        return targets
    
    def getActiveSource(self):
        for i in range(0,4):
            if 1 in self.data['PC Source '+str(i+1)+' Shutter Open'].unique():
                return self.targets[i]
    
    def convertTimestamp(self):
        ### Adds 2 columns with the absolute time in seconds and the corrected time. ###
        self.data['Time (s)'] = pd.to_datetime(self.data['Time Stamp']).apply(lambda x: x.value/1000000000)
        self.data['Corrected time (s)'] = self.data['Time (s)']-self.data['Time (s)'][0]
        
    def powerSPC(self):
        DCBias = self.data['Power Supply 1 DC Bias'].loc[self.data['PC Substrate Shutter Open']==1]
        
        return DCBias.mean(), DCBias.max(), DCBias.min()
    
    def temperatureSPC(self):
        temp = self.data['Substrate Heater Temperature'].loc[self.data['PC Substrate Shutter Open']==1]
        
        return temp.mean(), temp.max(), temp.min()


    def plotPower(self):
                       
        xdata = self.data['Corrected time (s)']/3600
        y1data = self.data['Power Supply 1 DC Bias']
        y2data = self.data['Power Supply 1 Output Setpoint']
        
        fig = plt.figure()
        plt.xlabel('Time (hour)')
        plt.ylabel('Power (W)')
        
        plt.plot(xdata,y1data,label='Power Supply 1 DC Bias')
        plt.plot(xdata,y2data,label='Power Supply 1 Output Setpoint')
        plt.legend()
        plt.grid(linestyle='--')
        
        return fig
        
    def plotTemp(self):
        
        xdata = self.data['Corrected time (s)']/3600
        y1data = self.data['Substrate Heater Temperature Setpoint']
        y2data = self.data['Substrate Heater Temperature']
        y3data = self.data['Substrate Heater Temperature 2']
        
        fig = plt.figure()
        plt.xlabel('Time (hour)')
        plt.ylabel('Temperature (K)')
        
        plt.plot(xdata,y1data,label='Substrate Heater Temperature Setpoint')
        plt.plot(xdata,y2data,label='Substrate Heater Temperature')
        plt.plot(xdata,y3data,label='Substrate Heater Temperature 2')
        plt.legend()
        plt.grid(linestyle='--')
        
        return fig
        

def selectFiles():
    root = tk.Tk()
    root.withdraw()
    
    chargeDischargeData = {}

    files = filedialog.askopenfilenames()
    
    return files

files = selectFiles()
xdata = []
DCBias_avg = []
DCBias_max = []
DCBias_min = []
T_avg = []
T_max = []
T_min = []
figures = []

for file in files:    
    test = deposition(file)
    if test.material == 'LiPO':
        DCavg, DCmx, DCmn = test.powerSPC()
        xdata += [file]
        DCBias_avg += [DCavg]
        DCBias_max += [DCmx]
        DCBias_min += [DCmn]
        figures+=[test.plotPower()]
        Tavg, Tmx, Tmn = test.temperatureSPC()
        T_avg += [Tavg]
        T_max += [Tmx]
        T_min += [Tmn]
        figures+=[test.plotTemp()]

for i in figures:
    i.show()
    
    
plt.plot(xdata,DCBias_avg,xdata,DCBias_max,xdata,DCBias_min)
plt.xticks(rotation=90)
plt.show()




    