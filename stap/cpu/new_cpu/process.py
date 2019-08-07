import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib as mpl


FILES_DIR = "./"

LENS = ['10.', '200.', '1000.', '1400.']
NETWORKS = ['flannel', 'ipvlan', 'sriov']
new_palette = ['#1f77b4',  '#ff7f0e',  '#2ca02c',
                  '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f',
                  '#bcbd22', '#17becf']
patterns = [ "/" , "|" , "\\"  , "-" , "+" , "x", "o", "O", ".", "*" ]

def process_recording():
	files_dir = FILES_DIR
	if not os.path.exists(files_dir):
		print("No corresponding cni.")
		return 
	files = os.listdir(files_dir)
	client_ingress_time = []
	client_egress_time = []
	client_application_time = []
	server_ingress_time = []
	server_egress_time = []
	server_application_time = []
	server_cpus = []
	client_cpus = []
	throughputs = []
	n_packets = []
	for i in range(len(LENS)):
		server_cpu = []
		client_cpu = []
		throughput = []
		n_packet = []
		data_size = float(LENS[i][:-1])
		for j in range(len(NETWORKS)):
			for file in files:
				netdev_recv_time = 0
				ip_recv_time = 0
				tcp_recv_time = 0
				socket_recv_time = 0
				socket_send_time = 0
				tcp_send_time = 0
				ip_send_time = 0
				netdev_send_time = 0
				if "server" in file and LENS[i] in file and NETWORKS[j] in file:
					cpu_usages = []
					file_path = files_dir + file
					with open(file_path, 'rb') as f:
						for line in f:
							parse = line.strip('\n')
							parse = line.split()
							# print(parse)
							# print(len(parse))
							if not len(parse) == 4:
								continue
							if parse[1] == 'sum':
								cpu_usages.append(float(parse[2]))
					server_cpu.append(np.mean(cpu_usages))

				elif "client" in file and LENS[i] in file and NETWORKS[j] in file:
					file_path = files_dir + file
					with open(file_path, 'rb') as f:
						cpu_usages = []
						temp_tp = []
						with open(file_path, 'rb') as f:
							for line in f:
								parse = line.strip('\n')
								parse = line.split()
								# print(parse)
								# print(len(parse))
								if not len(parse) == 7:
									if len(parse) == 4 and parse[0] == 'TCP':
										if float(parse[2]) > 0:
											temp_tp.append(float(parse[2]))
								elif len(parse) == 7:
									assert parse[1] == 'sum'
									cpu_usages.append(float(parse[2]))
					client_cpu.append(np.mean(cpu_usages))
					throughput.append(np.mean(temp_tp)*data_size*8/(1000000000))
					n_packet.append(np.mean(temp_tp)/1000000)

		server_cpus.append(server_cpu)
		client_cpus.append(client_cpu)	
		throughputs.append(throughput)
		n_packets.append(n_packet)
	print(server_cpus)
	print(client_cpus)
	print(throughputs)
	print(n_packets)
	
	# print("Client Application average:", np.mean(client_application_time), len(client_application_time))
	return server_cpus, client_cpus, throughputs, n_packet

