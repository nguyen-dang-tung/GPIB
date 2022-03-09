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

print(rm.list_resources())


kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

kl.write('smua.reset()')
kl.write('smub.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
start_time = time.time()

v_i = -0.5 
v_f = 0.5
v_points = 100

#v_range = np.linspace(v_i, v_f, v_points)
v_range = np.append(np.linspace(v_i, v_f, v_points), np.linspace(v_f, v_i, v_points))

current = []
voltage = []
timeLapse = []

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

kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.reset()')
kl.write('smub.reset()')

#print(current)
#print(voltage)
#export data
#set data
data = []
data.append(elapse_time)
data.append(voltage)
data.append(current)
data_export = np.array(data)
np.savetxt("linear_scan.csv", data_export.T,  delimiter = ", ", fmt = '% s')

#plot data
#plt.plot(timeLapse, current)
#plt.plot(timeLapse, voltage)
plt.plot(voltage, current)
plt.show()

print('end')
