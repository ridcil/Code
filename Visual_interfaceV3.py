# -*- coding: utf-8 -*-

#to open with terminal and python2.7 ->  change to directory, "chmod a+x Visual_interface.py" to make script exe and then "/imec/other/agt4073/bin/python2.7 ./Visual_interface.py"

"""
Created on Mon Feb 25 11:44:01 2019

@author: jlehmann

This file contains all the code for the visual interface

Update history:
    - V2 (update by Simon Hollevoet)
    Updated the textboxes during the wafer sequence to be more clear
    Added a counter to keep track of the number of points added to a wafer sequence
    Update bode amplitude to autoscale with each new measurement
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
#Make sure the right version of Functions is loaded here!
import FunctionsV3 as f #second file containing all the functions needed
import sys
from tkinter import simpledialog

from pathlib import Path


#To plot the graph, import:

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import matplotlib.animation as animation


###############################################################################
###############################################################################
###############################################################################

#dictionnary to associate the type of measurement with the correct keysight abbreviation

dictionnary_meas_var =	{
    "Cp - D": "CPD",
    "Cp - Q": "CPQ",
    "Cp - G": "CPG",
    "Cp - Rp":"CPRP",
    "Cs - D":"CSD",
    "Cs - Q":"CSQ",  
    "Cs - Rs":"CSRS",  
    "Lp - D":"LPD",  
    "Lp - Q":"LPQ",  
    "Lp - G":"LPG",
    "Lp - Rp":"LPRP",
    "Ls - D":"LSD",
    "Ls - Q":"LSQ",
    "Ls - Rs":"LSRS",
    "R - X":"RX",  
    "|Z|-Theta deg":"ZTD",
    "|Z|-Theta rad":"ZTR",
    "G - B":"GB",
    "|Y|-Theta_d":"YTD",
    "|Y|-Theta_r":"YTR",
    "Vdc - Idc":"VDID" 
}

###############################################################################
###############################################################################
###############################################################################
#As recommended, the interface code is placed inside a class. The main code is located at the end of the .py file.

class App():

#In the init function, we define all the visual aspects that need to be taken care of on the start-up

    def __init__(self, master):
        try:
            self.measurement=f.Meas() #create a meas instance (see functions.py file)

        except: #if keysight or chiller not connected
            messagebox.showinfo("Error", "It looks like one of the instruments (Keysight, ATT chiller) is disconnected or not in remote mode. The program will shut down.")
            master.destroy()
            sys.exit()

        #define the main frame

        self.frame = tk.Frame(master,borderwidth=2, relief='groove')
        self.frame.lift()
        self.frame.grid()
        
        #Measurement configuration panel
        
        self.frameMeas=tk.Frame(self.frame,relief='raised',bd = 1)
        self.frameMeas.grid(row=1,column=0,rowspan=2,padx=(5, 5),pady=(5, 5),sticky='news')
                 
        self.label_freq=tk.Label(self.frameMeas, text="Measurement config").grid(row=0,column=0,columnspan=2)

        self.label = tk.Label(self.frameMeas, text="AC level (mV rms)").grid(row=3, column=0,columnspan=2)      
        self.AClevel = tk.Scale(self.frameMeas, from_=5, to=100, resolution=5, orient=tk.HORIZONTAL)
        self.AClevel.grid(row=4, column=0,columnspan=2,padx=(5, 5),pady=(0, 5),sticky='ew')
     
        self.label = tk.Label(self.frameMeas, text="Integration Time").grid(row=1, column=1,columnspan=1)     
        self.Integrationtime=Combobox(self.frameMeas, values=["Short", "Medium", "Long"],width=17)
        self.Integrationtime.current(0)
        self.Integrationtime.grid(row=2, column=1,columnspan=1,padx=(5, 5),pady=(5, 5), sticky='s')

        self.label = tk.Label(self.frameMeas, text="Variables").grid(row=1, column=0,columnspan=1)     
        self.Meas_type=Combobox(self.frameMeas, values=["Cp - D","Cp - Q","Cp - G","Cp - Rp","Cs - D","Cs - Q","Cs - Rs","Lp - D","Lp - Q","Lp - G","Lp - Rp","Ls - D","Ls - Q","Ls - Rs","R - X","|Z|-Theta deg","|Z|-Theta rad","G - B","|Y|-Theta_d","|Y|-Theta_r","Vdc - Idc"],width=17)
        self.Meas_type.current(15)  
        self.Meas_type.grid(row=2, column=0,columnspan=1,padx=(5, 5),pady=(5, 5))

        self.button_init = tk.Button(self.frameMeas, text="Set Corrections", width=15, command=self.cmd_init_window)
        self.button_init.grid(row=8, column=0,columnspan=2,padx=(5, 5),pady=(5, 5), sticky='nesw')

        self.var_light = tk.IntVar()
        self.c_light = tk.Checkbutton(self.frameMeas, text="Light On/Off (auto test)", variable=self.var_light)
        self.c_light.grid(row=5, column=0,columnspan=1,padx=(5, 5),pady=(10, 5))

        self.var_auto = tk.IntVar()
        self.c_auto = tk.Checkbutton(self.frameMeas, text="Automatic test", variable=self.var_auto)
        self.c_auto.grid(row=5, column=1,columnspan=1,padx=(5, 5),pady=(10, 5),sticky='ew')

        self.button_path = tk.Button(self.frameMeas, text="Change Path", width=10,command=self.cmd_path)
        self.button_path.grid(row=6, column=0,columnspan=1,padx=5,pady=5,sticky='ew')     

#mypath = Path().absolute()
#print(mypath)
        self.path_var=""
        self.Path=tk.Entry(self.frameMeas,state='disabled')
        self.Path.grid(row=7, column=0,columnspan=2,padx=(5, 5),pady=(5, 5),sticky='ew')
        
        self.Path.configure(state='normal')
        self.Path.insert(0,str(Path().absolute())+'\\') #inserts new value assigned by 2nd parameter
        self.Path.configure(state='disabled')  
         #global variable containing the path
        
        self.correctionstate=0
        self.Radiobutton=tk.Radiobutton(self.frameMeas, text="Open and short correction",value=1,indicatoron=False,command = self.corr_state)
        self.Radiobutton.grid(row=9, column=0,columnspan=2,padx=(5, 5),pady=(5, 5),sticky='nesw')

        self.button_path = tk.Button(self.frameMeas, text="Wafer Sequence", width=15,command=self.wafer_seq)
        self.button_path.grid(row=10, column=0,columnspan=1,padx=(5, 5),pady=(10, 5),sticky='nesw')     

        self.button_start = tk.Button(self.frameMeas, text="Start Measurement", height = 5, command=self.cmd_measurement)
        self.button_start.grid(row=12, column=0,columnspan=2,padx=(5, 5),pady=(5, 5),sticky='nsew')
        
        #Start meas button

        #self.button_start = tk.Button(self.frame, text="Start Measurement", width=15, command=self.cmd_measurement)
        #self.button_start.grid(row=3, column=0,columnspan=1,padx=(5, 5),pady=(5, 5),sticky='nsew')
     
        #Frequency panel
        
        self.framefreq=tk.Frame(self.frame,relief='raised',bd = 1)
        self.framefreq.grid(row=0,column=0,padx=(5, 5),pady=(5, 5),sticky='nesw')
        
        self.label_freq=tk.Label(self.framefreq, text="Frequency").grid(row=0,column=1,columnspan=2)
              
        self.label = tk.Label(self.framefreq, text="Start [Hz]").grid(row=1, column=1,sticky=tk.W,columnspan=1)
        self.startfreqvar = tk.StringVar(master, value='0')      
        self.startfreq=tk.Entry(self.framefreq, textvariable=self.startfreqvar)
        self.startfreq.grid(row=2, column=1,columnspan=1,padx=(5, 5),pady=(5, 5),sticky='ew')

        self.label = tk.Label(self.framefreq, text="Stop [Hz]").grid(row=1, column=2,sticky=tk.W,columnspan=1)
        self.stopfreqvar = tk.StringVar(master, value='0')     
        self.stopfreq=tk.Entry(self.framefreq, textvariable=self.stopfreqvar)
        self.stopfreq.grid(row=2, column=2,columnspan=1,padx=(5, 5),pady=(5, 5),sticky='ew')
        
        self.label = tk.Label(self.framefreq, text="Number of points").grid(row=3, column=1,sticky=tk.W,columnspan=1)   
        self.numpointsvar = tk.StringVar(master, value='0')  
        self.numpoints=tk.Entry(self.framefreq, textvariable=self.numpointsvar)
        self.numpoints.grid(row=4, column=1,columnspan=1,padx=(5, 5),pady=(5, 5),sticky='ew')
        
        self.label = tk.Label(self.framefreq, text="Mode").grid(row=3, column=2,sticky=tk.W,columnspan=1)      
        self.loglin=Combobox(self.framefreq, values=["Lin", "Log"])
        self.loglin.current(0)
        self.loglin.grid(row=4, column=2,columnspan=1,padx=(5, 5),pady=(5, 5),sticky='ew')
        
        #DC bias panel
        
        self.frameDCbias=tk.Frame(self.frame,relief='raised',bd = 1)
        self.frameDCbias.grid(row=0,column=1,padx=(5, 5),pady=(5, 5),sticky='nsw')

        self.label_freq=tk.Label(self.frameDCbias, text="DC bias").grid(row=0,column=1,columnspan=3)

        self.label = tk.Label(self.frameDCbias, text="Start [V]").grid(row=1, column=1,sticky=tk.W,columnspan=1)
        self.startDCbiasvar = tk.StringVar(master, value='0')      
        self.startDCbias=tk.Entry(self.frameDCbias, textvariable=self.startDCbiasvar)
        self.startDCbias.grid(row=2, column=1,sticky=tk.W,columnspan=1,padx=(5, 5),pady=(5, 5))

        self.label = tk.Label(self.frameDCbias, text="Stop [V]").grid(row=1, column=2,sticky=tk.W,columnspan=1) 
        self.stopDCbiasvar = tk.StringVar(master, value='0')    
        self.stopDCbias=tk.Entry(self.frameDCbias, textvariable=self.stopDCbiasvar)
        self.stopDCbias.grid(row=2, column=2,sticky=tk.W,columnspan=1)

        self.label = tk.Label(self.frameDCbias, text="Sweep Mode").grid(row=1, column=3,sticky=tk.W,columnspan=1)      
        self.sweepmode=Combobox(self.frameDCbias, values=["Single", "Double"])
        self.sweepmode.current(0)
        self.sweepmode.grid(row=2, column=3,sticky=tk.W,columnspan=1,padx=(5, 5),pady=(5, 5))

        self.label = tk.Label(self.frameDCbias, text="Soaking time [s]").grid(row=3, column=3,sticky=tk.W,columnspan=1)     
        self.soakingtimeDCbiasvar = tk.StringVar(master, value='0') 
        self.soakingtimeDCbias=tk.Entry(self.frameDCbias, textvariable=self.soakingtimeDCbiasvar)
        self.soakingtimeDCbias.grid(row=4, column=3,sticky=tk.W,columnspan=1,padx=(5, 5),pady=(5, 5))
        
        self.label = tk.Label(self.frameDCbias, text="Step size [V]").grid(row=3, column=1,sticky=tk.W,columnspan=1)      
        self.stepsizevar = tk.StringVar(master, value='0') 
        self.stepsize=tk.Entry(self.frameDCbias, textvariable=self.stepsizevar)
        self.stepsize.grid(row=4, column=1,sticky=tk.W,columnspan=1,padx=(5, 5),pady=(5, 5))

        #Temperature control panel
        
        self.frameTemp=tk.Frame(self.frame,relief='raised',bd = 1)
        self.frameTemp.grid(row=0,column=2,padx=(5, 5),pady=(5, 5),sticky='nse')

        self.label=tk.Label(self.frameTemp, text="Temperature control").grid(row=0,column=1,columnspan=3)

        self.label = tk.Label(self.frameTemp, text="Temp [°C]").grid(row=1, column=1,sticky=tk.W,columnspan=1)      
        self.v = tk.StringVar(value='0')
        self.Temp=tk.Entry(self.frameTemp,textvariable=self.v)
        self.Temp.grid(row=2, column=1,sticky=tk.W,columnspan=1,padx=(5, 5),pady=(5, 5))
        
        self.tool3_button = tk.Button(self.frameTemp, width=3,text="->", command=self.cmd_Button)
        self.tool3_button.grid(row=2, column=2,columnspan=1,padx=(5, 5),pady=(5, 5))

        self.tool4_button = tk.Button(self.frameTemp, width=3,text="<-", command=self.cmd_Button2)
        self.tool4_button.grid(row=4, column=2,columnspan=1,padx=(5, 5),pady=(5, 5))
        
        self.label = tk.Label(self.frameTemp, text="Soaking time [s]").grid(row=3, column=1,sticky=tk.W,columnspan=1)
        self.soakingtimetempvar = tk.StringVar(master, value='0')     
        self.soakingtimetemp=tk.Entry(self.frameTemp, textvariable=self.soakingtimetempvar)
        self.soakingtimetemp.grid(row=4, column=1,sticky=tk.W,columnspan=1,padx=(5, 5),pady=(5, 5))


        #Temperature listbox

        self.temp_list = tk.Listbox(self.frameTemp,height=5)
        self.temp_list.grid(row=1,column=3,rowspan=4)

        self.scrollbar = tk.Scrollbar(self.frameTemp)
        self.scrollbar.grid(row=1,column=3,sticky=tk.E+tk.N+tk.S,rowspan=10 )
 
        self.temp_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.temp_list.yview)
               
        #Graph representation

        self.frameGraph=tk.Frame(self.frame,relief='raised',bd = 1)
        self.frameGraph.grid(row=1,column=1,columnspan=2,padx=(5, 5),pady=(5, 5))
                
        style.use("bmh")
        fig = Figure(figsize=(9, 4), dpi=112)
        self.ax0 = fig.add_subplot(131)
        self.ax1 = fig.add_subplot(132)
        self.ax2 = fig.add_subplot(133)
        
        self.ax1.set_xlabel('Frequency[Hz]',fontsize=6)
        self.ax2.set_xlabel('Frequency (Hz)',fontsize=6)

        self.ax0.set_xlabel("Z'",fontsize=6)
        self.ax0.set_ylabel("-Z''",fontsize=6)
        
        for tick in self.ax0.xaxis.get_major_ticks():
           tick.label.set_fontsize(6)
        for tick in self.ax0.yaxis.get_major_ticks():
           tick.label.set_fontsize(6)
        for tick in self.ax1.xaxis.get_major_ticks():
            tick.label.set_fontsize(6)
        for tick in self.ax1.yaxis.get_major_ticks():
           tick.label.set_fontsize(6)
        for tick in self.ax2.xaxis.get_major_ticks():
           tick.label.set_fontsize(6)
        for tick in self.ax2.yaxis.get_major_ticks():
           tick.label.set_fontsize(6)
           
        self.ax1.set_xscale('log')
        self.ax2.set_xscale('log')
            
        fig.tight_layout()
        
        self.canvas=FigureCanvasTkAgg(fig,self.frameGraph)
        self.canvas.get_tk_widget().grid(row=0,column=1)
        self.canvas.draw()

#to plot:df=pd.DataFrame([1,2,3,4]) self.ax1.plot(df) self.canvas.draw()

###############################################################################
#Functions associated to buttons defined previously
    
    def corr_state(self):
    #set open and short correction on or off
    
        if self.correctionstate==0:
            self.measurement.Short_Corr_On()
            self.measurement.Open_Corr_On()  
            self.Radiobutton.select()
            self.correctionstate=1
        else:
            self.measurement.Short_Corr_Off()
            self.measurement.Open_Corr_Off()    
            self.Radiobutton.deselect()
            self.correctionstate=0
    
    def cmd_init_window(self):
        #creation of the window for corrections      

        self.window = tk.Toplevel(self.frame)
        self.window.geometry('300x300')
        
        self.measurement.Measured_var(dictionnary_meas_var[self.Meas_type.get()])        

        self.button_open = tk.Button(self.window, text="Open correction", width=15, command=self.cmd_Open_corr)
        self.button_open.pack(padx=(10, 10),pady=(10,10))#(row=1, column=0,padx=(5, 5),pady=(5, 5))

        self.button_short = tk.Button(self.window, text="Short correction", width=15, command=self.cmd_Short_corr)
        self.button_short.pack(padx=(10, 10),pady=(10,10))#.grid(row=2, column=0,padx=(5, 5),pady=(5, 5))
        
        self.var_load = tk.IntVar()
        self.c_load = tk.Checkbutton(self.window, text="Load correction On/Off", variable=self.var_load)
        self.c_load.pack(padx=(10, 10),pady=(10,10))
                
        self.button_load = tk.Button(self.window, text="Load correction", width=15, command=self.cmd_Load_corr)
        self.button_load.pack(padx=(10, 10),pady=(10,10))#.grid(row=3, column=0,padx=(5, 5),pady=(5, 5))    

        self.button_OK = tk.Button(self.window, text="Ok", width=15, command=self.cmd_Ok)
        self.button_OK.pack(padx=(10, 10),pady=(10,10))#.grid(row=4, column=0,padx=(5, 5),pady=(5, 5))

    def cmd_Open_corr(self):
        #open correction button

        self.measurement.Open_Corr()         

    def cmd_Short_corr(self):
        #short correction button

        self.measurement.Short_Corr()   
        
    def cmd_Load_corr(self):
        #load correction button
        
        if int(self.var_load.get())==1:     
            
            self.measurement.LoadCorr_on(dictionnary_meas_var[self.Meas_type.get()])
            self.measurement.LoadCorr()         
        else:
            messagebox.showinfo("Load correction","Load correction disabled")
      
    def cmd_Ok(self):
        #ok button of the  correction window

        self.window.destroy()  

    def cmd_Button(self):
        #add a temperature to the temperature listbox

        self.temp_list.insert(tk.END, self.v.get())

    def cmd_Button2(self):
        #remove a temperature to the temperature listbox

        self.temp_list.delete(tk.END)

    def cmd_path(self):
        #define the path where measurements should be saved

        self.path_var = filedialog.askdirectory()
        self.path_var=self.path_var+'/'
        self.Path.configure(state='normal')
        self.Path.delete(0, tk.END) #deletes the current value
        self.Path.insert(0, self.path_var) #inserts new value assigned by 2nd parameter
        self.Path.configure(state='disabled')   
        
    def wafer_seq(self):
        
        try:    
            messagebox.showinfo("Wafer Sequence","Defining a wafer sequence. Please switch the prober in remote mode")               
            self.measurement.Pegasus_prober_connection()# try connection with Pegasus
        except:
            #if no connection was possible with the pegasus prober
            messagebox.showinfo("Error", "It looks like the Pegasus prober is not in remote mode. Test cancelled")
            
        name_prog=simpledialog.askstring("Name of the program", "Type the name of the program that you would like to create",parent=self.frame)#if we want to load a test program

        if name_prog is not None:
        
            self.measurement.Wafer_alignement() #launch wafer alignment screen
            messagebox.showinfo("Wafer Sequence","You will now have to perform wafer alignment. Close this window ONCE the alignment is completed.")
            self.measurement.Probe_height() #launch probe height screen 
            messagebox.showinfo("Wafer Sequence","You will now have to perform probe height tuning. Probes should make contact. Close this window ONCE it is completed.")
              
                
            df=self.measurement.Coord_df()
            messagebox.showinfo("Wafer Sequence","Please enter '1.local' mode > '5. manual' and go to your first die. Then resume remote mode by pressing '4. Back' and '1. Remote'. Press 'OK' to close this window ONCE it is completed.") #so that the probes are positioned on the first die
            x0,y0=self.measurement.Getcoord()
            MsgBox = messagebox.askquestion ('Go to next die, this will be point number 2',"Please enter '1.local' mode > '5. manual' and go to your first die. Then resume remote mode by pressing '4. Back' and '1. Remote'. Press 'OK' to close this window ONCE it is completed. Pressing 'YES' saves the current position and allows you to add more points. Pressing 'NO' saves the current position and stops the process.")
            print (x0,y0)
            i=1
            print(i)
            while MsgBox == 'yes':
                
                x,y=self.measurement.Getcoord()
                print (x,y)
                self.measurement.df_add_coord(df,int(x)-int(x0),int(y)-int(y0))
                MsgBox = messagebox.askquestion ('Define next point, this will be point number '+str(i+2),"Please enter '1.local' mode > '5. manual' and go to your first die. Then resume remote mode by pressing '4. Back' and '1. Remote'. Press 'OK' to close this window ONCE it is completed. Pressing 'YES' saves the current position and allows you to add more points. Pressing 'NO' saves the current position and stops the process.")               
                i=i+1
                print(i)
                
            self.measurement.df_save(df,name_prog)
            messagebox.showinfo("Wafer Sequence","Wafer sequence created. The file is saved in "+self.Path.get()) #so that the probes are positioned on the first die
        
        else:
            
            messagebox.showinfo("Wafer Sequence", "Wafer Sequence aborded")                
        
    def cmd_measurement(self):
       
        
        messagebox.showinfo("Info","Measurement is about to start, press OK to continue.")
        
        
        #start the measurement

        self.list_temperatures=list(self.temp_list.get(0, tk.END)) #get temperatures in list format       
        self.measurement.Measured_var(dictionnary_meas_var[self.Meas_type.get()]) #get the measured variable
        self.measurement.Meas_time(self.Integrationtime.get()) #get the integration time
        self.measurement.Signal_level(self.AClevel.get()) #get the AC signal level
        
        #Define the variables of the graph area depending on the measured variables that were choosen:
         
        str_var=str(self.Meas_type.get())        #Get the selected var
        str_var=str_var.split('-')
        self.var1=str_var[0]
        self.var2=str_var[1]        
        self.ax1.set_ylabel(self.var1,fontsize=6)
        self.ax2.set_ylabel(self.var2,fontsize=6)
        
        
        #if the test is automatic
        if int(self.var_auto.get())==1:       
            try:    
                messagebox.showinfo("Automatic test","Automatic test will start. Please switch the prober in remote mode")                
                self.measurement.Pegasus_prober_connection()# try connection with Pegasus
            except:
                #if no connection was possible with the pegasus prober
                messagebox.showinfo("Error", "It looks like the Pegasus prober is not in remote mode. Test cancelled")

            messagebox.showinfo("Select Wafer Sequence", "Please select the wafer sequence file")
            wafer_sequence_path = filedialog.askopenfilename(initialdir = Path().absolute(),title = "Select Wafer Sequence",filetypes = (("txt files","*.txt"),("all files","*.*")))

            if len(wafer_sequence_path)>0: # asksaveasfile return `None` if dialog closed with "cancel".
                
                
                self.measurement.Wafer_alignement() #launch wafer alignment screen
                messagebox.showinfo("Automatic test","If needed, you will now have to perform wafer alignment. Close this window ONCE the alignment is completed.")
                try:
                    self.measurement.Probe_height() #launch probe height screen
                except:
                    messagebox.showinfo("Error", "It looks like the Pegasus prober is not in remote mode. Please switch back to remote mode")
                    self.measurement.Probe_height() #launch probe height screen
                    
                messagebox.showinfo("Automatic test","You will now have to perform probe height tuning. Probes should make contact. Close this window ONCE it is completed.")
                messagebox.showinfo("Automatic test","Please enter '1.local' mode > '5. manual' and go to your first die. Then resume remote mode by pressing '4. Back' and '1. Remote'. Press 'OK' to close this window ONCE it is completed.") #so that the probes are positioned on the first die
                #now we call the measurement function
                try:
                    self.measurement.Meas_auto(self.startfreq.get(),self.stopfreq.get(),self.numpoints.get(),self.loglin.get(),self.startDCbias.get(),self.stopDCbias.get(),self.sweepmode.get(),self.stepsize.get(),self.soakingtimeDCbias.get(),self.list_temperatures,self.soakingtimetemp.get(),self.var_light.get(),self.Path.get(),self.ax0,self.ax1,self.ax2,self.canvas,self.var1,self.var2,wafer_sequence_path)
                except:
                    messagebox.showinfo("Error", "It looks like the Pegasus prober is not in remote mode. Please switch back to remote mode")
                    self.measurement.Meas_auto(self.startfreq.get(),self.stopfreq.get(),self.numpoints.get(),self.loglin.get(),self.startDCbias.get(),self.stopDCbias.get(),self.sweepmode.get(),self.stepsize.get(),self.soakingtimeDCbias.get(),self.list_temperatures,self.soakingtimetemp.get(),self.var_light.get(),self.Path.get(),self.ax0,self.ax1,self.ax2,self.canvas,self.var1,self.var2,wafer_sequence_path)

                messagebox.showinfo("Measurement", "Measurement finished")
            
            else:
                
                messagebox.showinfo("Measurement", "Measurement aborded")

        #if the test is not automatic
        elif int(self.var_auto.get())==0:
                self.measurement.Meas_no_auto(self.startfreq.get(),self.stopfreq.get(),self.numpoints.get(),self.loglin.get(),self.startDCbias.get(),self.stopDCbias.get(),self.sweepmode.get(),self.stepsize.get(),self.soakingtimeDCbias.get(),self.list_temperatures,self.soakingtimetemp.get(),self.Path.get(),self.ax0,self.ax1,self.ax2,self.canvas,self.var1,self.var2)            
                messagebox.showinfo("Measurement", "Measurement finished")

###############################################################################
###############################################################################
###############################################################################        
#Here we define the menu
class Menu:

    def __init__(self, master):
        # create a toplevel menu
        menubar = tk.Menu(master)
#        filemenu = tk.Menu(menubar, tearoff=0)
#        filemenu.add_command(label="Open", command=self.file_open)
#        filemenu.add_command(label="Save", command=self.file_save)
#        menubar.add_cascade(label="File", menu=filemenu)

        menubar.add_command(label="?", command=self.popup_showinfo)
        
        # display the menu
        master.config(menu=menubar)
        
#    def file_save(self):
#        path = filedialog.asksaveasfile(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
#        if path is None: # asksaveasfile return `None` if dialog closed with "cancel".
#            return
#        f = open(path.name,'w')
##        action=list(app.listbox.get(0, tk.END))
##        for t in action:
##            f.write(t + '\n')
#        f.close()      
# 
#    def file_open(self):
#        path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
#        if path is None: # asksaveasfile return `None` if dialog closed with "cancel".
#            return
#        #filename is in f
#        f = open(path, "r")
#        lines = f.read().split('\n')
##        for l in lines:
##            if len(l)>0:
##                app.listbox.insert(tk.END,l) 
                
    def popup_showinfo(self):
        messagebox.showinfo("Credits", "Developed by Jonathan Lehmann (jlehmann@greenfish.eu) from Greenfish SA for imec")

###############################################################################
###############################################################################
###############################################################################        
#Main code
###############################################################################
###############################################################################
###############################################################################

#First we create a tk instance
root = tk.Tk()
root.title("C-V measurement tool Electrochemical Storage Lab")

#Then, we define a custom icon
#root.wm_iconbitmap('/imec/users/lehman48isual_interface/9E.ico')
#root.wm_iconbitmap("C:/Users/jlehmann/Desktop/Jonathan/Python codes/9E.ico")
#root.wm_iconbitmap("C:/Users/lehman48/Desktop/Python code/9E.ico")

#Finally, we launch our interface and the menu
app = App(root)
menu=Menu(root)

#We lift the tk instance above other programms running

root.mainloop()