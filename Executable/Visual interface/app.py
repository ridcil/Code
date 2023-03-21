import tkinter as tk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns

col = ['Power Supply 1 Fwd Power', 'Power Supply 1 DC Bias', 'PC Capman Pressure', 'PC MFC 1 Flow', 'PC MFC 2 Flow', 'PC MFC 3 Flow', 'Power Supply 5 Voltage', 'Power Supply 5 Current', 'Substrate Heater Temperature'] #MFC1 = Ar, MFC2 = N2, MFC3 = O2
filetypes = (('All files', '*.*'), ('text files', '*.txt'))
format_string = '%b-%d-%Y %I:%M:%S.%f %p' # Fix datetime stamp

class Application(tk.Frame):

    def open_file(self):
        filename = fd.askopenfilename(title='Open a file', initialdir= r'C:\Users\lopezb41\OneDrive - imec\Desktop\test', filetypes=filetypes)
        df = pd.read_csv(filename, skiprows = 3)
        df['Time'] = [datetime.strptime(i, format_string) for i in df['Time Stamp']]       
        return df
        
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.createWidgets()
    
    def createWidgets(self):
        fig = plt.figure()
        ax = fig.add_subplot()
        
        df = self.open_file()
        
        canvas=FigureCanvasTkAgg(fig,master=root)
        canvas.get_tk_widget().grid(row=0,column=1, rowspan = 10)
        canvas.draw()
        
        self.open_button = tk.Button(master=root, text="Open file", command = self.createWidgets)# lambda: self.power(canvas,ax, df))
        self.dc_button = tk.Button(master=root, text="DC Bias", command=lambda: self.dc_bias(canvas,ax, df))
        self.press_button = tk.Button(master=root, text="Capman Pressure", command=lambda: self.capman(canvas,ax, df))
        self.power_button = tk.Button(master=root, text="Power", command=lambda: self.power(canvas,ax, df))
        self.argon_button = tk.Button(master=root, text="Argon Flow", command=lambda: self.argon(canvas,ax, df))
        self.nitrogen_button = tk.Button(master=root, text="Nitrogen Flow", command=lambda: self.nitrogen(canvas,ax, df))
        self.oxygen_button = tk.Button(master=root, text="Oxygen Flow", command=lambda: self.oxygen(canvas,ax, df))
        self.voltage_button = tk.Button(master=root, text="Voltage", command=lambda: self.voltage(canvas,ax, df))
        self.current_button = tk.Button(master=root, text="Current", command=lambda: self.current(canvas,ax, df))
        self.temp_button = tk.Button(master=root, text="Substrate Temperature", command=lambda: self.temp(canvas,ax, df))

        self.open_button.grid(row = 0)
        self.dc_button.grid(row = 1)
        self.press_button.grid(row = 2)
        self.power_button.grid(row = 3)
        self.argon_button.grid(row = 4)
        self.nitrogen_button.grid(row = 5)
        self.oxygen_button.grid(row = 6)
        self.voltage_button.grid(row = 7)
        self.current_button.grid(row = 8)
        self.temp_button.grid(row = 9)
    
    def power(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[0]) 
        canvas.draw()
        
    def dc_bias(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[1]) 
        canvas.draw()

    def capman(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[2]) 
        canvas.draw()
        
    def argon(self, canvas, ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[3])
        canvas.draw()
        
    def nitrogen(self, canvas, ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[4])
        canvas.draw()
        
    def oxygen(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[5]) 
        canvas.draw()
        
    def voltage(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[6]) 
        canvas.draw()
        
    def current(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[7]) 
        canvas.draw()

    def temp(self,canvas,ax, df):
        ax.clear()
        sns.lineplot(data = df, x = 'Time', y = col[8]) 
        canvas.draw()
    
    
root=tk.Tk()
root.title('Lesker Log')
app=Application(master=root)
app.mainloop()