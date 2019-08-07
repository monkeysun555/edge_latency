import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

type_names = ['native', 'container']
cpu_usages = ['p0', 'p8']
new_palette = ['#1f77b4',  '#ff7f0e',  '#2ca02c',
                  '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f',
                  '#bcbd22', '#17becf']
patterns = [ "/" , "|" , "\\"  , "-" , "+" , "x", "o", "O", ".", "*" ]


FLANNEL = [18.473, 7.262, 11.333, 8.682]
IPVLAN = [13.116, 3.144, 6.676, 3.467]
SRIOV = [12.296, 2.077, 6.643, 2.338]


def compare_n_c():
	barWidth = 0.35
	r1 = [2*x +0.1 for x in range(len(FLANNEL))]
	r2 = [x + 1.3*barWidth for x in r1]
	r3 = [x + 2.6*barWidth for x in r1]
	# r4 = [x + 4.3*barWidth for x in r1]

	p = plt.figure(figsize=(10, 8))
	# plt.bar(r1, equal_heights, color='none', width=barWidth, edgecolor=new_palette[0], hatch=patterns[0]*10, linewidth=1.0, zorder = 0, label='Equal Allocation')
	# plt.bar(r1, equal_heights, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r1, FLANNEL, color='none', width=barWidth, edgecolor=new_palette[0], hatch=patterns[0]*4, linewidth=1.0, zorder = 0, label='Flannel')
	plt.bar(r1, FLANNEL, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r2, IPVLAN, color='none', width=barWidth, edgecolor=new_palette[1], hatch=patterns[1]*4, linewidth=1.0, zorder = 0, label='IPVLAN')
	plt.bar(r2, IPVLAN, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r3, SRIOV, color='none', width=barWidth, edgecolor=new_palette[2], hatch=patterns[2]*4, linewidth=1.0, zorder = 0, label='SRIOV')
	plt.bar(r3, SRIOV, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	# plt.bar(r4, c_ingress, color='none', width=barWidth, edgecolor=new_palette[3], hatch=patterns[2]*4, linewidth=1.0, zorder = 0)
	# plt.bar(r4, c_ingress, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	# horizontal_x = [0., r4[-1] + 1.5*barWidth]
	# horizontal_y = [upper_bound for x in horizontal_x]
	# plt.plot(horizontal_x, horizontal_y, '-', color = 'k', linewidth=3, label='Upperbound',zorder = 2)

	# plt.xlabel('CPU Usage', fontweight='bold', fontsize=22)
	plt.xticks([1.7, 5.7], ['Ingress           Egress\nServer', 'Ingress          Engress\nClient'], fontsize=22, fontweight='bold')

	plt.yticks([0, 5, 10, 15, 20], fontsize=22)
	plt.ylabel('Processing Latency (us)', fontweight='bold', fontsize=22)
	plt.axis([0, r3[-1] + 1.3*barWidth, 0, 20])

	plt.legend(ncol=1, fontsize = 24, columnspacing=1, loc='upper right')
	p.show()
	raw_input()
	plt.savefig('k8scomp.eps', format='eps', dpi=1000, figsize=(10, 8))
	return p

def main():
	compare_n_c()


if __name__ == '__main__':
	main()