/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * http_record_win.c
 * Original Author:  zhuximin@ruijie.com.cn, 2018-4-11
 *
 * In a Windows environment, record access to specific URL information to EXCEL.
 *
 * History
 *
 */
 
#include <stdio.h>
#include <winsock2.h>
#include <windows.h>
#include <WS2tcpip.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

#define NAME_BUF_SIZE    50                /* Maximum length of hostname */
#define RECV_BUF_MAX     2048              /* Maximum length of Ethernet frame */
#define HEAD_LEN_MUL     4                 /* IP header length value */
#define MAX_ADDR_LEN     32                /* the length of IP address */
#define IP_HEAD_LEN      20                /* the length of ip head */
#define TIME_BUF_SIZE    50                /* The length of time_buf array */
#define DEFAULT_FILE     "record.csv"      /* The filename of excel */
#define URL_SIZE         2083              /* IE url maximum length */

typedef struct ip_hdr {
    uint8_t h_verlen;
    uint8_t tos;
    uint16_t total_len;
    uint16_t ident;
    uint16_t frag_and_flags;
    uint8_t ttl;
    uint8_t proto;
    uint16_t checksum;
    struct in_addr sip;
    struct in_addr dip;
}ip_hdr_t;

typedef struct tcp_hdr {
    uint16_t sport;
    uint16_t dport;
    uint32_t seq;
    uint32_t ack;
    uint8_t lenres;
    uint8_t flag;
    uint16_t win;
    uint16_t sum;
    uint16_t urp;
}tcp_hdr_t;


static void http_base(uint8_t * source_ip, uint8_t *url);
static void anlys_frame(uint8_t *buf);
static void stop(int signo);

static void http_base(uint8_t *source_ip, uint8_t *url) {
    time_t timep;
    struct tm *p;
    char time_buf[TIME_BUF_SIZE];
    FILE *fp;

    time(&timep);
    p = localtime(&timep);
    sprintf(time_buf, "%04d-%02d-%02d %02d:%02d:%02d",
        p->tm_year + 1900, p->tm_mon + 1, p->tm_mday,
        p->tm_hour, p->tm_min, p->tm_sec);

    fp = fopen(DEFAULT_FILE, "a+");
    if (fp == NULL) {
        printf("Fopen error!\n");
        return;
    }

    if (fp) {
        fprintf(fp, "%s, %s, %s\n", url, source_ip, time_buf);
    }
    
    fclose(fp);
}

static void anlys_frame(uint8_t *buf) {
    ip_hdr_t *iphead;
    tcp_hdr_t *tcphead;
    uint8_t *httphead;
    int tcp_head_len;
    uint8_t source_ip[MAX_ADDR_LEN];
    uint8_t url_buf[URL_SIZE];
    int i;

    iphead = (ip_hdr_t *)buf;
    strncpy((char *)source_ip, inet_ntoa(iphead->sip), MAX_ADDR_LEN);

    if (iphead->proto == IPPROTO_TCP) {
        tcphead = (tcp_hdr_t *)(buf + IP_HEAD_LEN);
        tcp_head_len = (tcphead->lenres >> 4) * HEAD_LEN_MUL;
        httphead = buf + IP_HEAD_LEN + tcp_head_len;
        if (strncmp((char *)httphead, "GET", 3) == 0) {
            memset(url_buf, 0, URL_SIZE);
             for (i = 0; i < URL_SIZE; i++) {
                if (*(httphead + 4 + i) == 0x20) {
                    break;
                }

                url_buf[i] = *(httphead + 4 + i);
                http_base(source_ip, url_buf);
            }
        }
    }
}

static void stop(int signo) {
    printf("Program terminated!\n");
    printf("The access record has been imported into %s,please check.\n", DEFAULT_FILE);
    exit(0);
}

int main(void)
{
    WSADATA wsd;                  /* Asynchronous startup function parameters */
    int wsasret;                  /* return of the asynchronous boot function */
    SOCKET raw_sock;
    char name[NAME_BUF_SIZE];     /* Store the standard hostname */
    struct hostent *host;         /* store host information */
    SOCKADDR_IN sa;
    int bind_ret;                 /* The return value of the bind() */
    int n;                        /* The number of bytes in the packet captured */
    uint8_t buf[RECV_BUF_MAX];    /* An array of data frames */

    wsasret = WSAStartup(MAKEWORD(2, 2), &wsd);
    if ((wsasret != 0)) {
        printf("Asynchronous socket startup failed!\n");
        return -1;
    }

    raw_sock = socket(AF_INET, SOCK_RAW, IPPROTO_IP);
    if (raw_sock == INVALID_SOCKET) {
        if (WSAGetLastError() == WSAEACCES) {
            printf("Use the administrator permission to restart the program.\n");
            printf("The program will automatically exit after 20S.\n");
            Sleep(20000);
            return -1;
        }
    }

    if (gethostname(name, NAME_BUF_SIZE)) {
        exit(WSAGetLastError());
    }

    host = gethostbyname(name);
    if (host == NULL) {
        printf("Failed to gethostbtname()\n");
        closesocket(raw_sock);
        return -1;
    }

    sa.sin_family = AF_INET;
    sa.sin_port = htons(1);
    memcpy(&sa.sin_addr, host->h_addr_list[0], host->h_length);

    bind_ret = bind(raw_sock, (SOCKADDR *)&sa, sizeof(sa));
    if (bind_ret < 0) {
        printf("Failed to bind()!\n");
        closesocket(raw_sock);
        printf("The program will automatically exit after 20S.\n");
        Sleep(20000);
        return -1;
    }

    printf("Start to capture the access record!\n");

    signal(SIGINT, stop);
    while (1) {
        memset(buf, 0, sizeof(buf));
        n = recv(raw_sock, (char *)buf, sizeof(buf), 0);

        if (n == SOCKET_ERROR) {
            printf("%d", WSAGetLastError());
            continue;
        }

        anlys_frame(buf);
    }

    closesocket(raw_sock);

    return 0;
}
