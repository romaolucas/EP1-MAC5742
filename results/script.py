import glob
import numpy as np
import matplotlib.pyplot as plt

from parse import *

data = {}

list_of_files = glob.glob('mandelbrot_omp/*.log')
for file_name in list_of_files:
    FI = open(file_name, 'r')
    data_list = []
    #FO = open(file_name.replace('log', 'out'), 'w') 
    for line in FI:
        r = search('{clock}      task-clock (msec)         #    {cpu} CPUs utilized', line)
        if r:
            data['clock'] = float(r['clock']) 
            data['cpu'] = float(r['cpu'])
        r = search('{time} seconds time elapsed', line)
        if r:
            data['time'] = float(r['time'])
            data_list.append(data.copy())
    FI.close()

data_list = []
FI = open("mandelbrot_seq/full.log")
for line in FI:
    data = {}
    r = search('{clock}      task-clock (msec)         #    {cpu} CPUs utilized', line)
    if r:
        data['clock'] = float(r['clock']) 
        data['cpu'] = float(r['cpu'])
    r = search('{time} seconds time elapsed', line)
    if r:
        data['time'] = float(r['time'])
        data_list.append(data.copy())
y = [d['time'] for d in data_list]
x = [2**i for i in range(4, 14)] 

plt.xlim(16, 8192)
plt.ylim(min(y), max(y))
plt.autoscale(False)
plt.plot(x, y)
plt.show()

#FO.close()
