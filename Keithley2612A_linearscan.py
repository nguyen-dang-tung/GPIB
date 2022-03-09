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
hold = 0.1
#v_range = np.linspace(v_i, v_f, v_points) #one direction
v_range = np.append(np.linspace(v_i, v_f, v_points), np.linspace(v_f, v_i, v_points)) #sweep 

current = [] 
voltage = []
timeLapse = []

current.append('I')
voltage.append('V')
timeLapse.append('time')

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
data_export = np.array(data)
np.savetxt("linear_scan.csv", data_export.T,  delimiter = ", ", fmt = '% s')

### plot data
#plt.plot(timeLapse[1:], np.absolute(current[1:]))
#plt.plot(timeLapse[1:], voltage[1:])
#plt.plot(voltage[1:], np.absolute(current[1:]))
#plt.yscale('log')
plt.show()

print('end')
