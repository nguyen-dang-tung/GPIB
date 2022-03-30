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
time_now = today.strftime('_%H_%M')#grabbing current time, hours and minutes
path_parent = os.path.dirname(os.getcwd()) + "\\export"
if os.path.isdir(path_parent) == False:
    os.mkdir(path_parent)
#print(path_parent)
path_export = path_parent + "\\" + date_today
path_data = path_export + "\\data"
path_plot = path_export + "\\plot"
file_name = "linear_scan_" + date_today + time_now 
#print(path_export)
try:
    os.mkdir(path_export)
    os.mkdir(path_data)
    os.mkdir(path_plot)
    print('folders created')
except:
    print('')
    
    
    
rm = pyvisa.ResourceManager()
kl = rm.open_resource('GPIB0::6::INSTR')
kl.write('smua.reset()') 
kl.write('smub.reset()') 
kl.write('smua.source.output = smua.OUTPUT_ON')


amplitude_On = int(); # amplitude of wave function 
amplitude_Off = int()
t_On = 10;
t_Off = 10;
N = 200; #number of pulses 
hold_On = 0;
hold_Off = 0;
current = [] 
timeLapse = []

current.append('I')
timeLapse.append('time')
pulses = np.linspace(1, N)
start_time = time.time()

for pulse in pulses:
    kl.write('smua.source.levelv=' + str(amplitude_On)) 
    for xx in range(t_On):
        kl.write('smua.measure.i(smua.nvbuffer1)')
        el_time = time.time() - start_time
        timeLapse.append(el_time)
        currenti = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
        current.append(currenti)
        sleep(hold_On)
    kl.write('smua.source.levelv=' + str(amplitude_Off))
    for xx in range(t_Off):
        kl.write('smua.measure.i(smua.nvbuffer1)')
        el_time = time.time() - start_time
        timeLapse.append(el_time)
        currenti = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
        current.append(currenti)
        sleep(hold_Off)
        
kl.write('smua.source.output = smua.OUTPUT_OFF')
kl.write('smub.source.output = smub.OUTPUT_OFF')
kl.write('smua.reset()')
kl.write('smub.reset()')
data = []
data.append(timeLapse)
data.append(current)


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


        
                
    
    