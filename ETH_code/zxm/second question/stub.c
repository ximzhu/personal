/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * stub.c
 * Original Author: zhuximin@ruijie.com.cn, 2018-04-16
 *
 * Pile test function.
 *
 * History
 *
 */

#include <stdio.h>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <stdlib.h>
#include <Windows.h>
#include <string.h>
#include <time.h>
#include <windows.h>

void *stub_malloc(int s, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return NULL;
        }
        fclose(fd);
    }

    return malloc(s);
}

FILE *stub_fopen(const char * path, const char *mode, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return NULL;
        }
        fclose(fd);
    }

    return fopen(path, mode);
}

int stub_WSAGetLastError(int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return -99;
        }
        fclose(fd);
    }

    return WSAEACCES;
}

int stub_gethostname(char FAR *name, int namelen, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return SOCKET_ERROR;
        }
        fclose(fd);
    }

    return gethostname(name, namelen);
}

int stub_bind(SOCKET sockaddr, const struct sockaddr FAR *my_addr, int addrlen, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return -1;
        }
        fclose(fd);
    }

    return bind(sockaddr, my_addr, addrlen);
}

int stub_WSAIoctl(SOCKET s, DWORD dwIoControlCode, LPVOID lpvInBuffer,
    DWORD cbInBuffer, LPVOID lpvOutBuffer, DWORD cbOutBuffer, LPDWORD lpcbBytesReturned,
    LPWSAOVERLAPPED lpOverlapped, LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return 1;
        }
        fclose(fd);
    }

    return WSAIoctl(s, dwIoControlCode, lpvInBuffer, cbInBuffer, lpvOutBuffer, cbOutBuffer, 
        lpcbBytesReturned, lpOverlapped, lpCompletionRoutine);
}

int stub_WSAStartup(WORD wVersionRequested, LPWSADATA lpWSAData, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return -1;
        }
        fclose(fd);
    }

    return WSAStartup(wVersionRequested, lpWSAData);
}

int stub_socket(int domain, int type, int protocol, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return -1;
        }
        fclose(fd);
    }

    return socket(domain, type, protocol);
}

int stub_recv(int s, void *buf, int len, unsigned int flags, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return 20;
        }
        fclose(fd);
    }

    return recv(s, buf, len, flags);
}

struct hostent* stub_gethostbyname(const char *name, int line)
{
    FILE *fd;
    int fail_line;

    fd = fopen("stub.cfg", "r");
    if (fd) {
        fail_line = 0;
        (void)fscanf(fd, "%d", &fail_line);
        if (line == fail_line) {
            return NULL;
        }
        fclose(fd);
    }

    return gethostbyname(name);
}
