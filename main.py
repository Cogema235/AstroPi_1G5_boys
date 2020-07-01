'''
This code will measure the vibrations of the international space station, first of all it will take 5000 mesures spaced by 0.02s of the acceleration on 3 axis (x y z),store data in data01.csv and then wait for significatives vibrations/accelarations if a vibration is detected, 200 measures will be taked and stored in data02.cvs and a graph of the acceleration depending on the time (relative, in cs), will be plotted with the "mathplotlib" library. The program will stop runnig after 3 hours and four LED will be on to indicate the experiment is running.

When we will get the data, the measures will be analysed by FFT to get the vibrations frequency specter.
'''

import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from time import time
from sense_hat import SenseHat
from datetime import datetime
from time import sleep
import sys

x=0
y=0
z=0

sense = SenseHat()

totalTime = 3*3600 #define the running time of the program to 3 hours (3*3600 seconds)
startTime = time() #set the start time of the program

dir_path = os.path.dirname(os.path.realpath(__file__))

def decompte(n):
    for i in reversed(range(n+1)):
        sense.show_message(str(i))

def aquisition(nb_mesures, graph, name):

    Time = []
    X = []
    Y = []
    Z = []

    previousTime = time()
    centisecondes = 0
    i = 0

    while i < nb_mesures: #take mesures while the wanted number of measures is not reached

        if time() - previousTime >= 0.02: #take a measure if the last measure was taken since 0.02 seconds or more

            previousTime = time() #set the date of the last measure
            centisecondes += 2 #increment the time variable (2 cs)

            acceleration = sense.get_accelerometer_raw() #get acceleration values on 3 axis

            x = acceleration['x']
            y = acceleration['y']
            z = acceleration['z']

            Time.append(centisecondes) #add the time to the time list
            X.append(x)
            Y.append(y) #add acceleration value to the accelaration lists
            Z.append(z)
            i += 1

    for i in range(len(Time)): #store the acceleration data in the data01.csv file

        row = (Time[i], X[i], Y[i], Z[i])
        writer.writerow(row)

    if graph: #plot a graph if a graph is requested

        plt.grid(True)
        plt.plot(Time, X)
        plt.ylabel('acceleration (g)')
        plt.xlabel('time (cs)')
        title = name + ".pdf"
        plt.savefig(title) #save the graph
        plt.clf()

sense.show_message("By Noa MOULIN, Leo RACLOT and Vincent LAUGIER")
sleep(1)
decompte(5)#contdown on the LED matrix to announce the first phase of the experiment

#trun on the LEDs
sense.set_pixel(4,4,255,0,0)
sense.set_pixel(3,4,0,255,0)
sense.set_pixel(4,3,0,0,255)
sense.set_pixel(3,3,255,0,255)

with open((dir_path + '/data01.csv'), 'w') as f:
    writer = csv.writer(f)
    header = ("time (cs)" , "x_acceleration(g)", "y_acceleration(g)", "z_acceleration(g)")
    writer.writerow(header)

    #aquisition(5000, True, "fond_debut "+ str(datetime.now())) #take 5000 measures of the acceleration on 3 axis spaced by 0.02s
    aquisition(5000, True, "fond_debut_"+ datetime.now().strftime("%d-%m-%Y-%H_%M_%s"))
sense.show_message("starting vibration detection")
sleep(1)
decompte(5)#contdown on the LED matrix to announce the second phase of the experiment

#trun on the LEDs
sense.set_pixel(4,4,255,0,0)
sense.set_pixel(3,4,0,255,0)
sense.set_pixel(4,3,0,0,255)
sense.set_pixel(3,3,255,0,255)

with open((dir_path + '/data02.csv'), 'w') as f:
    writer = csv.writer(f)
    header = ("time (cs)" , "x_acceleration(g)", "y_acceleration(g)", "z_acceleration(g)")
    writer.writerow(header)

    while True: #a while True loop is used to continuously measure the accelartion to detect vibration

        '''Stop the expreriment after 3 hours or if the data file is larger than 30MB'''
        if time() - startTime >= totalTime - 15 or os.path.getsize(dir_path+'/data02.csv') >= 30*10**6:

            #turn off the LEDs to indicate the experiment is finished
            sense.set_pixel(4,4,0,0,0)
            sense.set_pixel(5,4,0,0,0)
            sense.set_pixel(4,5,0,0,0)
            sense.set_pixel(5,5,0,0,0)

            sense.show_message("Experience finished")
            sys.exit() #shutdow the program

        diff = 0.035 #set the acceleration level to detect a vibration

        acceleration = sense.get_accelerometer_raw() #get acceleration values on 3 axis
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        while abs(x) < diff or abs(y) < diff or abs(z) < diff: #the program will stay on this loop unless a significative vibration is detected

            acceleration = sense.get_accelerometer_raw() #get acceleration values on 3 axis
            x = acceleration['x']
            y = acceleration['y']
            z = acceleration['z']

        date = datetime.now().strftime("%d-%m-%Y-%H_%M_%s") #set the name of the graph file (saved in vector pdf)
        aquisition(200, True, date) #take 200 measures and plot a graph named with the date when the vibration is detected
        sense.show_message("Vibration detected")
        sense.set_pixel(4,4,255,0,0)
        sense.set_pixel(3,4,0,255,0)
        sense.set_pixel(4,3,0,0,255)
        sense.set_pixel(3,3,255,0,255)
