import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import filedialog as fd
import numpy as np
from datetime import datetime
import pandas as pd

# filetypes = ( ('All files', '*.*'), ('Text files', '*.txt') )
format_string = '%b-%d-%Y %I:%M:%S.%f %p' # Fix datetime stamp
col = ['Power Supply 1 Fwd Power', 'Power Supply 1 DC Bias', 'PC Capman Pressure', 'PC MFC 1 Flow', 'PC MFC 2 Flow', 'PC MFC 3 Flow', 'Power Supply 5 Voltage', 'Power Supply 5 Current', 'Substrate Heater Temperature'] #MFC1 = Ar, MFC2 = N2, MFC3 = O2

# create a function that updates the plot data

def open_file():
    filetypes = (('All files', '*.*'), ('text files', '*.txt'))
    
    filename = fd.askopenfilename(title='Open a file', initialdir= r'C:\Users\lopezb41\OneDrive - imec\Desktop\test', filetypes=filetypes)
    
    return filename


def blank():
    
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ncanvas = FigureCanvasTkAgg(fig, master=root)
    ncanvas.draw()
    ncanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    canvas.get_tk_widget().destroy()

def power():
    
    # nfig = Figure(figsize=(5, 4), dpi=100)
    # nax = fig.add_subplot(111)
    ax.plot(df['Time'], df[col[0]])   
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)    
    
    
def argon():
    
    nfig = Figure(figsize=(5, 4), dpi=100)
    nax = fig.add_subplot(111)
    nax.plot(df['Time'], df[col[3]])   
    ncanvas = FigureCanvasTkAgg(nfig, master=root)
    ncanvas.draw()
    ncanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    canvas.get_tk_widget().destroy()
    
def nitrogen():
    canvas.get_tk_widget().destroy()
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df['Time'], df[col[3]])   
    ncanvas = FigureCanvasTkAgg(fig, master=root)
    ncanvas.draw()
    ncanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    

# create a tkinter window
root = tk.Tk()
# path = fd.askopenfilename( title='Open a file', initialdir='/', filetypes=filetypes)
path = open_file()
df = pd.read_csv(path, skiprows = 3)
df['Time'] = [datetime.strptime(i, format_string) for i in df['Time Stamp']]

# create a figure and add a plot to it
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# create a canvas widget to display the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# create a button to update the plot data
btn_blank = tk.Button(root, text='Restore', command=blank)
btn_power = tk.Button(root, text="Power", command=power)
btn_ar = tk.Button(root, text = 'Argon flow', command=argon)

btn_power.pack()
btn_ar.pack()
btn_blank.pack()


# start the tkinter event loop
tk.mainloop()