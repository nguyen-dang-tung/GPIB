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
print(rm.list_resources())
kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

#initiate
kl.write('smua.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
start_time = time.time()

hold = 0

current = []
voltage = []
timeLapse = []


for i in np.linspace(0.1, 0.5, 5):
    for j in (1, -1):
        #print(j)
        kl.write('smua.source.levelv =' + str(i*j))
        #kl.write('smua.measure.iv(smua.nvbuffer1, sma.nvbuffer2)')
        kl.write('smua.measure.i(smua.nvbuffer1)')
        el_time = time.time() - start_time
        timeLapse.append(el_time)
        #sleep(hold)
        kl.write('smua.measure.v(smua.nvbuffer2)')
        currenti = kl.query_ascii_values("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)")
        voltagei = kl.query_ascii_values("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)")
        current.append(currenti)
        voltage.append(voltagei)

#current = kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1)")
#voltage = kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)")

#print(current)
#kl.write('read_buffer(smua.nvbuffer1)')
#kl.query('trace:data?')
#data = kl.query_ascii_values("trace:data?")
#data = kl.query(":READ?")


kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.buffer.clear()')
kl.write('smua.reset()')
print(current)
print(voltage)

#plt.plot(timeLapse, current)
plt.plot(timeLapse, voltage)
#plt.plot(voltage, current)
plt.show

print('end')