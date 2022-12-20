from tkinter import *
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from time import sleep
import pandas as pd 
import datetime 
import os 
import time 
import threading 
from matplotlib.animation import FuncAnimation
import pyvisa
import matplotlib.pyplot as plt
from itertools import count


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
file_name = "diode_time_dep_" + date_today + time_now 
#print(path_export)
try:
    os.mkdir(path_export)
    os.mkdir(path_data)
    os.mkdir(path_plot)
    print('folders created')
except:
    print('')

#check the ressource and assign the Keithley
rm = pyvisa.ResourceManager()
#print(rm.list_resources())
kl = rm.open_resource('GPIB0::6::INSTR')
#print(kl.query('*IDN?'))

#initiate
kl.write('smua.reset()')
kl.write('smub.reset()')
kl.write('smua.source.output = smua.OUTPUT_ON')
kl.write('smub.source.output = smub.OUTPUT_ON')


current = []
voltage = []
elapse_time = []

start_time = time.time()

root = Tk()
label = Label(root, text='Animation').grid(column=0, row=0)


canvas = FigureCanvasTkAgg(plt.gcf(),master=root)
canvas.get_tk_widget().grid(column=0,row=1)
plt.gcf().subplots(1)

KeepRecording = BooleanVar()
KeepRecording.set(True)


###Change V_On here
v_ON = -0.5

def animate(i):
    if KeepRecording.get() == True:
        kl.write('smua.source.levelv =' + str(v_ON)) 
        kl.write('smua.measure.i(smua.nvbuffer1)')
        kl.write('smua.measure.v(smua.nvbuffer2)')
        current_i = float(kl.query("printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)"))
        voltage_i = float(kl.query("printbuffer(1, smua.nvbuffer2.n, smua.nvbuffer2.readings)"))
        elapse_time.append(time.time()-start_time)
        current.append(current_i)
        voltage.append(voltage_i)
        ax1 = plt.gca()
        ax1.cla()
        ax1.plot(elapse_time, current)
    
    

#GUI



def get_data():
    tocsv = pd.DataFrame()
    tocsv['current']=current
    tocsv['voltage']=voltage
    tocsv['elapse_time']=elapse_time 
    os.chdir(path_data)
    tocsv.to_csv(file_name + '.csv')
    os.chdir(path_plot)
    plt.savefig(file_name + ".png")
    plt.show()
    kl.write('smua.reset()')
    kl.write('smub.reset()')
    
    

tocsvbutton = Button(root,text='export',command=get_data)

tocsvbutton.grid(column=0,row=2)


def halt_recording():
    print(KeepRecording.get())
    KeepRecording.set(False)
    kl.write('smua.reset()')
    kl.write('smub.reset()')
    
    

stopbutton = Button(root,text='stop',command=halt_recording)

stopbutton.grid(column=1,row=2)


ani = FuncAnimation(plt.gcf(),animate)

mainloop()

    
    
    

