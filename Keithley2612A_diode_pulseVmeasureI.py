#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:39:49 2022

@author: tung
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
file_name = "PulseVMeasureI" + date_today + time_now 
#print(path_export)
try:
    os.mkdir(path_export)
    os.mkdir(path_data)
    os.mkdir(path_plot)
    print('folders created')
except:
    print('')



#########################Main Code##########################################
rm = pyvisa.ResourceManager()

print(rm.list_resources()) #see list of resources, find the GPIB to fit with the 

kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))
print("test")

#reset the device
kl.write('smua.reset()') 
kl.write('smua.nvbuffer1.clear()')
kl.write('smub.reset()') 
kl.write('smua.source.output = smua.OUTPUT_ON')
start_time = time.time()

#kl.write('smua.nvbuffer1.clear()')
#kl.write('smua.nvbuffer1.appendmode=1')

#kl.write('PulseVMeasureI(smua, .20, 0.5, 1, 0.002, 0.2, 10)')
#kl.write('InitiatePulseTest(1)')
smux = 'smua' #smua or smub
bias = -0.3  # OFF level in V
level = 0.3 # ON level in V
pulse = 0.005
ton = pulse # time On in s
toff = pulse # time Off in s
points = 10 # number of pulse
data =[]
data.append(str(pulse))
pulse_command = 'PulseVMeasureI('+smux +',' +str(bias) +',' + str(level) +',' + str(ton) +',' + str(toff) + ',' +  str(points) +')'
print(pulse_command)
kl.write(pulse_command)
data_1 = kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
print(data_1)
kl.write('smua.nvbuffer1.clear()')

pulse_command_2 = 'PulseVMeasureI('+smux +',' +str(level) +',' + str(bias) +',' + str(ton) +',' + str(toff) + ',' +  str(points) +')'
kl.write(pulse_command_2)
data_2 = kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
print(data_2)
kl.write('smua.nvbuffer1.clear()')

data.append(data_1.strip())
data.append(data_2.strip())
print(data)
data_export = np.array(data)
print(data_export)

os.chdir(path_data)
np.savetxt(file_name + ".csv", data_export.T,  delimiter = ", ", fmt = '% s')

### plot data

#moving to plot folder
kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.reset()')
kl.write('smub.reset()')
print('finished after ' + str(int(time.time()-start_time)) + ' s;')
print('end.')
