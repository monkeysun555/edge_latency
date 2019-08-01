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
	if (argc < 3){
		return -1;
	}
	char buffer1[256], buffer2[100]; 
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
	my_addr.sin_port = htons(11111); 
	  
	// This ip address will change according to the machine 
	my_addr.sin_addr.s_addr = inet_addr(argv[1]); 
	// my_addr.sin_addr.s_addr = inet_addr("10.20.42.96");

	// Explicitly assigning port number 12010 by  
	// binding client with that port  
	my_addr1.sin_family = AF_INET; 
	// my_addr1.sin_addr.s_addr = INADDR_ANY; 
	my_addr1.sin_port = htons(11112); 
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
		strcpy(buffer2, "Hello"); 
		while (1) {
			printf("Enter measure counts!\n");
			scanf("%d", &count); 
			// count = 50;
			if (count == -1) {
				close(con);
				break;
			}

			for (int i=0;i<count;i++){
				gettimeofday(&tv,NULL);
				time_in_micros1 = 1000000 * tv.tv_sec + tv.tv_usec;
				send(client, buffer2, 50, 0);  
				recv(client, buffer1, 256, 0); 
				gettimeofday(&tv,NULL);
				time_in_micros2 += 1000000 * tv.tv_sec + tv.tv_usec - time_in_micros1;
			    usleep(500);
				// printf("Server : %s\n", buffer1); 
			}
			
			printf("Average latency: %d.\n", time_in_micros2/count);
			time_in_micros2 = 0;
		}
	}
	else
	{	printf("Error in Connection\n"); 
		printf("Error Code: %d\n", con);
	  }  
   
	return 0; 
} 