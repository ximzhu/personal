

#include <stdio.h>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <stdlib.h>
#include <Windows.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <errno.h>

#define BUF_MAX        1500              /* Maximum length of data */
#define IP_HEAD        20                /* IP header */
#define IPADDR_LEN     32                /* length of IP address */
#define DATE_SIZE      10                /* length of date_buf array */
#define TIME_SIZE      80                /* length of time_buf array */
#define URL_SIZE       2083              /* IE url maximum length */
#define CONFIG_FILE    "config.txt"      /* filename of config */
#define EXCEL_FILE     "visitor.csv"     /* filename of excel */
#define DST_IP         "172.31.53.11"    /* Destination IP */
#define MAX_URL_SNFX   10                /* Maximum length of the URL suffix */

typedef unsigned char u_8_t;
typedef unsigned short u_16_t;
typedef unsigned int u_32_t;
typedef struct ip_hdr {
    u_8_t h_verlen;
    u_8_t tos;
    u_16_t total_len;
    u_16_t ident;
    u_16_t frag_and_flags;
    u_8_t ttl;
    u_8_t proto;
    u_16_t checksum;
    struct in_addr sip;
    struct in_addr dip;
}ip_hdr_t;

typedef struct tcp_hdr {
    u_16_t sport;
    u_16_t dport;
    u_32_t seq;
    u_32_t ack;
    u_8_t lenres;
    u_8_t flag;
    u_16_t win;
    u_16_t sum;
    u_16_t urp;
}tcp_hdr_t;

static int is_url_snfx(char *url, int url_size);
static void record(u_8_t *ip_buf, char *url);
static void parse(u_8_t *buf);
static void stop(int signo);