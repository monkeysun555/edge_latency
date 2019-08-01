#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#define BUFFER_SIZE 3000
#define TCP_PORT 22221
#define UDP_PORT 22222
#define on_error(...) { fprintf(stderr, __VA_ARGS__); fflush(stderr); exit(1); }


int tcp_server(){
  // if (argc < 2) on_error("Usage: %s [port]\n", argv[0]);

  // int port = atoi(argv[1]);

  // TCP Connection
  int port = TCP_PORT;
  int server_fd, client_fd, err;
  struct sockaddr_in server, client;
  char buf[BUFFER_SIZE];
  char httpHeader[50] = "HTTP/1.1 200 OK, mark!\r\n\n";
  server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd < 0) on_error("Could not create socket\n");
  // printf("arrive 1\n");
  server.sin_family = AF_INET;
  server.sin_port = htons(port);
  server.sin_addr.s_addr = htonl(INADDR_ANY);
  // printf("arrive 2, after inaddr_any\n");

  int opt_val = 1;
  setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt_val, sizeof opt_val);

  err = bind(server_fd, (struct sockaddr *) &server, sizeof(server));
  if (err < 0) on_error("Could not bind socket\n");

  err = listen(server_fd, 128);
  if (err < 0) on_error("Could not listen on socket\n");

  printf("TCP is listening on: %d\n", port);

  while (1) {
    socklen_t client_len = sizeof(client);
    client_fd = accept(server_fd, (struct sockaddr *) &client, &client_len);

    if (client_fd < 0) on_error("Could not establish new connection\n");

    while (1) {
      int read = recv(client_fd, buf, BUFFER_SIZE, 0);

      if (!read) break; // done reading
      if (read < 0) on_error("Client read failed\n");
      // printf("tcp get one\n");
      // err = send(client_fd, buf, read, 0);
      // err = send(client_fd, httpHeader, sizeof(httpHeader), 0);
      // if (err < 0) on_error("Client write failed\n");
      // close(client_fd);
      // break;
    }
  }
  return 0;
}

int udp_server(){
    int sockfd; 
    char buffer[BUFFER_SIZE]; 
    // char *hello = "Hello from server"; 
    struct sockaddr_in servaddr, cliaddr; 
      
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 
      
    // memset(&servaddr, 0, sizeof(servaddr)); 
    // memset(&cliaddr, 0, sizeof(cliaddr)); 
      
    // Filling server information 
    servaddr.sin_family    = AF_INET; // IPv4 
    servaddr.sin_addr.s_addr = INADDR_ANY; 
    servaddr.sin_port = htons(UDP_PORT); 
      
    // Bind the socket with the server address 
    if ( bind(sockfd, (const struct sockaddr *)&servaddr,  
            sizeof(servaddr)) < 0 ) 
    { 
        perror("bind failed"); 
        exit(EXIT_FAILURE); 
    } 
    printf("UDP is listening on: %d\n", UDP_PORT);
    int len, n; 

    while (1) {
      n = recvfrom(sockfd, (char *)buffer, BUFFER_SIZE,  
                MSG_WAITALL, ( struct sockaddr *) &cliaddr, 
                &len);
      // recvfrom(sockfd,buffer,BUFFER_SIZE,0,(struct sockaddr*)&src_addr,&src_addr_len);
      // int read = recv(sockfd, buffer, BUFFER_SIZE, 0);
      // printf("udp get one\n");
    }

    return 0;
}


int main (int argc, char *argv[]) {
  pthread_t thread_id1, thread_id2;
  pthread_create(&thread_id1, NULL, tcp_server, NULL); 
  pthread_create(&thread_id2, NULL, udp_server, NULL); 

  pthread_join(thread_id1, NULL); 
  pthread_join(thread_id2, NULL); 

  return 0;
}