/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * capture.c
 * Original Author:  zhuximin@ruijie.com.cn, 2018-3-6
 *
 * Capture frames that pass through the network card.
 *
 * History
 *
 */
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ether.h>
#include <arpa/inet.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>

#define BUF_MAX        1518                          /* Maximum length of Ethernet frame */
#define ETH_HEAD       14                            /* The head of Ethernet frame */
#define HEX_MAC_LEN    6                             /* The length of hexadecimal MAC address */
#define BYTE_LEN       8                             /* The number of bits per byte */
#define MAX            100                           /* The maximum number of capturing */

static void hex_to_bin(unsigned char hex_temp, int bin_temp[]);
static int get_mac_type(unsigned char *ethhead);
static void anlys_frame(unsigned char *buf, int n);
static void stop(int signo);

static void hex_to_bin(unsigned char hex_temp, int bin_temp[]) {
    int i;

    if (bin_temp == NULL) {
        printf("The array of binary MAC address does not exit!\n");
        return;
    }

    for (i = 7; i >= 0; i--) {
        if (hex_temp & 1) {
            bin_temp[i] = 1;
            hex_temp = hex_temp >> 1;
        } else {
            bin_temp[i] = 0;
            hex_temp = hex_temp >> 1;
        }
    }

}

static int get_mac_type(unsigned char *ethhead) {
    unsigned char temp;
    int ig_bit;
    int bin_temp[BYTE_LEN];

    if (ethhead == NULL) {
        printf("The MAC address is empty!\n");
        return -1;
    }

    temp = ethhead[0];
    hex_to_bin(temp, bin_temp);
    ig_bit = bin_temp[7];

    return ig_bit;
}

static void anlys_frame(unsigned char *buf, int n) {
    unsigned char *ethhead;
    unsigned char *iphead;
    int ig_sa;
    int ig_da;
    int i, j;
    int index;

    if (buf == NULL) {
        printf("The array of data frames is empty!\n");
        return;
    }

    ethhead = buf + HEX_MAC_LEN;
    printf("Source MAC address: %02x:%02x:%02x:%02x:%02x:%02x",
        ethhead[0], ethhead[1], ethhead[2],
        ethhead[3], ethhead[4], ethhead[5]);
    ig_sa = get_mac_type(ethhead);
    if (ig_sa == 0) {
        printf(" (unicast address.)\n");
    } else if (ig_sa == 1) {
        printf(" (multicast address.)\n");
    }

    ethhead = buf;
    printf("Destination MAC address: %02x:%02x:%02x:%02x:%02x:%02x",
        ethhead[0], ethhead[1], ethhead[2],
        ethhead[3], ethhead[4], ethhead[5]);
    ig_da = get_mac_type(ethhead);
    if (ig_da == 0) {
        printf(" (unicast address.)\n");
    } else if (ig_da == 1) {
        printf(" (multicast address.)\n");
    }

    iphead = buf + ETH_HEAD;
    if (*iphead == 0x45) {
        printf("Source IP address: %d.%d.%d.%d\n",
            iphead[12], iphead[13], iphead[14], iphead[15]);
        printf("Destination IP address: %d.%d.%d.%d\n",
            iphead[16], iphead[17], iphead[18], iphead[19]);
    }

    for (i = 0; i <= (n / 16); i++) {
        for (j = 0; j < 16; j++) {
            index = (i * 16) + j;
            if (n > index) {
                printf("%02x ", ethhead[index]);
            }
        }

        printf("\n");
    }

    printf("\n");
}

static void stop(int signo) {
    printf("Program terminated!\n");
    exit(0);
}

int main(void)
{
    int raw_sock;                                /* Original socket */
    int n;                                       /* The length of data frame captured */
    unsigned char buf[BUF_MAX];                  /* An array of data frames */
    int sum;

    raw_sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (raw_sock < 0) {
        printf("Failed to create the original socket!\n");
        return -1;
    }

    while (1) {
        n = recvfrom(raw_sock, buf, sizeof(buf), 0, NULL, NULL);

        if (n < 42) {
            printf("Incomplete Ethernet frames!\n");
            close(raw_sock);
            return -1;
        }

        printf("Capturing %d bytes of data frames.\n", n);
        anlys_frame(buf, n);
        signal(SIGINT,stop);
    }

    close(raw_sock);

    return 0;
}
