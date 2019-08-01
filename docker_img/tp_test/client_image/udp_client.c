// Client side implementation of UDP client-server model 
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 
  
#define PORT   22222 
#define MAXLINE 3000 
  
// Driver code 
int main(int argc, char *argv[]) {
    if (argc < 4){
        printf("No enough inputs!\n");
        return -1;
    }

    int packet_len = atoi(argv[3]);
    if (packet_len < 0 || packet_len > 3000) {
        return -1;
    }

    int sockfd; 
    char buffer[MAXLINE]; 
    // char *hello = "Hello from client"; 
    struct sockaddr_in     servaddr; 
  
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 
  
    memset(&servaddr, 0, sizeof(servaddr)); 
      
    // Filling server information 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_port = htons(PORT); 
    servaddr.sin_addr.s_addr = INADDR_ANY; 
      
    int n, len; 
    for (int i=0;i<packet_len;i++){
        buffer[i] = 'a';
    }
    while (1) {
        sendto(sockfd, buffer, packet_len, 
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
            sizeof(servaddr)); 
        
        // send(sockfd, buffer, packet_len, 0);
        // send(sockfd, buffer, packet_len, 
        // MSG_CONFIRM); 
        // printf("udp send one\n");
    }

    // printf("Hello message sent.\n"); 
          
    // n = recvfrom(sockfd, (char *)buffer, MAXLINE,  
    //             MSG_WAITALL, (struct sockaddr *) &servaddr, 
    //             &len); 
    // buffer[n] = '\0'; 
    // printf("Server : %s\n", buffer); 
  
    close(sockfd); 
    return 0; 
}