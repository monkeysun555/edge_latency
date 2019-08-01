#include <stdio.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <sys/un.h> 
#include <string.h> 
#include <netdb.h> 
#include <netinet/in.h> 
#include <arpa/inet.h> 
#include <stdlib.h> 
  
int main(int argc, char *argv[]) 
{ 
	// Two buffer are for message communication 
	if (argc < 4){
		printf("No enough inputs!\n");
		return -1;
	}

	int packet_len = atoi(argv[3]);
	if (packet_len < 0 || packet_len > 3000) {
		return -1;
	}
	char buffer1[3000], buffer2[3000]; 
	struct sockaddr_in my_addr, my_addr1; 
	int count;
	unsigned long time_in_micros1, time_in_micros2 = 0;
	int client = socket(AF_INET, SOCK_STREAM, 0); 
	struct timeval tv;

	if (client < 0) 
	printf("Error in client creating\n"); 
	else
		printf("Client Created\n"); 
		  
	my_addr.sin_family = AF_INET; 
	// my_addr.sin_addr.s_addr = INADDR_ANY; 
	my_addr.sin_port = htons(22221); 
	  
	// This ip address will change according to the machine 
	my_addr.sin_addr.s_addr = inet_addr(argv[1]); 
	// my_addr.sin_addr.s_addr = inet_addr("10.20.42.96");

	// Explicitly assigning port number 12010 by  
	// binding client with that port  
	my_addr1.sin_family = AF_INET; 
	// my_addr1.sin_addr.s_addr = INADDR_ANY; 
	my_addr1.sin_port = htons(24444); 
	my_addr1.sin_addr.s_addr = inet_addr(argv[2]); 

	// This ip address will change according to the machine 
	// my_addr1.sin_addr.s_addr = inet_addr("10.32.40.213"); 
	if (bind(client, (struct sockaddr*) &my_addr1, sizeof(struct sockaddr_in)) == 0) 
		printf("Binded Correctly\n"); 
	else
		printf("Unable to bind\n"); 
	  
	// socklen_t addr_size = sizeof my_addr; 
	int con = connect(client, (struct sockaddr*) &my_addr, sizeof my_addr); 
   
	if (con == 0) {
		printf("Client Connected\n"); 
		// strcpy(buffer2, "Hello");
		for (int i=0;i<packet_len;i++){
			buffer2[i] = 'a';
		}

		while (1) {
			send(client, buffer2, packet_len, 0);  
			// printf("tcp send one\n");
		}
	}
	else
	{	printf("Error in Connection\n"); 
		printf("Error Code: %d\n", con);
	  }  
   
	return 0; 
} 