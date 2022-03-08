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
kl.write('smua.source.output = smua.OUTPUT_ON')
start_time = time.time()

current = []
voltage = []
timeLapse = []

for i in np.linspace(-0.5, 0.5, 100):
    #print(i)
    kl.write('smua.source.levelv =' + str(i))
    kl.write('smua.measure.iv(smua.nvbuffer1)')
    el_time = time.time() - start_time
    timeLapse.append(el_time)
    kl.write('smua.measure.v(smua.nvbuffer2)')
    currenti = kl.query_ascii_values("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
    voltagei = kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)")
    current.append(currenti)
    voltage.append(voltagei)


#kl.write('read_buffer(smua.nvbuffer1)')
#kl.query('trace:data?')
#data = kl.query_ascii_values("trace:data?")
#data = kl.query(":READ?")


kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.reset()')
#print(current)
#print(voltage)

#plt.plot(timeLapse, current)
#plt.plot(timeLapse, voltage)
plt.plot(voltage, current)
plt.show

print('end')