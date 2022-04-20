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
date_today = today.strftime('%y-%m-%d')#grabbing today's date
time_now = today.strftime('_%H_%M_%S')#grabbing current time, hours and minutes
path_parent = os.path.dirname(os.getcwd()) + "\\export"
if os.path.isdir(path_parent) == False:
    os.mkdir(path_parent)
#print(path_parent)
path_export = path_parent + "\\" + date_today
path_data = path_export + "\\data"
path_plot = path_export + "\\plot"
file_name = "linear_scan_" + date_today + time_now 
#print(path_export)
try:
    os.mkdir(path_export)
    os.mkdir(path_data)
    os.mkdir(path_plot)
    print('folders created')
except:
    print('')


"""
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
"""
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

v_i = 0.6 #initial voltage
v_f = -0.6
v_points = 61
hold = 0.2 #hold time after each point
#v_range = np.linspace(v_i, v_f, v_points) #one direction
v_range = np.append(np.linspace(v_i, v_f, v_points), np.linspace(v_f, v_i, v_points)) #sweep 

current = [] 
voltage = []
timeLapse = []
absCurrent = []

current.append('I')
current.append('A')
voltage.append('V')
voltage.append('V')
timeLapse.append('time')
timeLapse.append('s')
absCurrent.append('abs(I)')
absCurrent.append('A')

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


absCurrent = current
absCurrent[0] = 0
absCurrent[1] = 0
absCurrent = np.absolute(absCurrent)

absCurrent = absCurrent.tolist()
absCurrent[0] = 'abs(I)'
absCurrent[1] = 'A'
current[0] = 'I'
current[1] = 'A'
    
### export data
data = []
data.append(timeLapse)
data.append(voltage)
data.append(current)

data.append(absCurrent)


data_export = np.array(data)

os.chdir(path_data)
np.savetxt(file_name + ".csv", data_export.T,  delimiter = ", ", fmt = '% s')

### plot data
#plt.plot(timeLapse[1:], np.absolute(current[1:]))
#plt.plot(timeLapse[1:], voltage[1:])
plt.plot(voltage[2:], absCurrent[2:])
#plt.yscale('')
#plt.xscale('')
#plt.xlabel(str(absCurrent[0]))
#plt.ylabel(str(absCurrent[0]))

#moving to plot folder
#export plot here(image processing here)
os.chdir(path_plot)
plt.savefig(file_name + ".jpg")
plt.show()

print('finished after ' + str(int(time.time()-start_time)) + ' s;')
print('end.')
