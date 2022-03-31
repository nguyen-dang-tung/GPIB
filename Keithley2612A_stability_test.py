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
file_name = "stability_scan_" + date_today + time_now 
#print(path_export)
try:
    os.mkdir(path_export)
    os.mkdir(path_data)
    os.mkdir(path_plot)
    print('folders created')
except:
    print('')
    
    
    
rm = pyvisa.ResourceManager()
print(rm.list_resources()) #see list of resources, find the GPIB to fit with the 

kl = rm.open_resource('GPIB0::6::INSTR')
print(kl.query('*IDN?'))

kl.write('smua.reset()') 
kl.write('smub.reset()') 
kl.write('smua.source.output = smua.OUTPUT_ON')


amplitude_On = 0.1 # amplitude of wave function 
amplitude_Off = 0
t_On = 50;
t_Off = 50;
N_pulses = 200; #number of pulses 
hold_On = 0;
hold_Off = 0;
voltage = []
current = [] 
timeLapse = []

current.append('I')
voltage.append('V')
timeLapse.append('time')
#pulses = np.linspace(1, N)
start_time = time.time()

for pulse in range(N_pulses):
    #turn device ON
    kl.write('smua.source.levelv=' + str(amplitude_On)) 
    for xx in range(t_On):
        kl.write('smua.measure.i(smua.nvbuffer1)')
        kl.write('smua.measure.v(smua.nvbuffer2)')
        el_time = time.time() - start_time
        timeLapse.append(el_time)
        currenti = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
        voltagei = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
        current.append(currenti)
        voltage.append(voltagei)
        #sleep(hold_On)
    #turn device OFF
    kl.write('smua.source.levelv=' + str(amplitude_Off))
    for xx in range(t_Off):
        kl.write('smua.measure.i(smua.nvbuffer1)')
        kl.write('smua.measure.v(smua.nvbuffer2)')
        el_time = time.time() - start_time
        timeLapse.append(el_time)
        currenti = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
        voltagei = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
        current.append(currenti)
        voltage.append(voltagei)
        #sleep(hold_Off)
        
kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.reset()')
kl.write('smub.reset()')
data = []
data.append(timeLapse)
data.append(voltage)
data.append(current)

absCurrent = current
absCurrent[0] = 0
absCurrent = np.absolute(absCurrent)

absCurrent = absCurrent.tolist()
absCurrent[0] = 'abs(I)'
current[0] = 'I'
data.append(absCurrent)



data_export = np.array(data)

data_export = np.array(data)

os.chdir(path_data)
np.savetxt(file_name + ".csv", data_export.T,  delimiter = ", ", fmt = '% s')

### plot data
plt.plot(timeLapse[1:], np.absolute(current[1:]))
#plt.plot(timeLapse[1:], voltage[1:])
#plt.plot(voltage[1:], absCurrent[1:])
#plt.yscale('log')
#plt.xscale('log')
#plt.xlabel(str(voltage[0]))
#plt.ylabel(str(absCurrent[0]))
plt.xlabel(str(timeLapse[0]))
plt.ylabel(str(current[0]))
#moving to plot folder
#export plot here(image processing here)
os.chdir(path_plot)
plt.savefig(file_name + ".png")
plt.show()

print('finished after ' + str(int(time.time()-start_time)) + ' s;')
print('end.')


        
                
    
    