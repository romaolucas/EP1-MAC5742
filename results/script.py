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
#FO.close()