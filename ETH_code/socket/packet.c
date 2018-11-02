/*
 * Copyright(C) 2017 Ruijie Network. All rights reserved.
 */ 
/*
 * packet.c
 * Original Author:  zhuximin@ruijie.com.cn, 2017-12-2
 * 
 * 实现对经过网卡的所有数据包的捕获
 *             
 */

#include<stdio.h> 
#include<stdlib.h>
#include<WinSock2.h>
#include<string.h>  
#include <ws2tcpip.h>
#include <windows.h>

#define SIO_RCVALL  (IOC_IN|IOC_VENDOR|1)  /*定义网卡为混杂模式*/

int main(void) {
  SOCKET sock;                             /*n来表示接收到的数据包的字节数*/
  char buffer[65535];                      /*buffer数组存放接收到的数据包内容*/
  char *iphead;                            /*两个指针分别指向数据包中的MAC地址和IP地址*/ 
  DWORD n;
  WSADATA wsd;
  DWORD dwBytesRet;
  unsigned int optval = 1;
  char FAR name[MAXBYTE];
  struct hostent FAR* pHostent;
  SOCKADDR_IN sa;
  
  WSAStartup(MAKEWORD(2, 1), &wsd);        /*windows下异步套接字启动命令函数*/
  
  if ( (sock=socket(AF_INET,SOCK_RAW,IPPROTO_IP)) == SOCKET_ERROR) {
    perror("socket");
  }
  
  gethostname(name, MAXBYTE);  
  pHostent = (struct hostent*)malloc(sizeof(struct hostent));  
  pHostent = gethostbyname(name);        
  sa.sin_family = AF_INET;  
  sa.sin_port = htons(1); 
  memcpy(&sa.sin_addr,pHostent->h_addr_list[0],pHostent->h_length);
  
  bind(sock, (SOCKADDR*)&sa, sizeof(sa));
  
  WSAIoctl(sock, SIO_RCVALL, &optval, sizeof(optval), NULL, 0, &dwBytesRet,NULL,NULL);
  
  while (1) {
    printf("----------\n");
    memset(buffer,0,sizeof(buffer));
    n = recv(sock,buffer,sizeof(buffer),0);
    
    printf("%ld bytes read\n",n);
    if (n<42) {                            /*最短的数据包大小判断*/
      perror("recvfrom():");
      printf("Incomplete packet\n");
    }
    
    iphead = (char *)malloc(sizeof(char));
    if (iphead == NULL) {
      printf("申请内存空间失败\n");
      return -1;
    }
    iphead = buffer;
    if (*iphead==0x45) { 
      printf("Source host %d.%d.%d.%d\n",
             iphead[12],iphead[13],
             iphead[14],iphead[15]);
      printf("Dest host %d.%d.%d.%d\n",
             iphead[16],iphead[17],
             iphead[18],iphead[19]);
    }

  }
  free(iphead);
  if ( LOBYTE( wsd.wVersion ) != 1 
            || HIBYTE( wsd.wVersion ) != 1 ) {
      WSACleanup( );
    }
  return 0; 
}
