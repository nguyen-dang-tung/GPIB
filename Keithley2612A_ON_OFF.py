# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 16:58:51 2022

@author: Tung
"""

import pyvisa
from time import sleep
import time as time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os as os

#create path to export. Usually the source code is put at src
path_parent = os.path.dirname(os.getcwd())
path_export = path_parent + '\\export'
if os.path.isdir(path_export) == False:
    os.mkdir(path_export)
print(path_export)
os.chdir(path_export)
	
#check the ressource and assign the Keithley
rm = pyvisa.ResourceManager()
print(rm.list_resources())
kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

#initiate
kl.write('smua.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
kl.write('smub.source.output = smub.OUTPUT_ON')

#temp = 0

#define parameter of scan

hold = 0.1 #hold time for each measurement OECT might require hold time = 100 ms

vd = 0.3

vg_ON = 0.2 # 
points_ON = 5 #
vg_OFF = -0.6 # 
points_OFF = 5 #

cycles = 2000 #

data = []

el_time = []
current_d = []
voltage_d = []
current_g = []
voltage_g = []

el_time.append('Time (s)')
current_d.append('Id (A)' )
voltage_d.append('Vd (V)' )
current_g.append('Ig (A)' )
voltage_g.append('Vg (V)' )

kl.write('smua.source.levelv =' + str(vdi))    
start_time = time.time()
for i in range(cycles):
    kl.write('smub.source.levelv =' + str(vg_ON))
	for j in range(points_ON):
		#here we measure
		kl.write('smua.measure.i(smua.nvbuffer1)')
		kl.write('smua.measure.v(smua.nvbuffer2)')
		kl.write('smub.measure.i(smub.nvbuffer1)')
		kl.write('smub.measure.v(smub.nvbuffer2)')
		#here we save data        
		el_time.append(time.time() - start_time)
		current_d.append(float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")))
		voltage_d.append(float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)")))
		current_g.append(float(kl.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)")))
		voltage_g.append(float(kl.query("printbuffer(1, smub.nvbuffer2.n, smub.nvbuffer2.readings)")))
	kl.write('smub.source.levelv =' + str(vg_ON))
		for k in range(point_OFF):
		#here we measure
		kl.write('smua.measure.i(smua.nvbuffer1)')
		kl.write('smua.measure.v(smua.nvbuffer2)')
		kl.write('smub.measure.i(smub.nvbuffer1)')
		kl.write('smub.measure.v(smub.nvbuffer2)')
		#here we save data        
		el_time.append(time.time() - start_time)
		current_d.append(float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")))
		voltage_d.append(float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)")))
		current_g.append(float(kl.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)")))
		voltage_g.append(float(kl.query("printbuffer(1, smub.nvbuffer2.n, smub.nvbuffer2.readings)")))

data.append(el_time)			
data.append(voltage_d)
data.append(current_d)
data.append(voltage_g)
data.append(current_g)

plt.plot(el_time[1:], current_d[1:])
plt.show()

kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.buffer.clear()')
kl.write('smua.reset()')
kl.write('smub.reset()')

data_export = np.array(data)
np.savetxt("transfer.csv", data_export.T,  delimiter = ", ", fmt = '% s')

print('finished after ' + str(int(time.time()-start_time) + ' s;')
print('end.')
