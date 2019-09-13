'''
Script for plotting output from DFRobot electrical conductivity meter.
Adapted from https://highvoltages.co/project/arduino/arduino-real-time-plotting-with-python/
'''

import serial
import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_var(value,value_last,i,dt,ax=None):
    if ax == None:
        ax = plt.gca()
    if i >= dt:
        ax.plot(i, value, 'bo-')
    if i >= 2*dt:
        ax.plot([i-dt,i],[value_last, value],'b-')
    if i < 30:
        plt.xlim([0,30])
    else:
        plt.xlim([0,i])
    plt.xlabel('time [s]')
    plt.tight_layout()

def make_plot(var='Sp'):

    baud_rate = 115200
    port = '/dev/cu.usbmodem1411'

    ser = serial.Serial(port,baud_rate)
    ser.close()
    ser.open()

    i=0
    dt = 0.5

    x=list()
    y=list()
    value_Sp_last = np.nan
    value_T_last = np.nan
    value_EC_last = np.nan

    plt.ion()
    fig=plt.figure()

    if var=='all':
        ax1 = plt.subplot(311)
        ax2 = plt.subplot(312)
        ax3 = plt.subplot(313)

    while True:

        data = ser.readline()
        print(data)
        print(type(data))

        try:
            idx = data.index(b'Sp:')
            val_str = data[idx+3:idx+7]
            value_Sp = float(val_str)
        except:
            value_Sp = np.nan

        try:
            idx = data.index(b'temp:')
            val_str = data[idx+5:idx+9]
            value_T = float(val_str)
        except:
            value_T = np.nan

        try:
            idx = data.index(b'EC:')
            val_str = data[idx+3:idx+8]
            value_EC = float(val_str)
        except:
            value_EC = np.nan

        if var == 'Sp':
            plot_var(value_Sp,value_Sp_last,i,dt)
            plt.title('practical salinity')
        elif var == 'T':
            plot_var(value_T,value_T_last,i,dt)
            plt.title('temperature [degrees C]')
        elif var == 'EC':
            plot_var(value_EC,value_EC_last,i,dt)
            plt.title('conductivity [mS/cm]')
        elif var == 'all':
            plt.subplot(311)
            plot_var(value_T,value_T_last,i,dt,ax1)
            plt.title('temperature [degrees C]')
            plt.subplot(312)
            plot_var(value_EC,value_EC_last,i,dt,ax2)
            plt.title('conductivity [mS/cm]')
            plt.subplot(313)
            plot_var(value_Sp,value_Sp_last,i,dt,ax3)
            plt.title('practical salinity')

        i += dt
        value_Sp_last = value_Sp
        value_T_last = value_T
        value_EC_last = value_EC

        plt.show()
        plt.pause(dt)

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    make_plot(*sys.argv[1:])
