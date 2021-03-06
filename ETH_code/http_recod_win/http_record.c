/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * http_record.c
 * Original Author:  liqinban@ruijie.com.cn, 2018-4-9
 *
 * In a Windows environment, read the filter rule from a configuration
 * file first, and then record the access log information of the local
 * server to the EXCEL file.
 *
 * History
 *   v1.2     zhuximin@ruijie.com.cn        2018-4-22
 *            The function of the parse function is independently
 *            composed of more simple and explicit functions, he-
 *            -ader file references and function declarations us-
 *            -ing the HTTP.h header file.
 *   v1.1     zhuximin@ruijie.com.cn        2018-4-13
 *            Modify the function implementation, and then import
 *            the excel file after reading the url rule filter a-
 *            -ccess record from config.txt.
 */

#include <stdio.h>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <stdlib.h>
#include <Windows.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <stdint.h>
#include <stdbool.h>
#include "stub.h"

#define BUF_MAX         1500             /* Maximum length of data */
#define IPADDR_LEN      32               /* length of IP address */
#define DATE_SIZE       11               /* length of date_buf array */
#define TIME_SIZE       9                /* length of time_buf array */
#define CONFIG_FILE     "config.txt"     /* filename of config */
#define EXCEL_FILE      "visitor.csv"    /* filename of excel */
#define MAX_URL_SNFX    10               /* Maximum length of the URL suffix */
#define URL_SIZE        2048             /* The URL of the GET method is the maximum length */
#define SIO_RCVALL      (IOC_IN | IOC_VENDOR | 1)

/* IP header */
typedef struct ip_hdr {
    uint8_t           ihl:4;
    uint8_t           version:4;
    uint8_t           tos;
    uint16_t          total_len;
    uint16_t          ident;
    uint16_t          frag_and_flags;
    uint8_t           ttl;
    uint8_t           proto;
    uint16_t          checksum;
    struct in_addr    sip;
    struct in_addr    dip;
} ip_hdr_t;

/* TCP header */
typedef struct tcp_hdr {
    uint16_t    sport;
    uint16_t    dport;
    uint32_t    seq;
    uint32_t    ack_seq;
    uint8_t     reserved_1:4;
    uint8_t     doff:4;
    uint8_t     fin:1;
    uint8_t     syn:1;
    uint8_t     rst:1;
    uint8_t     psh:1;
    uint8_t     ack:1;
    uint8_t     urg:1;
    uint8_t     reserved_2:2;
    uint16_t    win;
    uint16_t    sum;
    uint16_t    urp;
} tcp_hdr_t;

SOCKET raw_sock;

static void init_socket(void)
{
    WSADATA wsd;
    struct hostent *host_entry;
    SOCKADDR_IN sa;
    char name[MAXBYTE];

    /* initiates use of the Winsock DLL by a process */
    if ((WSAStartup(MAKEWORD(2, 2), &wsd)) != 0) {
        printf("WSAStartup failed with error: %d\n", WSAGetLastError());
        printf("For specific reasons, please find the corresponding explanation from the"
            " Windows official website according to the error code!\n");
        return;
    }

    raw_sock = socket(AF_INET, SOCK_RAW, IPPROTO_IP);
    if (raw_sock == INVALID_SOCKET) {
        if (WSAGetLastError() == WSAEACCES) {
            printf("Use the administrator permission to restart the program!\n");
        }
        return;
    }

    if (gethostname(name, MAXBYTE)) {
        printf("gethostname failed with error:%d\n", WSAGetLastError());
        goto err_printf;
    }
    host_entry = gethostbyname(name);
    sa.sin_family = AF_INET;
    memcpy(&sa.sin_addr, host_entry->h_addr_list[0], host_entry->h_length);
    if (bind(raw_sock, (SOCKADDR *)&sa, sizeof(sa)) < 0) {
        printf("bind failed with error:%d\n", WSAGetLastError());
        goto err_printf;
    }

    return;

err_printf:
    printf("For specific reasons, please find the corresponding explanation from the"
        " Windows official website according to the error code!\n");
    closesocket(raw_sock);
    WSACleanup();
    return;
}

static void get_ip(uint8_t *ip_buf, uint8_t *buf)
{
    ip_hdr_t *ip_head;

    ip_head = (ip_hdr_t *)buf;
    if (ip_head->proto != IPPROTO_TCP) {
        return;
    }

    /* The length of the IP address is fixed */
    (void)strncpy((char *)ip_buf, inet_ntoa(ip_head->sip), IPADDR_LEN);
}