def plot_cpus(server_info):
	barWidth = 0.35
	r1 = [2*x +0.1 for x in range(len(server_info))]
	r2 = [x + 1.3*barWidth for x in r1]
	r3 = [x + 2.6*barWidth for x in r1]
	# r4 = [x + 4.3*barWidth for x in r1]

	flannel_cpus = [x[0] for x in server_info]
	ipvlan_cpus = [x[1] for x in server_info]
	sriov_cpus = [x[2] for x in server_info]

	p = plt.figure(figsize=(10, 8))
	# plt.bar(r1, equal_heights, color='none', width=barWidth, edgecolor=new_palette[0], hatch=patterns[0]*10, linewidth=1.0, zorder = 0, label='Equal Allocation')
	# plt.bar(r1, equal_heights, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r1, flannel_cpus, color='none', width=barWidth, edgecolor=new_palette[0], hatch=patterns[0]*4, linewidth=1.0, zorder = 0, label='Flannel')
	plt.bar(r1, flannel_cpus, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r2, ipvlan_cpus, color='none', width=barWidth, edgecolor=new_palette[1], hatch=patterns[1]*4, linewidth=1.0, zorder = 0, label='IPVLAN')
	plt.bar(r2, ipvlan_cpus, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r3, sriov_cpus, color='none', width=barWidth, edgecolor=new_palette[2], hatch=patterns[2]*4, linewidth=1.0, zorder = 0, label='SRIOV')
	plt.bar(r3, sriov_cpus, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	# plt.bar(r4, c_ingress, color='none', width=barWidth, edgecolor=new_palette[3], hatch=patterns[2]*4, linewidth=1.0, zorder = 0)
	# plt.bar(r4, c_ingress, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	# horizontal_x = [0., r4[-1] + 1.5*barWidth]
	# horizontal_y = [upper_bound for x in horizontal_x]
	# plt.plot(horizontal_x, horizontal_y, '-', color = 'k', linewidth=3, label='Upperbound',zorder = 2)

	# plt.xlabel('CPU Usage', fontweight='bold', fontsize=22)
	plt.xticks([r+0.2 for r in r2],['10','200','1000','1400'], fontsize=22, fontweight='bold')
	plt.xlabel('Packet Data Payload (byte)', fontweight='bold', fontsize=22)

	plt.yticks([0, 50, 100], fontsize=22)
	plt.ylabel('CPU Utilization (%)', fontweight='bold', fontsize=22)

	plt.axis([0, r3[-1] + 1.3*barWidth, 0, 120])

	plt.legend(ncol=3, fontsize = 24, columnspacing=1, loc='upper right')
	p.show()
	raw_input()
	plt.savefig('cpu_info.eps', format='eps', dpi=1000, figsize=(10, 8))
	return p

def plot_tp(tp_info):
	barWidth = 0.35
	r1 = [2*x +0.1 for x in range(len(tp_info))]
	r2 = [x + 1.3*barWidth for x in r1]
	r3 = [x + 2.6*barWidth for x in r1]

	flannel_tp = [x[0] for x in tp_info]
	ipvlan_tp = [x[1] for x in tp_info]
	sriov_tp = [x[2] for x in tp_info]

	p = plt.figure(figsize=(10, 8))
	# plt.bar(r1, equal_heights, color='none', width=barWidth, edgecolor=new_palette[0], hatch=patterns[0]*10, linewidth=1.0, zorder = 0, label='Equal Allocation')
	# plt.bar(r1, equal_heights, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r1, flannel_tp, color='none', width=barWidth, edgecolor=new_palette[0], hatch=patterns[0]*4, linewidth=1.0, zorder = 0, label='Flannel')
	plt.bar(r1, flannel_tp, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r2, ipvlan_tp, color='none', width=barWidth, edgecolor=new_palette[1], hatch=patterns[1]*4, linewidth=1.0, zorder = 0, label='IPVLAN')
	plt.bar(r2, ipvlan_tp, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	plt.bar(r3, sriov_tp, color='none', width=barWidth, edgecolor=new_palette[2], hatch=patterns[2]*4, linewidth=1.0, zorder = 0, label='SRIOV')
	plt.bar(r3, sriov_tp, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	# plt.bar(r4, c_ingress, color='none', width=barWidth, edgecolor=new_palette[3], hatch=patterns[2]*4, linewidth=1.0, zorder = 0)
	# plt.bar(r4, c_ingress, color='none', width=barWidth, edgecolor='k', linewidth=1.5, zorder = 1)

	# horizontal_x = [0., r4[-1] + 1.5*barWidth]
	# horizontal_y = [upper_bound for x in horizontal_x]
	# plt.plot(horizontal_x, horizontal_y, '-', color = 'k', linewidth=3, label='Upperbound',zorder = 2)

	# plt.xlabel('CPU Usage', fontweight='bold', fontsize=22)
	plt.xticks([r+0.2 for r in r2],['10','200','1000','1400'], fontsize=22, fontweight='bold')
	plt.xlabel('Packet Data Payload (byte)', fontweight='bold', fontsize=22)

	plt.yticks([0, 2, 4, 6, 8, 10], fontsize=22)
	plt.ylabel('TCP Throughput (Gbps)', fontweight='bold', fontsize=22)
	plt.axis([0, r3[-1] + 1.3*barWidth, 0, 10])

	plt.legend(ncol=1, fontsize = 24, columnspacing=1, loc='upper left')
	p.show()
	raw_input()
	plt.savefig('tp_info.eps', format='eps', dpi=1000, figsize=(10, 8))


def main():
	server_info, client_info, tp_info, n_packets = process_recording()
	# plot_cpus(client_info)
	# plot_tp(tp_info)

if __name__ == '__main__':
	main()