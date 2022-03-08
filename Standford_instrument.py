# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyvisa 
import sys
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
from time import sleep
import pandas as pd

rm = pyvisa.ResourceManager()

#print(rm.list_resources())

my_instrument = rm.open_resource('GPIB0::10::INSTR')

print(my_instrument.query('*IDN?'))

my_instrument.query('FUNC 1; FUNC?')
#https://www.thinksrs.com/downloads/pdfs/manuals/DS345m.pdf
#Check this website(pg54) for different function outputs. 


my_instrument.query('AMPL 0.01VP; AMPL?')
my_instrument.write('AMPL 0.015VP')


my_instrument.query('FREQ 100; FREQ?')#done = False

'''
for n in 10:
    freq = 10^n
    function = {sqrt, sin, triangle}
    run 10 periods of freq
    '''
'''
while True:    
    function_to_iterate = 1
    while function_to_iterate <= 3:
        frq_iterator = 0;
        while frq_iterator <= 3:#where to change frequency parameters
            frequency = 10**frq_iterator
            my_instrument.write('FREQ ' + str(frequency))
            print(frequency)
            sleep(2)#Pause this function for certain seconds
            frq_iterator = frq_iterator + 1
        function_to_iterate = function_to_iterate + 1
        
'''

while True:
    my_instrument.write('FREQ 10')
    amp_iterator = 0;
    while amp_iterator <= 3:
        amplitude = 0.1*amp_iterator
        my_instrument.write('AMPL' + str(amplitude) +' VP')
        print(amplitude)
        sleep(1)
        amp_iterator = amp_iterator + 1
        


    '''
    for n in range(10):
        ampt = 1*n
        freq = fixed 
        run 10 period
      '''   

