import csv
import scipy.fftpack
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
import time
import math

chemin01 = '/home/noa/Bureau/AstroPi/1g5boys-LIS/data01.csv'
chemin02 = '/home/noa/Bureau/AstroPi/1g5boys-LIS/data02.csv'

frequencedechantillonage = 50 #Hz

def convert(chemin):

    f = open(chemin)
    csv_f = csv.reader(f)

    
    tableau = [[],[]]

    for line in csv_f:
    	tableau[0].append(float(line[0]))
    	tableau[1].append(float(line[1]))

    f.close

    return tableau

def triSeries(tableau):
	series = []
	temp = []
	iserie = 0

	for i in range(0,len(tableau[0])):

		if i == 0:
			temp.append(tableau[1][i])
		
		elif tableau[0][i] > tableau[0][i-1]:
			temp.append(tableau[1][i])

		else:
			series.append(temp)
			temp = []
			temp.append(tableau[1][i])

	return series 

data01 = convert(chemin01)[1]
data02 = triSeries(convert(chemin02))

def FFT(liste,nom,save):
    
    y = liste
    N = len(y)
    T = 0.02
    x = np.linspace(0.0, N*T, N)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

    for v in range(len(yf)//20): #remove the 0 Hz peak from the spectrum
    	yf[v] = 0

    plt.plot(xf,2.0/N*np.abs(yf[0:N//2]))
    plt.grid(True)
    plt.ylabel('amplitude')
    plt.xlabel('frequency [Hz]')

    if save:
	    title = nom + ".pdf"
	    plt.savefig(title) 
	    plt.clf()

    else:
	    plt.show()

h = 0

for serie in data02:
	h += 1
	FFT(serie,str(h),True)
	time.sleep(0.5)


