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

#function sweep
def sweep(i, f, points):
    return np.append(np.linspace(i,f,points), np.linspace(f,i,points))
#check the ressource and assign the Keithley
rm = pyvisa.ResourceManager()
print(rm.list_resources())
kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

#initiate
kl.write('smua.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
kl.write('smub.source.output = smub.OUTPUT_ON')
#start_time = time.time()
#temp = 0

#define parameter of scan

hold = 0.1 #hold time for each measurement OECT might require hold time = 100 ms
vg_i = -0.5 # initial Vd 
vg_f = 0.5 # final Vd
vg_points = 10 # number of point
sweep = sweep(vg_i, vg_f, vg_points)

vd_i = 0.1
vd_f = 0.2
vd_points = 2
vd_range = np.linspace(vd_i, vd_f, vd_points)

#creat a sweep list

#ascending = np.linspace(vg_i, vg_f, vd_points)
#descending = np.linspace(vd_f, vd_i, vd_points)


data = []
enum = 1

for vdi in vd_range:

    current_d = []
    voltage_d = []
    current_g = []
    voltage_g = []
    
    current_d.append('Id (' + str(enum) +')' )
    voltage_d.append('Vd (' + str(enum) +')' )
    current_g.append('Ig (' + str(enum) +')' )
    voltage_g.append('Vg (' + str(enum) +')' )
    enum = enum + 1
    print('Vd =' + str(vdi))
    for vgi in sweep:
        kl.write('smub.source.levelv =' + str(vgi))
        kl.write('smua.source.levelv =' + str(vdi))
        #here we measure
        kl.write('smua.measure.i(smua.nvbuffer1)')
        kl.write('smua.measure.v(smua.nvbuffer2)')
        kl.write('smub.measure.i(smub.nvbuffer1)')
        kl.write('smub.measure.v(smub.nvbuffer2)')
        #here we save data        
        current_di = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
        voltage_di = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
        current_d.append(current_di)
        voltage_d.append(voltage_di)
        current_gi = float(kl.query("printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)"))
        voltage_gi = float(kl.query("printbuffer(1, smub.nvbuffer2.n, smub.nvbuffer2.readings)"))
        current_g.append(current_gi)
        voltage_g.append(voltage_gi)
        #print(time.time() - temp)
        #temp = time.time()
    
    data.append(voltage_d)
    data.append(current_d)
    data.append(voltage_g)
    data.append(current_g)


kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.buffer.clear()')
kl.write('smua.reset()')

data_export = np.array(data)
np.savetxt("transfer.csv", data_export.T,  delimiter = ", ", fmt = '% s')

print('end')