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

	server_usages = []
	client_usages = []
	for file in files:
		file_path = files_dir + file
		if "server" in file and not 'cpu' in file:
			with open(file_path, 'rb') as f:
				for line in f:
					parse = line.strip('\n')
					parse = line.split()
					# print(len(parse), parse)
					if not len(parse) == 5:
						continue
					if parse[1] == 'sum':
						server_usages.append(float(parse[2]))
		elif 'client' in file and not 'cpu' in file:
			with open(file_path, 'rb') as f:
				for line in f:
					parse = line.strip('\n')
					parse = line.split()
					# print(len(parse), parse)
					if not len(parse) == 8:
						continue
					if parse[1] == 'sum':
						client_usages.append(float(parse[2]))
	print("Server average CPU usage: " + str(np.round(np.mean(server_usages),2)) + "%")
	print("Client average CPU usage: " + str(np.round(np.mean(client_usages),2)) + "%")

	return 

def main():
	process_recording()

if __name__ == '__main__':
	main()