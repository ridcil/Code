import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import seaborn as sns

matplotlib.use('TkAgg')


class App(tk.Tk):
     
    def __init__(self):
        # Initialize interface
        super().__init__()
    
        # Root window
        self.title('Lesker log')    # Name of window
        self.geometry('800x500')    # Size of window
        
        self.fig = Figure(figsize = (6, 4), dpi = 100) #Create a blank figure for canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # Use matplotlib in tkinter as a widget
        self.canvas.draw()
            
        self.btn_openfile = ttk.Button(self, text='Open file') # Open file button
        self.btn_openfile.bind('<Button-1>', self.plot) # Execute plot method if left-click
        self.btn_openfile.bind('<Return>', self.plot) # Execute plot method if 'tab' - 'return/enter'
        self.btn_openfile.focus() # to be able to navigate with 'tab'
        
        # Packing order matters
        self.btn_openfile.pack(anchor = tk.N, padx=1, pady=10) # button
        self.canvas.get_tk_widget().pack(anchor = tk.CENTER) # Plot
        
    def plot(self, event):
        
        #Clear screen
        self.canvas.get_tk_widget().destroy()
        
        # open file
        filetypes = ( ('All files', '*.*'), ('Text files', '*.txt') )
        path = fd.askopenfilename( title='Open a file', initialdir='/', filetypes=filetypes) # Open file dialog
        # Make plot
        fig = Figure(figsize = (6, 4), dpi = 100)
        ax = fig.add_subplot()
        df = pd.read_csv(path, skiprows = 3)    
        format_string = '%b-%d-%Y %I:%M:%S.%f %p' # Fix datetime stamp
        df['Time'] = [datetime.strptime(i, format_string) for i in df['Time Stamp']]
        sns.lineplot(data = df, x = df['Time'], y = 'Power Supply 5 Current', label = 'Current', ax = ax) # Plot
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M")) # X - axis tick format for date
        
        
        self.canvas = FigureCanvasTkAgg(fig, master=self)  # Define new canvas for plot
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(anchor = tk.CENTER) # Pack
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
