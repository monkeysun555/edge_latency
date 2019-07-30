import numpy as np
import os
import sys


FILES_DIR = "./"

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
	for file in files:
		file_path = files_dir + file
		netdev_recv_time = 0
		ip_recv_time = 0
		tcp_recv_time = 0
		socket_recv_time = 0
		socket_send_time = 0
		tcp_send_time = 0
		ip_send_time = 0
		netdev_send_time = 0
		if "server" in file:
			with open(file_path, 'rb') as f:
				for line in f:
					parse = line.strip('\n')
					parse = line.split()
					if not len(parse) == 18:
						continue
					if parse[17] == '102.' and parse[13] == 'enp135s0f0,' and parse[10] == 'netdev_recv,':
						netdev_recv_time = int(parse[1])
					# elif parse[17] == '102.' and parse[13] == 'eth1,' and parse[10] == 'ip_recv,':
					# 	ip_recv_time = int(parse[1])
					# elif parse[17] == '82.' and parse[10] == 'tcp_receive,':
					# 	tcp_recv_time = int(parse[1])
					elif parse[17] == '50.' and parse[13] == 'cent_server.out,' and parse[10] == 'socket_recv,':
						socket_recv_time = int(parse[1])
						ingress = socket_recv_time - netdev_recv_time
						if ingress <= 0 or ingress > 300:
							continue
						else:
							server_ingress_time.append(ingress)

					elif parse[17] == '50.' and parse[13] == 'cent_server.out,' and parse[10] == 'socket_send,':
						socket_send_time = int(parse[1])
						if socket_send_time - socket_recv_time > 0 and socket_send_time - socket_recv_time < 100:
							server_application_time.append(socket_send_time - socket_recv_time)
					elif parse[17] == '116.' and parse[13] == 'enp135s0f0,' and parse[10] == 'net_send,':
						netdev_send_time = int(parse[1])
						egress = netdev_send_time - socket_send_time
						if egress <= 0 or egress > 300:
							continue
						else:
							server_egress_time.append(egress)
		else:
			with open(file_path, 'rb') as f:
				for line in f:
					parse = line.strip('\n')
					parse = line.split()
					if not len(parse) == 18:
						continue
					if parse[17] == '102.' and parse[13] == 'enp135s0f0,' and parse[10] == 'netdev_recv,':
						netdev_recv_time = int(parse[1])
					# elif parse[17] == '102.' and parse[13] == 'eth1,' and parse[10] == 'ip_recv,':
					# 	ip_recv_time = int(parse[1])
					# elif parse[17] == '82.' and parse[10] == 'tcp_receive,':
					# 	tcp_recv_time = int(parse[1])
					elif parse[17] == '50.' and parse[13] == 'cent_client.out,' and parse[10] == 'socket_recv,':
						socket_recv_time = int(parse[1])
						ingress = socket_recv_time - netdev_recv_time
						if ingress <= 0 or ingress > 300:
							continue
						else:
							client_ingress_time.append(ingress)

					elif parse[17] == '50.' and parse[13] == 'cent_client.out,' and parse[10] == 'socket_send,':
						socket_send_time = int(parse[1])
						# if socket_send_time - socket_recv_time > 0 and socket_send_time - socket_recv_time < 100:
						# 	client_application_time.append(socket_send_time - socket_recv_time)
					elif parse[17] == '116.' and parse[13] == 'enp135s0f0,' and parse[10] == 'net_send,':
						netdev_send_time = int(parse[1])
						egress = netdev_send_time - socket_send_time
						if egress <= 0 or egress > 300:
							continue
						else:
							client_egress_time.append(egress)
	print("Server Ingress average:", np.mean(server_ingress_time), len(server_ingress_time))
	print("Server Egress average:", np.mean(server_egress_time), len(server_egress_time))
	print("Server Application average:", np.mean(server_application_time), len(server_application_time))
	print("Client Ingress average:", np.mean(client_ingress_time), len(client_ingress_time))
	print("Client Egress average:", np.mean(client_egress_time), len(client_egress_time))
	# print("Client Application average:", np.mean(client_application_time), len(client_application_time))
	return server_ingress_time, server_egress_time, client_ingress_time, client_egress_time

def main():
	process_recording()

if __name__ == '__main__':
	main()