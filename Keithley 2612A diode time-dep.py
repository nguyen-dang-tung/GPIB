# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:58:51 2022
@author: Tung
"""

import pyvisa
from time import sleep
import time as time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#check the ressource and assign the Keithley
rm = pyvisa.ResourceManager()
print(rm.list_resources())
kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

#initiate
kl.write('smua.reset()')
kl.write('smub.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
#kl.write('smub.source.output = smub.OUTPUT_ON')

#define parameter of scan

hold = 0 #hold time for each measurement OECT might require hold time = 100 ms
v_ON = 0.5 #apply a voltage 
points_before = 100
points_after = 4000

current = []
voltage = []
elapse_time = []

start_time = time.time()
for i in range(points_before)
  #here we measure
  kl.write('smua.measure.i(smua.nvbuffer1)')
  kl.write('smua.measure.v(smua.nvbuffer2)')
  #kl.write('smub.measure.i(smub.nvbuffer1)')
  #kl.write('smub.measure.v(smub.nvbuffer2)')
  
  #here we record
  current_i = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
  voltage_i = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
  elapse_time.append(time.time()- start_time)
  current.append(current_i)
  voltage.append(voltage_i)

#here we apply a voltage
kl.write('smua.source.levelv =' + str(v_ON))  

for i in range(points_after)
  #here we measure
  kl.write('smua.measure.i(smua.nvbuffer1)')
  kl.write('smua.measure.v(smua.nvbuffer2)')
  #here we record
  current_i = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
  voltage_i = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
  elapse_time.append(time.time()- start_time)
  current.append(current_i)
  voltage.append(voltage_i)

#set data
data = []
data.append(elapse_time)
data.append(voltage)
data.append(current)

#reset  
kl.write('smua.source.output = smua.OUTPUT_OFF')
#kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.buffer.clear()')
kl.write('smua.reset()')  

#export data
data_export = np.array(data)
np.savetxt("output.csv", data_export.T,  delimiter = ", ", fmt = '% s')

#plot data
plt.plot(timeLapse, current)
#plt.plot(timeLapse, voltage)
#plt.plot(voltage, current)
plt.show()

print('end')
