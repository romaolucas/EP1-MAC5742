# encoding=utf8  
import glob
import numpy as np
import matplotlib.pyplot as plt

from parse import *

data = {}

list_of_files = glob.glob('mandelbrot_seq/*.log')
file_times = {}
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
    file_times[file_name] = [d['time'] for  d in data_list]
    import numpy as np
    print("Media dos tempos de {} : {}".format(file_name, np.mean(file_times[file_name])))
    print("Desvio padrao de {} : {}".format(file_name, np.std(file_times[file_name])))
    FI.close()

x = [2**i for i in range(4, 14)] 
for file_name in file_times:
    plt.plot(x, file_times[file_name], label=(file_name.split('/')[1]).split('.')[0])

plt.legend()
plt.xlabel('Tamanho da Entrada')
plt.ylabel('Tempo de Execucao (s)')
plt.savefig('seq.png')
