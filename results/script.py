import glob
from parse import *

data = {}
data_list = []

list_of_files = glob.glob('mandelbrot_omp/*.log')
for file_name in list_of_files:
	FI = open(file_name, 'r')
	#FO = open(file_name.replace('log', 'out'), 'w') 
	for line in FI:
		r = search('{clock}      task-clock (msec)         #    {cpu} CPUs utilized', line)
		if r:
			data['clock'] = float(r['clock']) 
			data['cpu'] = float(r['cpu'])
		r = search('{time} seconds time elapsed', line)
		if r:
			data['time'] = float(r['time'])
			data_list.append(data)

FI.close()
#FO.close()