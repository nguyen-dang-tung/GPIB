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
file_name = "linear_scan_" + date_today + time_now 
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

#reset the device
kl.write('smua.reset()') 
kl.write('smub.reset()') 
kl.write('smua.source.output = smua.OUTPUT_ON')
start_time = time.time()


smux = 'smua' #smua or smub
bias = -0.3  # OFF level in V
level = 0.3 # ON level in V
ton = 0.005 # time On in s
toff = 0.005 # time Off in s
points = 10 # number of pulse

pulse_command = 'PulseVMeasureI( '+smux +',' +str(bias) +',' + str(level) +',' + str(ton) +',' + str(toff) + ',' +  str(points) +')'
print(pulse_command)
kl.write(pulse_command)
data = kl.query("printbuffer(1,smua.nvbuffer1.n, smua.nvbuffer1.reading)")
print(data)
data_export = np.array(data)
print(data_export)

os.chdir(path_data)
np.savetxt(file_name + ".csv", data_export.T,  delimiter = ", ", fmt = '% s')

### plot data

#moving to plot folder

print('finished after ' + str(int(time.time()-start_time)) + ' s;')
print('end.')
