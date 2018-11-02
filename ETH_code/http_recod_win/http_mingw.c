/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * http_mingw.c
 * Original Author:  liqinban@ruijie.com.cn, 2018-4-9
 *
 * Get the visitor information ( HTTP requests[http://172.31.53.11/xxxxx]).
 * In a Windows environment, record access to specific URL information to EXCEL,
 * and then import the excel file after reading the url rule filter access reco-
 * -rd from config.txt.
 *
 * History 
 *   v1.1     zhuximin@ruijie.com.cn        2018-4-13
 *            Modify the function implementation, and then import
 *            the excel file after reading the url rule filter a-
 *            -ccess record from config.txt.
 */

#include "http.h"

static int is_url_snfx(char *url, int url_size)
{
    FILE *config_file;
    char *url_sufx;
    char url_config[MAX_URL_SNFX];
    int flag;

    flag = 0;
    config_file = fopen("config.txt", "r");
    memset(url_config, 0x00, sizeof(url_config));
    while (fgets(url_config, MAX_URL_SNFX, config_file) != NULL) {
        url_sufx = url + url_size - strlen(url_config) + 1;
        if (strncmp(url_config, url_sufx, strlen(url_config) - 1) == 0) {
            flag = 1;
            return flag;
        }
        memset(url_config, 0, MAX_URL_SNFX);
    }

    return flag;
}

static void record(u_8_t *ip_buf, char *url)
{
    time_t timep;
    struct tm *p;
    u_8_t date_buf[DATE_SIZE];
    u_8_t time_buf[TIME_SIZE];
    FILE *excel_file;
    
    memset(time_buf, 0x00, sizeof(time_buf));
    time(&timep);
    p = localtime(&timep);
    sprintf((char *)date_buf, "%04d-%02d-%02d", p->tm_year + 1900, p->tm_mon + 1, p->tm_mday);
    sprintf((char *)time_buf, "%02d:%02d:%02d", p->tm_hour, p->tm_min, p->tm_sec);

    excel_file = fopen(EXCEL_FILE, "a+");
    if (excel_file == NULL) {
        printf("Open %s failed!\n", EXCEL_FILE);
        printf("Please close it and then resatrt\n!");
        return;
    } else {
        fseek(excel_file, 0, 2);
        if (ftell(excel_file) == 0) {
            fprintf(excel_file, "URL,IP,Date,Time\n");
        }
        printf("%s visits your web page(url is :%s)\n", ip_buf, url);
        printf("records it to the %s!\n", EXCEL_FILE);
        fprintf(excel_file, "%s, %s, %s, %s\n", url, ip_buf, date_buf, time_buf);
    }
    fclose(excel_file);
    excel_file = NULL;
}

static void parse(u_8_t *buf) 
{
    ip_hdr_t *ip_head;
    tcp_hdr_t *tcp_head;
    u_8_t *http_head;
    u_8_t ip_buf[IPADDR_LEN];
    char url[URL_SIZE];
    int tcp_lenth;
    int i;

    ip_head = (ip_hdr_t *)buf;

    if (ip_head->proto != IPPROTO_TCP) {
        return;
    }

    memset(ip_buf, 0x00, sizeof(ip_buf));
    strncpy((char *)ip_buf, inet_ntoa(ip_head->sip), IPADDR_LEN);

    if (strncmp((char *)inet_ntoa(ip_head->dip), DST_IP, strlen(DST_IP)) != 0) {
        return;
    }

    tcp_head = (tcp_hdr_t *)(buf + IP_HEAD);
    tcp_lenth = (tcp_head->lenres >> 4) * 4;
    http_head = buf + IP_HEAD + tcp_lenth;
    if (strncmp((char *)http_head, "GET", 3) != 0) {
        return;
    }
    
    memset(url, 0x00, sizeof(url));
    for (i = 0; i < URL_SIZE; i++) {
        if (*(http_head + 4 + i) == 0x20) {
            break;
        }
        url[i] = (char)*(http_head + 4 + i);
    }

    if (is_url_snfx(url, strlen(url))) {
        record(ip_buf, url);
    }
}

static void stop(int signo) 
{
    printf("Program terminated!\n");
    exit(0);
}

int main(void)
{
    SOCKET raw_sock;
    int recv_data;                 /* The length of recv data */
    u_8_t buf[BUF_MAX];            /* store packet captured */
    struct hostent * host_entry;    /* store host information */
    WSADATA wsd;                   /* parameter of WSAStartup */
    int ret_wsas;                  /* return value of WSAStartup() */
    SOCKADDR_IN sa;
    char name[MAXBYTE];            /* Store the standard hostname */
    int ret_bind;                  /* return value of bind() */

    /* initiates use of the Winsock DLL by a process */
    if ((ret_wsas = WSAStartup(MAKEWORD(2, 2), &wsd)) != 0) {
        exit(ret_wsas);
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

    memset(name, 0x00, sizeof(name));
    if (gethostname(name, MAXBYTE)) {
        exit(WSAGetLastError());
    }
    host_entry = gethostbyname(name);
    sa.sin_family = AF_INET;
    sa.sin_port = htons(1);
    memcpy(&sa.sin_addr, host_entry->h_addr_list[0], host_entry->h_length);
    ret_bind = bind(raw_sock, (SOCKADDR*)&sa, sizeof(sa));
    if (ret_bind < 0) {
        printf("Failed to bind()!\n");
        closesocket(raw_sock);
        return -1;
    }

    signal(SIGINT, stop);
    printf("The program is running......\n");
    while (1) {
        memset(buf, 0x00, sizeof(buf));
        recv_data = recv(raw_sock, (char *)buf, sizeof(buf), 0);
        if (recv_data == SOCKET_ERROR) {
            continue;
        }

        parse(buf);
    }

    closesocket(raw_sock);

    return 0;
}
