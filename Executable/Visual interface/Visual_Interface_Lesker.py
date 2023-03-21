import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import seaborn as sns

matplotlib.use('TkAgg')
format_string = '%b-%d-%Y %I:%M:%S.%f %p' # Fix datetime stamp
filetypes = ( ('All files', '*.*'), ('Text files', '*.txt') )
col = ['Power Supply 1 Fwd Power', 'Power Supply 1 DC Bias', 'PC Capman Pressure', 'PC MFC 1 Flow', 'PC MFC 2 Flow', 'PC MFC 3 Flow', 'Power Supply 5 Voltage', 'Power Supply 5 Current', 'Substrate Heater Temperature'] #MFC1 = Ar, MFC2 = N2, MFC3 = O2
# df = pd.DataFrame()

def update_plot():
    # update the plot data here, e.g. by generating random data
    new_data = df[col[0]]
    line.set_ydata(new_data)
    canvas.draw()

class App(tk.Tk):
    
    def __init__(self):
        
        # Initialize interface
        super().__init__()
    
        # Root window
        self.title('Lesker log')    # Name of window
        self.geometry('1000x500')    # Size of window
        
        frame = tk.Frame(self)
        frame.pack(side=tk.LEFT, padx=50, pady=10)
        
        self.fig = Figure(figsize = (10, 5), dpi = 200) #Create a blank figure for canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # Use matplotlib in tkinter as a widget
        self.canvas.draw()
            
        # btn_openfile = ttk.Button(frame, text='Open file') # Open file button
        # btn_openfile.bind('<Button-1>', self.open) # Execute plot method if left-click
        # btn_openfile.bind('<Return>', self.open) # Execute plot method if 'tab' - 'return/enter'
        # btn_openfile.focus() # to be able to navigate with 'tab'
        
        btn_power = ttk.Button(frame, text="Power", command=power)
        # btn_power.bind('<Button-1>', self.open)
        
        other_btn = ttk.Button(frame, text = 'Holi')
        
        
        # btn_openfile.grid(row = 0, column=0, pady=10)
        btn_power.grid(row=1, column=0, pady=10)
        other_btn.grid(row = 2, column=0, pady=10)
        

        
        # Packing order matters
        # self.btn_openfile.pack(side = tk.LEFT, padx=50, pady=5) # button
        # self.other_btn.pack(side = tk.LEFT, padx=50, pady=5) # button
        
        self.canvas.get_tk_widget().pack(side = tk.RIGHT, padx=10, pady=5) # Plot
        
        path = fd.askopenfilename( title='Open a file', initialdir='/', filetypes=filetypes) # Open file dialog
        df = pd.read_csv(path, skiprows = 3)
        df['Time'] = [datetime.strptime(i, format_string) for i in df['Time Stamp']]
        
        
    # def open(self, event):
        
    #     #Clear screen
    #     self.canvas.get_tk_widget().destroy()
        
    #     # open file
    #     path = fd.askopenfilename( title='Open a file', initialdir='/', filetypes=filetypes) # Open file dialog
    #     df = pd.read_csv(path, skiprows = 3)
    #     df['Time'] = [datetime.strptime(i, format_string) for i in df['Time Stamp']]
    #     df_ = df
    
          
        # fig = Figure(figsize = (6, 4), dpi = 100)
        # ax = fig.add_subplot()
             
        # self.canvas = FigureCanvasTkAgg(fig, master=self)  # Define new canvas for plot
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(side = tk.RIGHT) # Pack
        
        
        # return path
        
        # Make plot
        
        
        # 
        # sns.lineplot(data = df, x = df['Time'], y = 'Power Supply 5 Current', label = 'Current', ax = ax) # Plot
        # ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M")) # X - axis tick format for date
        

        
        
 
    
        # #Clear screen
        # self.canvas.get_tk_widget().destroy()
                
        # # Make plot
        # fig = Figure( dpi = 100)
        # ax = fig.add_subplot()

        # sns.lineplot(data = df, x = 'Time', y = col[0], label = 'Power', ax = ax) # Plot
        # ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M")) # X - axis tick format for date
        
        
        # self.canvas = FigureCanvasTkAgg(fig, master=self)  # Define new canvas for plot
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(side = tk.RIGHT) # Pack
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
