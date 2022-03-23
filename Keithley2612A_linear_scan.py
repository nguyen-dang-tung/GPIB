# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 16:58:51 2022

@author: Visitor
"""
import pymeasure as pm
import  pymeasure.instruments.keithley.keithley2400 as Keithley
import pyvisa
from time import sleep
import time as time
import matplotlib.pyplot as plt
import numpy as np
import os as os
import datetime


######################
#Create folders to export files (raw data and plots)
today = datetime.datetime.now()
date_today = today.strftime('%d%m%y')#grabbing today's date
time_now = today.strftime('%H_%M')#grabbing current time, hours and minutes
path_parent = os.getcwd()
#print(path_parent)
path_export = path_parent + "\\" + date_today
#print(path_export)
try:
    os.mkdir(path_export)
    #print('folder created')
except:
    #print('folder was created today, moving on to next step...')

path_linearscan = path_export + "\\linear_scan_" + time_now

if os.path.isdir(path_linearscan) == False:
    os.mkdir(path_linearscan)
    #print('linearscan folder created successfully')
path_data = path_linearscan + '//data'  #creating data directory at current time
if os.path.isdir(path_data) == False:
    os.mkdir(path_data)
    #print('data folder created in current directory')
    
path_plot = path_linearscan + '//plot'#creating data directory at current time
if os.path.isdir(path_plot) == False:
    os.mkdir(path_plot)
    #print('plot folder created in current directory')

os.chdir(path_data)#Moving to the data folder

#########################Main Code##########################################
rm = pyvisa.ResourceManager()

print(rm.list_resources()) #see list of resources, find the GPIB to fit with the 

kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

#reset the device
kl.write('smua.reset()') 
kl.write('smub.reset()') 
kl.write('smua.source.output = smua.OUTPUT_ON')
start_time = time.time()

v_i = -0.5 
v_f = 0.5
v_points = 99
hold = 0.1 #hold time after each point
#v_range = np.linspace(v_i, v_f, v_points) #one direction
v_range = np.append(np.linspace(v_i, v_f, v_points), np.linspace(v_f, v_i, v_points)) #sweep 

current = [] 
voltage = []
timeLapse = []
absCurrent = []

current.append('I')
voltage.append('V')
timeLapse.append('time')
absCurrent.append('abs(I)')

for i in v_range:
    #print(i)
    kl.write('smua.source.levelv =' + str(i))
    kl.write('smua.measure.i(smua.nvbuffer1)')
    kl.write('smua.measure.v(smua.nvbuffer2)')
    el_time = time.time() - start_time
    timeLapse.append(el_time)
    currenti = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
    voltagei = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
    current.append(currenti)
    voltage.append(voltagei)
    sleep(hold)

### turn off the sources and reset the device
kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.reset()')
kl.write('smub.reset()')

#print(current)
#print(voltage)
### export data
data = []
data.append(timeLapse)
data.append(voltage)
data.append(current)
absCurrent.append(np.absolute(current))
data.append(absCurrent)

data_export = np.array(data)
np.savetxt("linear_scan.csv", data_export.T,  delimiter = ", ", fmt = '% s')

### plot data
#plt.plot(timeLapse[1:], np.absolute(current[1:]))
#plt.plot(timeLapse[1:], voltage[1:])
#plt.plot(voltage[1:], np.absolute(current[1:]))
#plt.yscale('log')

#moving to plot folder
#export plot here(image processing here)
os.chdir(path_plot)

plt.show()

print('finished after ' + str(int(time.time()-start_time)) + ' s;')
print('end.')