static bool get_url(char *url, uint8_t *buf)
{
    ip_hdr_t *ip_head;
    tcp_hdr_t *tcp_head;
    uint8_t *http_head;
    int url_index;
    int i;

    ip_head = (ip_hdr_t *)buf;
    tcp_head = (tcp_hdr_t *)(buf + (ip_head->ihl * 4));
    http_head = buf + (ip_head->ihl * 4) + (tcp_head->doff * 4);
    if (strncmp((char *)http_head, "GET", 3) != 0) {
        return false;
    }

    i = 0;
    url_index = 4;
    while ((i < URL_SIZE) && (*(http_head + url_index + i) != 0x20)) {
        url[i] = (char)*(http_head + url_index + i);
        i++;
    }
    url[i] = '\0';

    return true;
}

static bool is_urlsnfx(char *url, int url_size)
{
    FILE *config_file;
    char *url_sufx;
    char url_config[MAX_URL_SNFX];

    config_file = fopen(CONFIG_FILE, "r");
    if (config_file == NULL) {
        printf("Open the config.txt configuration file failed!\n");
        printf("please check if the file exists!\n");
        return false;
    }

    while (fgets(url_config, MAX_URL_SNFX, config_file) != NULL) {
        printf("%s %d\n", url_config, strlen(url_config));
        url_sufx = url + url_size - strlen(url_config);
        if (strncmp(url_config, url_sufx, strlen(url_config)) == 0) {
            fclose(config_file);
            return true;
        }
    }

    fclose(config_file);
    return false;
}

static void get_time(char *date_buf, char *time_buf)
{
    time_t tm_now;
    struct tm *p_tm;

    if (time(&tm_now) < 0) {
        return;
    }

    p_tm = localtime(&tm_now);
    if (p_tm == NULL) {
        return;
    }

    (void)strftime(date_buf, 11, "%Y-%m-%d", p_tm);
    (void)strftime(time_buf, 9, "%H:%M:%S", p_tm);
}

static void record_visit(uint8_t *ip_buf, char *url)
{
    char date_buf[DATE_SIZE];
    char time_buf[TIME_SIZE];
    FILE *excel_file;

    get_time(date_buf, time_buf);

    excel_file = fopen(EXCEL_FILE, "a+");
    if (excel_file == NULL) {
        printf("Open %s failed!\n", EXCEL_FILE);
        printf("Please close it and then resatrt!\n");
        return;
    } else {
        (void)fseek(excel_file, 0, 2);
        if (ftell(excel_file) == 0) {
            (void)fprintf(excel_file, "URL,IP,Date,Time\n");
        }
        printf("%s visits your web page(url is :%s)\n", ip_buf, url);
        printf("records it to the %s!\n", EXCEL_FILE);
        (void)fprintf(excel_file, "%s, %s, %s, %s\n", url, ip_buf, date_buf, time_buf);
    }
    fclose(excel_file);
}

static void parse_packet(uint8_t *buf) 
{
    uint8_t ip_buf[IPADDR_LEN];
    char url[URL_SIZE];

    get_ip(ip_buf, buf);

    if (!get_url(url, buf)) {
        return;
    }

    if (is_urlsnfx(url, strlen(url))) {
        record_visit(ip_buf, url);
    }
}

static void end_program(int signo)
{
    printf("Program terminated!\n");
    exit(0);
}

int main(void)
{
    int recv_data;           /* The length of recv data */
    uint8_t buf[BUF_MAX];    /* store packet captured */
    uint32_t optval;
    DWORD bytes_ret;

    init_socket();

    optval = 1;
    if (WSAIoctl(raw_sock, SIO_RCVALL, &optval, sizeof(optval), NULL, 0, &bytes_ret, NULL, NULL)) {
        closesocket(raw_sock);
        exit(WSAGetLastError());
    }

    signal(SIGINT, end_program);
    printf("The program is running......\n");
    while (1) {
        memset(buf, 0x0, BUF_MAX);
        recv_data = recv(raw_sock, (char *)buf, sizeof(buf), 0);
        if (recv_data == SOCKET_ERROR) {
            continue;
        }

        parse_packet(buf);
    }

    return 0;
}
