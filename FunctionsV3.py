
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:22:40 2019

@author: jlehmann
This file contains all functions associated to:
*the communication with the prober, the chiller and the keysight instruments
*the definition of the frequency range, DC range
*the configuration of the measurement
*the measurement

When giving a command to the chiller, it might be useful to read the answer (if there is an answer) so that the order of answers does not get mixed up
For the prober, it seems that this not have the same importance

Update history:
    - V2 (Simon Hollevoet)
    Fixed a bug in the automated measurement process which would make the probes go up with one fine lift at each temperature
"""

import visa as V
import numpy as np
import time
from pyvisa.resources import MessageBasedResource
import pandas as pd
import datetime
import math as m

#%%  
class Meas():

############################################################################################################
#In the first part, we initialise the communication with instruments, we configure them, we prepare the measurement
############################################################################################################

    def __init__(self):
#init is called upon initialisation of an occurence of the Meas class. Here we initialise the connection to the chiller and the keysight
        
        #initiate pyvisa
        self.rm = V.ResourceManager()
        
        #open keysight resource
        self.Keysight_instr = self.rm.open_resource('GPIB0::2::INSTR')#open the keysight 
        self.Keysight_instr.write("*RST;*CLS") #Initialisation and reset message / status:preset???

        #open chiller resource
        self.Att_chiller_instr = self.rm.open_resource('ASRL1::INSTR', resource_pyclass=MessageBasedResource, write_termination='\r\n')

    def Short_Corr(self):
#in order to perform short circuit correction with the Keysight
        self.Keysight_instr.write(":CORR:SHOR") #Does short correction measurement    

    def Short_Corr_On(self):
#to switch short corr on 
        self.Keysight_instr.write(":CORR:SHOR:STATe ON") #Does short correction measurement    

    def Short_Corr_Off(self):
#to switch short corr off
        self.Keysight_instr.write(":CORR:SHOR:STATe OFF") #Does short correction measurement    
 
    def Open_Corr(self):
# in order to perform open circuit correction with the Keysight
        self.Keysight_instr.write(":CORR:OPEN") #Doesd short correction measurement

    def Open_Corr_On(self):
# to switch open correction on
        self.Keysight_instr.write(":CORR:OPEN:STATe ON") #Doesd short correction measurement

    def Open_Corr_Off(self):
# to switch open correction off
        self.Keysight_instr.write(":CORR:OPEN:STATe OFF") #Doesd short correction measurement
         
    def LoadCorr_on(self,value):
#turn load correction on
        
        #step 1: turn load correction on
        self.Keysight_instr.write(":CORR:LOAD:STAT ON")
        
        #step 2: type of load correction   
        self.Keysight_instr.write(":CORR:LOAD:TYPE %s" % value)

    def LoadCorr_off(self):
#turn load correction off
        
        self.Keysight_instr.write(":CORR:LOAD:STAT OFF")   
        
    def LoadCorr(self):
#do load correction on this spot
        
        self.Keysight_instr.write(":CORR:SPOT:LOAD")

    def Meas_time(self,value):
#Configuration of measurement time on the keysight
        if value=="Short":
            self.Keysight_instr.write(":APERture SHORt") #short measurement time
        elif value=="Medium":
            self.Keysight_instr.write(":APERture MEDium") #medium measurement time
        elif value=="Long":
            self.Keysight_instr.write(":APERture LONG") #long measurement time

    def Measured_var(self,value):
        
        self.Keysight_instr.write(":FUNCtion:IMPedance %s" % value)#configure the type of value that we want to measure


    def Signal_level(self,value):
        
        #print ('the value is'+  str(value))
            
        self.Keysight_instr.write(":VOLTage %fE-3" % value) #configuration of the AC level of the measurement signal

    def Pegasus_prober_connection(self):
#If the test is automatic, we need to connect with the Pegasus

        self.Pegasus_instr = self.rm.open_resource('GPIB0::3::INSTR', resource_pyclass=MessageBasedResource, write_termination='\n')       
#        try:
#            print(self.Pegasus_instr.read()) #when entering remote, gives a message that we need to read
#        except:
#            pass
        
        #on peut envisager ici de tester si read = 00INF 000\n pour voir si la communication fonctionne bien?

    def Wafer_alignement(self):
#Before running automatic test, we need to align the wafer

        self.Pegasus_instr.query('VA CV 1') #turn vaccum on
        self.Pegasus_instr.write('LDALN') # run wafer alignement screen -> gives an answer. we will read it in the probe height function

    def Probe_height(self):
#before running automatic test, we need to configure probe height
        try:
            self.Pegasus_instr.read() #here we read first the answer given for the wafer alignement screen
        except:
            pass
        self.Pegasus_instr.write('LDPH') #probe height

#Not working
#    def load_prog(self,prog):
##in case there is a wish to load a program
#        self.Pegasus_instr.write('PPRO %s'% prog) #

    def Getcoord(self):
#return the x and y coordinate of a point
        coord=self.Pegasus_instr.query('PSXY') #here we read first the answer given for the wafer alignement screen
        coord=coord.split(' ')
        coord=coord[1]
        coord=coord.split(',')      
        x=coord[0]
        y=coord[1]
        y=y[:-1]
        
        return x,y
    
    def Coord_df(self):
        #create a dataframe for the coordinates
        df=pd.DataFrame(columns=['x','y'])
        return df
    
    def df_add_coord(self,df,x,y):
        #Add coordinates
        df.loc[len(df)]=[x,y]

    def df_save(self,df,name):
        #Add coordinates
        df.to_csv(name+".txt",index=False,header=False)
        
    def Freq_DC_range(self,startfreq,stopfreq,numpoints,loglin,startDCbias,stopDCbias,sweepmode,stepsize):
#this function creates a list of frequencies and DC voltages based on the inputs
#first, we create the frequency list
        if int(numpoints)>1: 
            if loglin=="Lin":   
                    freq=np.linspace(float(startfreq),float(stopfreq),float(numpoints))                        
                
            elif loglin=="Log":
                freq=np.geomspace(float(startfreq),float(stopfreq),float(numpoints))
            
        else:
            freq=[float(startfreq)]
                   
        myList = ','.join(map(str, freq))	#make a string with my array   
            
#Then we create the DC list
        if float(stepsize)>0:
            DC=np.arange(float(startDCbias),float(stopDCbias),float(stepsize))  
            if sweepmode=="Double": #if sweep mode double 
                #we need to sweep from start to end and from end to start
                DC=np.append(DC,DC[::-1])
        else:
            DC=[startDCbias]
            
        return myList,DC

############################################################################################################
#In the next section, we run the measurements (automatic or not, DC sweep or not, temp sweep or not)
############################################################################################################

#############################
#If the measurements are not automatic

    def Meas_no_auto(self,startfreq,stopfreq,numpoints,loglin,startDCbias,stopDCbias,sweepmode,stepsize,soakingtimeDCbias, temp_list, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2):
 
        #Creation of lists of frequencies and DC voltages
        myList,DC=self.Freq_DC_range(startfreq,stopfreq,numpoints,loglin,startDCbias,stopDCbias,sweepmode,stepsize)        

        self.Measurement(myList,DC,soakingtimeDCbias, temp_list, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2)

#############################
#If the measurements are automatic

    def Meas_auto(self,startfreq,stopfreq,numpoints,loglin,startDCbias,stopDCbias,sweepmode,stepsize,soakingtimeDCbias, temp_list, soakingtimetemp,light_on_off,Path,ax0,ax1,ax2,canvas,var1,var2,wafer_sequence_path):
        #If we are in the case of an automatic measurement
                        
        #Creation of lists of frequencies and DC voltages
        myList,DC=self.Freq_DC_range(startfreq,stopfreq,numpoints,loglin,startDCbias,stopDCbias,sweepmode,stepsize)   

        try:
            self.Pegasus_instr.read() #when entering remote mode, gives a message that we need to read
        except:
            pass
        
        #load the list of positions
        
        data_coord=pd.read_csv(wafer_sequence_path, header = None,names=['x','y'])

        #Pegasus configuration  

        if int(light_on_off)==1: #depends on the value that was chosen by the user
            #switch light on:
            self.Pegasus_instr.query('LI1') #because an answer is given
        else:
            self.Pegasus_instr.query('LI0') #because an answer is given
                    
        self.Pegasus_instr.query('GUP') #gross lift up
        self.Pegasus_instr.query('CUR 100') #fine lift to lower the probe on the first die

        x0,y0=self.Getcoord() #get the x and y position from the first die

        #Measurement sequence
        
        if len(temp_list)==0:  #if no temperature is specified
            
            # the prober should be positioned on the first die
            # test sequence 1st die
            die_numb=1
            time.sleep(3)
            self.Measurement(myList,DC,soakingtimeDCbias, temp_list, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2,die_numb)  # first die measurement
            self.Pegasus_instr.query('CDR 100')  # move probes away from chuck         
            #we now need to iterate over the rows of our data_coord dataframe
            
            for index, row in data_coord.iterrows(): #for each set of coord
                xpos=int(x0)+int(row['x'])
                ypos=int(y0)+int(row['y'])
                #xpos=str(ypos).zfill(6) #fill with zeros if needed
                #ypos=str(ypos).zfill(6) #fill with zeros if needed
                
                self.Pegasus_instr.query('GTXY %(x)s,%(y)s'%{'x': xpos,'y':ypos})
                die_numb=die_numb+1    
                self.Pegasus_instr.query('CUR 100') #lower probe
                time.sleep(3)
                self.Measurement(myList,DC,soakingtimeDCbias, temp_list, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2,die_numb)
                self.Pegasus_instr.query('CDR 100') #move probes away from chuck      
            
        else: #if we need to test the temperature
                        
            for t in temp_list:#for each temperature of the list 

                #temperatures have to be converted from for example 20 to +00200
                if float(t)>0:
                    s="%.1f" % float(t)
                    s=s.zfill(5)
                    s='+'+s
                    s = s.replace(".", "")
                else:
                    s=float(t)
                    s="%.1f" % s
                    s=s.zfill(6)
                    s = s.replace(".", "")	
				
                #set the chiller to the specified temperature
                self.Att_chiller_instr.query("TS=%s" %s) #0250 = 25.0 deg> We need to query and not only write because the chiller answers to commands

                #We wait until the temperature is more or less obtained. For this, we check twice if the temperature (without decimal) set and measured are the same
                
                while True:
                    try:
                        if int((self.Att_chiller_instr.query("TA?"))[-7:-3]) == int(s[0:4]): #we are checking if actual temperature (without decimal) is equal to set temperature (without decimal)
                            break
                    except:
                        time.sleep(0.8)#no need to saturate the chiller with queries
                        pass
                    
                time.sleep(7)       #wait 5 seconds
                
                #try again, to be sure that we have reached a more or less stable value. this is especially needed when we lower the chuck temperature     
                while True:
                    try:
                        if int((self.Att_chiller_instr.query("TA?"))[-7:-3]) == int(s[0:4]): #we are checking if actual temperature (without decimal) is equal to set temperature (without decimal)
                            break
                    except:
                        time.sleep(0.8)#no need to saturate the chiller with queries                        
                        pass                
                    
                time.sleep(int(soakingtimetemp))

                # the prober should be positioned on the first die
                # test sequence 1st die
                die_numb=1 
                time.sleep(3) #for test purpose
                self.Measurement_auto_temp(myList,DC,soakingtimeDCbias, t, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2,die_numb)  # first die measurement
                self.Pegasus_instr.query('CDR 100')  # move probes away from chuck
                
                #we now need to iterate over the rows of our data_coord dataframe
            
                for index, row in data_coord.iterrows(): #for each set of coord
                    xpos=int(x0)+int(row['x'])
                    ypos=int(y0)+int(row['y'])
                    #xpos=str(ypos).zfill(6) #fill with zeros if needed
                    #ypos=str(ypos).zfill(6) #fill with zeros if needed
                    
                    self.Pegasus_instr.query('GTXY %(x)s,%(y)s'%{'x': xpos,'y':ypos})
                    die_numb=die_numb+1    
                    self.Pegasus_instr.query('CUR 100') #lower probe
                    time.sleep(3) #for test purpose
                    self.Measurement_auto_temp(myList,DC,soakingtimeDCbias, t, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2,die_numb)
                    self.Pegasus_instr.query('CDR 100') #move probes away from chuck
                    
                #once we have finished for a temperature, we need to try the next one. Thus, we go back to first die position
                self.Pegasus_instr.query('GTXY %(x)s,%(y)s'%{'x': x0,'y':y0}) 
                
                # We need to lower the probes again before we do the first measurement, otherwise we move the probes up by CDR/CUR 100 with eath temperature
                self.Pegasus_instr.query('CUR 100') #lower probe to be in same position as set by line 230 and used in line 304
                
            
        print(self.Pegasus_instr.query('GDW')) #gross lift down
        print ("test fini")
        self.Pegasus_instr.query("LDM") #end of test
        self.Pegasus_instr.write('ESC') #exit remote mode    
                
#############################
#Measurement itself (except special case see down). We need to sweep frequencies for each DC voltage and each temperature

    def Measurement(self,myList,DC,soakingtimeDCbias, temp_list, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2,die_numb=None):
        #keysight, DC and temperature sweep
        
        self.Keysight_instr.write(":ABOR;:INIT")#System in Idle state then system in Waiting for trigger
        self.Keysight_instr.write("DISP:PAGE LIST") #To allow sweep measurements
        self.Keysight_instr.write(":BIAS:STATe ON") #To allow DC bias

        if len(temp_list)==0:  #if no temperature is specified

        #freq & DC (sweep freq for each voltage)
           
            for dc in DC: #for each DC voltage
                
                print (dc)

                #set the DC bias
                self.Keysight_instr.write(":BIAS:VOLTage %s" % dc) 
                #wait for the soaking DC bias time.
                time.sleep(int(soakingtimeDCbias))

                #load frequencies
                self.Keysight_instr.write("LIST:FREQ  %s"% myList)

                #configure trigger
                self.Keysight_instr.write("*SRE 128")
                self.Keysight_instr.write("STAT:OPER:ENAB 16") #bit 8 pour list sweep On peut lire avec ca: STAT:OPER:COND?
                self.Keysight_instr.write(":TRIG:SOUR BUS")
                self.Keysight_instr.write("TRIG") #run measurement
               
                
                while True:
                    #test if the measurement is finished or not
                    try:
                        if int(self.Keysight_instr.query("*STB?")) == 192:
                            break
                    except:
                        pass
                
                #print(self.Keysight_instr.query_ascii_values("FETCh?"))
                #retrieve values
                y=self.Keysight_instr.query_ascii_values("FETCh?",separator=',')
                #y contains the measured values separated by a comma.

                print("meas voltage:"+self.Keysight_instr.query(":VOLTage?"))
                #create a dataframe containing the values
                n=0
                df=pd.DataFrame(columns=['freq',var1,var2,'DC'])
                listfreq=myList.split(',')
                for frequ in listfreq:
                    df.loc[len(df)] = [frequ,y[n],y[n+1],dc]                                           
                    n=n+4

                #to make the file unique, we use the time
                temps=datetime.datetime.now().time()
                temps_name=str(temps.hour)+'h'+str(temps.minute)+'m'+str(temps.second)+'s'            
                #save and plot the dataframe
                if die_numb!=None: #if automatic test, we add the number of the die to the filename
                    path=Path+'dc=%(second)s die=%(die)s %(temps_name)s.txt'%{'second': dc,'die':die_numb,'temps_name':temps_name} 
                else:
                    path=Path+'dc=%(second)s %(temps_name)s.txt'%{'second': dc,'temps_name':temps_name}            
                #df.to_csv(path,index=False)
                df=df.apply(pd.to_numeric) #convert df to numerical values
                print (df)
                try: #Try to delete existing plot 
                    del ax1.lines[0]
                    del ax2.lines[0]
                    del ax0.lines[0]
                except:
                    pass
                
                Zre=df[var1]*np.cos(df[var2]*m.pi/180)
                Zim=df[var1]*np.sin(df[var2]*m.pi/180)
                Zim=-Zim
                
                axes_limit=max(Zre.max(),Zim.max())
                ax0.set_xlim([0,axes_limit])
                ax0.set_ylim([0,axes_limit])
                ax1.set_ylim([0,max(df[var1])+0.1*max(df[var1])])
                
                ax0.plot(Zre,Zim,color='k')
                ax1.plot(df.freq,df[var1],color='k')              
                ax2.plot(df.freq,df[var2],color='k')
                
                canvas.draw()
    
                df.loc[-2]=[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'','','']
                df.loc[-1]=['Freq',var1,var2,'DC']
                df.index = df.index + 2  # shifting index
                df.sort_index(inplace=True)
                df.to_csv(path,index=False,header=False)
            
########################################################################            

	#freq & DC (sweep freq for each voltage) depending of temperature
        else:
              
            print(temp_list)
            
            for t in temp_list:
                #temperatures have to be converted from for example 20 to +00200
                if float(t)>0:
                    s="%.1f" % float(t)
                    s=s.zfill(5)
                    s='+'+s
                    s = s.replace(".", "")
                else:
                    s= float(t)
                    s="%.1f" % s
                    s=s.zfill(6)
                    s = s.replace(".", "")	
                
                #set the chiller to the specified temperature
                self.Att_chiller_instr.query("TS=%s" %s) #0250 = 25.0 deg> We need to query and not only write because the chiller answers to commands

                #We wait until the temperature is more or less obtain. For this, we check twice if the temperature (without decimal) set and measured are the same
                
                while True:
                    try:
                        if int((self.Att_chiller_instr.query("TA?"))[-7:-3]) == int(s[0:4]): #we are checking if actual temperature (without decimal) is equal to set temperature (without decimal)
                            break
                    except:
                        time.sleep(0.8)#no need to saturate the chiller with queries
                        pass
                    
                time.sleep(7)       #wait 5 seconds
                
                #try again, to be sure that we have reached a more or less stable value. this is especially needed when we lower the chuck temperature     
                while True:
                    try:
                        if int((self.Att_chiller_instr.query("TA?"))[-7:-3]) == int(s[0:4]): #we are checking if actual temperature (without decimal) is equal to set temperature (without decimal)
                            break
                    except:
                        time.sleep(0.8)#no need to saturate the chiller with queries                        
                        pass                
                    
                time.sleep(int(soakingtimetemp))  
                
                for dc in DC:
	                #for each dc bias specified
                    
                    #set the dc bias
                    self.Keysight_instr.write(":BIAS:VOLTage %s" % dc) 
                    #wait for the soaking DC bias time.
                    time.sleep(int(soakingtimeDCbias))

                    # load frequencies
                    self.Keysight_instr.write("LIST:FREQ  %s"% myList)
                  
                    self.Keysight_instr.write("*SRE 128")
                    self.Keysight_instr.write("STAT:OPER:ENAB 16") #bit 8 pour list sweep On peut lire avec ca: STAT:OPER:COND?
                    self.Keysight_instr.write(":TRIG:SOUR BUS")
                    self.Keysight_instr.write("TRIG") #start measurement
                   
                    #wait until measurement is finished
                    while True:
                        try:
                            if int(self.Keysight_instr.query("*STB?")) == 192:
                                break
                        except:
                            pass

                    #retrieve values
                    y=self.Keysight_instr.query_ascii_values("FETCh?",separator=',')
                    #y contains the measured values separated by a comma.	

                    #create a dataframe containing the values                    
                    n=0
                    df=pd.DataFrame(columns=['freq',var1,var2,'DC','Temp'])
                    listfreq=myList.split(',')
                    for frequ in listfreq:
                        df.loc[len(df)] = [frequ,y[n],y[n+1],dc,t]  
                        n=n+4

                    #to make the file unique, we use the time
                    temps=datetime.datetime.now().time()
                    temps_name=str(temps.hour)+'h'+str(temps.minute)+'m'+str(temps.second)+'s'  
                    if die_numb!=None: #if automatic test, we add the number of the die to the filename
                        path=Path+'dc=%(second)s temp=%(third)s die=%(die)s %(temps_name)s.txt'%{ 'second': dc,'third': t,'die':die_numb,'temps_name':temps_name} 
                    else:
                        path=Path+'dc=%(second)s temp=%(third)s %(temps_name)s.txt'%{ 'second': dc,'third': t,'temps_name':temps_name}             
                    df=df.apply(pd.to_numeric) #convert df to numerical values
                    print (df)
                    
                    try: #Try to delete existing plot 
                        del ax1.lines[0]
                        del ax2.lines[0]
                        del ax0.lines[0]
                    except:
                        pass
                    
                    Zre=df[var1]*np.cos(df[var2]*m.pi/180)
                    Zim=df[var1]*np.sin(df[var2]*m.pi/180)
                    Zim=-Zim
                    
                    axes_limit=max(Zre.max(),Zim.max())
                    ax0.set_xlim([0,axes_limit])
                    ax0.set_ylim([0,axes_limit])        
                    ax1.set_ylim([0,max(df[var1])+0.1*max(df[var1])])
                    
                    ax0.plot(Zre,Zim,color='k')
                    ax1.plot(df.freq,df[var1],color='k')              
                    ax2.plot(df.freq,df[var2],color='k')   
                    canvas.draw()
                    
                    df.loc[-2]=[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'','','','']
                    df.loc[-1]=['Freq',var1,var2,'DC','Temp']
                    df.index = df.index + 2  # shifting index
                    df.sort_index(inplace=True)
                    df.to_csv(path,index=False,header=False)


#############################
#Special case of measurement in automatic mode with temperature

    def Measurement_auto_temp(self,myList,DC,soakingtimeDCbias, temp_list, soakingtimetemp,Path,ax0,ax1,ax2,canvas,var1,var2,die_numb=None):
        #keysight, DC and temperature sweep
        
        self.Keysight_instr.write(":ABOR;:INIT")#System in Idle state then system in Waiting for trigger
        self.Keysight_instr.write("DISP:PAGE LIST") #To allow sweep measurements
        self.Keysight_instr.write(":BIAS:STATe ON") #To allow DC bias
                                  
        for dc in DC:
	                #for each dc bias specified
            
            #set the dc bias
            self.Keysight_instr.write(":BIAS:VOLTage %s" % dc) 
            #wait for the soaking DC bias time.
            time.sleep(int(soakingtimeDCbias))

            # load frequencies
            self.Keysight_instr.write("LIST:FREQ  %s"% myList)
          
            self.Keysight_instr.write("*SRE 128")
            self.Keysight_instr.write("STAT:OPER:ENAB 16") #bit 8 pour list sweep On peut lire avec ca: STAT:OPER:COND?
            self.Keysight_instr.write(":TRIG:SOUR BUS")
            self.Keysight_instr.write("TRIG") #start measurement
           
            #wait until measurement is finished
            while True:
                try:
                    if int(self.Keysight_instr.query("*STB?")) == 192:
                        break
                except:
                    pass

            #retrieve values
            y=self.Keysight_instr.query_ascii_values("FETCh?",separator=',')
            #y contains the measured values separated by a comma.	

            #create a dataframe containing the values                    
            n=0
            df=pd.DataFrame(columns=['freq',var1,var2,'DC','Temp'])
            listfreq=myList.split(',')
            for frequ in listfreq:
                df.loc[len(df)] = [frequ,y[n],y[n+1],dc,temp_list]  
                n=n+4

            #to make the file unique, we use the time
            temps=datetime.datetime.now().time()
            temps_name=str(temps.hour)+'h'+str(temps.minute)+'m'+str(temps.second)+'s'  
            if die_numb!=None: #if automatic test, we add the number of the die to the filename
                path=Path+'dc=%(second)s temp=%(third)s die=%(die)s %(temps_name)s.txt'%{ 'second': dc,'third': temp_list,'die':die_numb,'temps_name':temps_name} 
            else:
                path=Path+'dc=%(second)s temp=%(third)s %(temps_name)s.txt'%{ 'second': dc,'third': temp_list,'temps_name':temps_name}             
            df=df.apply(pd.to_numeric) #convert df to numerical values
            print (df)
            
            try: #Try to delete existing plot 
                del ax1.lines[0]
                del ax2.lines[0]
                del ax0.lines[0]
            except:
                pass
            
            Zre=df[var1]*np.cos(df[var2]*m.pi/180)
            Zim=df[var1]*np.sin(df[var2]*m.pi/180)
            Zim=-Zim
            
            axes_limit=max(Zre.max(),Zim.max())
            ax0.set_xlim([0,axes_limit])
            ax0.set_ylim([0,axes_limit])       
            ax1.set_ylim([0,max(df[var1])])
            
            ax0.plot(Zre,Zim,color='k')
            ax1.plot(df.freq,df[var1],color='k')              
            ax2.plot(df.freq,df[var2],color='k')   
            canvas.draw()
            
            df.loc[-2]=[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'','','','']
            df.loc[-1]=['Freq',var1,var2,'DC','Temp']
            df.index = df.index + 2  # shifting index
            df.sort_index(inplace=True)
            df.to_csv(path,index=False,header=False)
            
#%%

#CDW/CUP -> moves chuck to fine down (CDW) or fine up (CUP) position
#ESC -> exit remote mode
#GDW / GUP -> chuck gross down or up
#LDALN -> run wafer alignement screen LDALN 1 ou LDALN 0
#LDM -> move to manual load position (genre fin de test?)
#LDPH -> run probe height screen
#LI0 ou LI1 lamp on / off
#NXT -> enters indexing mode qnd moves to the first die to be probed
#NXF -> exists indexing mode
#VAC -> vacuum control

#inst.write_ascii_values('WLISt:WAVeform:DATA somename,', values, converter='x', separator='$')
#query_ascii_values(message, converter='f', separator=', ', container=<class 'list'>, delay=None)
#values = np.array(inst.query_ascii_values('CURV?'))
#values = inst.query_ascii_values('CURV?', container=numpy.array)
