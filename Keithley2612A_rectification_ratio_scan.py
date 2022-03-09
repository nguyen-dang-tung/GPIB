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

#check the ressource and assign the Keithley
rm = pyvisa.ResourceManager()
print(rm.list_resources()) #list all devices connected
kl = rm.open_resource('GPIB0::6::INSTR') #the Keithley at Quyen's lab is set at GPIB 6
print(kl.query('*IDN?'))

#initiate
kl.write('smua.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
vd_i = 0
vd_f = 0.8
vd_points = 17
vd_range = np.linspace(vd_i, vd_f, vd_points) #set the range of switching

hold = 0 #hold time after each points

current = []
voltage = []
timeLapse = []

current.append('I')
voltage.append('V')
timeLapse.append('time')

start_time = time.time()
for i in vd_range:
    for j in (1, -1):
        #print(j)
        kl.write('smua.source.levelv =' + str(i*j)) #set voltage
        sleep(hold) #for OECT set hold at 0.1s
        kl.write('smua.measure.i(smua.nvbuffer1)')
        kl.write('smua.measure.v(smua.nvbuffer2)')
        el_time = time.time() - start_time #elapsed time
        timeLapse.append(el_time)
        
        currenti = kl.query_ascii_values("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
        voltagei = kl.query_ascii_values("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)")
        current.append(currenti)
        voltage.append(voltagei)

#reset the Keithley       
kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.buffer.clear()')
kl.write('smua.reset()')
kl.write('smub.reset()')

### plot data
#plt.plot(timeLapse[1:], np.absolute(current[1:]))
#plt.plot(timeLapse[1:], voltage[1:])
plt.plot(voltage[1:], np.absolute(current[1:]))
plt.yscale('log')
plt.show()

#exporting data
data = []
data.append(timeLapse)
data.append(voltage)
data.append(current)
data_export = np.array(data)
np.savetxt("diode-rectif.csv", data_export.T,  delimiter = ", ", fmt = '% s')

print('end')
