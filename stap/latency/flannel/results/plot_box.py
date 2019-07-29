import numpy as np
import os
import process as ps
import matplotlib.pyplot as plt
import matplotlib as mpl

networks = ['flannel', 'weave']
nodes = ['client', 'server']

def box_show(datas):
	# barWidth = 0.35
	# r = []
	# r1 = [2.5*x +0.1 for x in range(len(datas))]
	# r2 = [x + 1.3*barWidth for x in r1]
	# r3 = [x + 3.0*barWidth for x in r1]
	# r4 = [x + 4.3*barWidth for x in r1]
	# for i in range(len(r1)):
	# 	r.append(r1[i])
	# 	r.append(r2[i])
	# 	r.append(r3[i])
	# 	r.append(r4[i])

	p = plt.figure(figsize=(10, 7))

	# for i in range(len(datas[0])):
	# 	for j in range(len(datas)):
	# 		print(r[i][j], datas[j][i])
	plt.boxplot(datas)

	p.show()
	raw_input()

def loadfile():
	datas = ps.process_recording()

	# print(datas, len(datas[0]))
	return datas

def main():
	datas = loadfile()
	box_show(datas)

if __name__ == '__main__':
	main()