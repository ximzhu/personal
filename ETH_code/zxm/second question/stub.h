/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * stub.h
 * Original Author: zhuximin@ruijie.com.cn, 2018-04-16
 *
 * The head file of stub.c file.
 *
 * History
 *
 */

/* stub.h */

#ifndef _STUB_H_
#define _STUB_H_

#ifdef _STUB_OPEN_

#define malloc(s)                              stub_malloc(s, __LINE__)
#define fopen(a, b)                            stub_fopen(a, b, __LINE__)
#define WSAGetLastError()                      stub_WSAGetLastError(__LINE__)
#define gethostname(a, b)                      stub_gethostname(a, b, __LINE__)
#define bind(a, b, c)                          stub_bind(a, b, c, __LINE__)
#define WSAIoctl(a, b, c, d, e, f, g, h, i)    stub_WSAIoctl(a, b, c, d, e, f, g, h, i, __LINE__)
#define WSAStartup(a, b)                       stub_WSAStartup(a, b, __LINE__)
#define socket(a, b, c)                        stub_socket(a, b, c, __LINE__)
#define recv(a, b, c, d)                       stub_recv(a, b, c, d, __LINE__)
#define gethostbyname(a)                       stub_gethostbyname(a, __LINE__)

void *stub_malloc(int s, int line);
FILE *stub_fopen(const char *path, const char *mode, int line);
int stub_WSAGetLastError(int line);
int stub_gethostname(char FAR *name, int namelen, int line);
int stub_bind( SOCKET sockaddr, const struct sockaddr FAR *my_addr, int addrlen, int line);
int stub_WSAIoctl(SOCKET s, DWORD dwIoControlCode, LPVOID lpvInBuffer,
    DWORD cbInBuffer, LPVOID lpvOutBuffer, DWORD cbOutBuffer, LPDWORD lpcbBytesReturned,
    LPWSAOVERLAPPED lpOverlapped, LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine,
    int line);
int stub_WSAStartup(WORD wVersionRequested, LPWSADATA lpWSAData, int line);
int stub_socket(int domain, int type, int protocol, int line);
int stub_recv(int s, void *buf, int len, unsigned int flags, int line);
struct hostent* stub_gethostbyname(const char *name, int line);

#endif /* _STUB_OPEN_ */

#endif /* _STUB_H_ */
