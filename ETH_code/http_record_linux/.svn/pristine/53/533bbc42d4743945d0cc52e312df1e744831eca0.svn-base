/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * http_record_capture.c
 * Original Author:  zhuximin@ruijie.com.cn, 2018-3-6
 *
 * Capture frames that pass through the network card and
 * record access to a specific url to EXCEL.
 *
 * History
 *
 * v1.2     zhuximin@ruijie.com.cn        2018-4-10
 *          Remove unnecessary function code.
 *
 * v1.1     zhuximin@ruijie.com.cn        2018-4-9
 *          Added the ability to record access records.
 *
 */
 
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/ether.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#include <time.h>

#define BUF_MAX            1522          /* Maximum length of Ethernet frame */
#define ETH_MIN            42            /* the minimum length of Ethernet frame */
#define ETH_HEAD           14            /* The head of Ethernet frame */
#define MAX                100000        /* The maximum number of capturing */
#define IP_BUF_SIZE        50            /* The length of ip_buf array */
#define TIME_BUF_SIZE      50            /* The length of time_buf array */
#define IP_LEN             20            /* The length of IP head */
#define TCP_LEN            20            /* The length of TCP head */
#define DEFAULT_URL        "/meol"       /* default url path */
#define METHOD             "GET"         /* http method */
#define DEFAULT_FILE       "test.csv"    /* The filename of excel */
#define URL_MAX_SIZE       128           /* the maximum length of url_buf */
#define METHOD_MAX_SIZE    10            /* the length of method buf */
#define IP_PROTO           0x45          /* the hex value of IP protocol */
#define PORT_HEX_VAL_1     0x00          /* the hex first byte of TCP PORT */
#define PORT_HEX_VAL_2     0x50          /* the hex second byte of TCP PORT */

int raw_sock;                    /* Original socket */
char *url;                       /* pointer to url */
char *excel_file;                /* pointer to excel_file */
int flag_url;                    /* url is entered or not */
int flag_file;                   /* filename is entered or not */
char ip_buf[IP_BUF_SIZE];        /* an array of store ip */
char time_buf[TIME_BUF_SIZE];    /* an array of store time */

static void getdata(int argc, char *argv[]);
static void wt_ip_buf(unsigned char *ip_head);
static void http_base(unsigned char *http_head);
static void anlys_frame(unsigned char *buf);
static void p_free(void);
static void stop(int signo);

static void getdata(int argc, char *argv[]) {
    int opt;
    int len_opt;
    char *p_tmp;
    
    if (argc < 2) {
        printf("Use the system default parameters!\n");
        return;
    }

    while ((opt = getopt(argc, argv, "u:f:")) != EOF) {
        if (optarg== NULL) {
            break;
        } else {
            len_opt = strlen(optarg);
        }

        switch (opt) {
        case 'u':
            flag_url = 1;
            url = NULL;
            url = (char *)malloc(len_opt);
            if (url == NULL) {
                printf("Failed to malloc!\n");
                return;
            }

            p_tmp = url;
            break;
         case 'f':
            flag_file = 1;
            excel_file = NULL;
            excel_file = (char *)malloc(len_opt);
            if (excel_file == NULL) {
                printf("Failed to malloc!\n");
                return;
            }

            p_tmp = excel_file;
            break;
        default:
            break;

        }/* end for switch */

        bzero(p_tmp, len_opt);
        memmove(p_tmp, optarg, len_opt);
    }/* end for while */

    p_tmp = NULL;
}

static void wt_ip_buf(unsigned char *ip_head) {
    sprintf(ip_buf, "%u.%u.%u.%u",
            (unsigned char)*(ip_head + 12), (unsigned char)*(ip_head + 13),
            (unsigned char)*(ip_head + 14), (unsigned char)*(ip_head + 15));
}

static void http_base(unsigned char *http_head) {
    time_t timep;
    struct tm *p;
    unsigned char meth_buf[METHOD_MAX_SIZE];
    unsigned char url_buf[URL_MAX_SIZE];
    FILE *fp;

    strncpy((char *)meth_buf, (const char *)(http_head), sizeof(METHOD) - 1);
    strncpy((char *)url_buf, (const char *)(http_head + 4), sizeof(url) - 1);

    if ((strncmp((const char*)meth_buf, METHOD, sizeof(METHOD) - 1) == 0) 
            && (strncmp((const char*)url_buf, url, sizeof(url) - 1) == 0)) {
        time(&timep);
        p = localtime(&timep);
        sprintf(time_buf, "%04d-%02d-%02d %02d:%02d:%02d",
            p->tm_year + 1900, p->tm_mon + 1, p->tm_mday,
            p->tm_hour, p->tm_min, p->tm_sec);

        fp = fopen(excel_file, "a+");
        if (fp == NULL) {
            printf("Fopen error!\n");
            return;
        }

        if (fp) {
            fprintf(fp, "%s, %s\n", ip_buf, time_buf);
        }
        
        fclose(fp);
    }
}

static void anlys_frame(unsigned char *buf) {
    unsigned char *iphead;
    unsigned char *httphead;

    if (buf == NULL) {
        printf("The array of data frames is empty!\n");
        return;
    }

    iphead = buf + ETH_HEAD;
    if (*iphead == IP_PROTO) {
        printf("Source IP address: %d.%d.%d.%d\n",
            iphead[12], iphead[13], iphead[14], iphead[15]);
        printf("Destination IP address: %d.%d.%d.%d\n",
            iphead[16], iphead[17], iphead[18], iphead[19]);
    }
    (void)wt_ip_buf(iphead);

    if (*(iphead + IP_LEN + 2) == PORT_HEX_VAL_1 
            && *(iphead + IP_LEN + 3) == PORT_HEX_VAL_2) {
        httphead = iphead + IP_LEN + TCP_LEN;
        (void)http_base(httphead);
    }

    printf("\n");
}

static void p_free(void) {
    if (flag_url) {
        free(url);
    }

    if (flag_file) {
        free(excel_file);
    }

    close(raw_sock);
}

static void stop(int signo) {
    printf("Program terminated!\n");
    (void)p_free();
    exit(0);
}

int main(int argc, char *argv[]) 
{
    int n;                         /* The length of data frame captured */
    unsigned char buf[BUF_MAX];    /* An array of data frames */

    url = DEFAULT_URL;
    excel_file = DEFAULT_FILE;
    (void)getdata(argc, argv);

    raw_sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (raw_sock < 0) {
        printf("Failed to create the original socket!\n");
        return -1;
    }

    while (1) {
        n = recvfrom(raw_sock, buf, sizeof(buf), 0, NULL, NULL);

        if (n < ETH_MIN) {
            printf("Incomplete Ethernet frames!\n");
            close(raw_sock);
            return -1;
        }

        printf("Capturing %d bytes of data frames.\n", n);
        (void)anlys_frame(buf);
        (void)signal(SIGINT,stop);
    }
}
