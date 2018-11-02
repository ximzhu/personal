/*
 * Copyright(C) 2013 Ruijie Network. All rights reserved.
 */
/*
 * intf.c
 * Original Author: gaoxf@ruijie.com.cn, 2013-9-30
 *
 *
 * History
 */

#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pcap.h>
#include <cli.h>
#include <as_parse.h>
#include <debug.h>
#include <send.h>

static int send_intf(void);

CLI_DEF(intf, "Display all interface", send_intf);

static int dump_intf(void)
{
    pcap_if_t *alldevs;
    char errbuf[PCAP_ERRBUF_SIZE];
    int i;
    pcap_if_t *d;
    pcap_addr_t *a;
    unsigned char *ipv4ch;

    /* Retrieve the device list */
    if(pcap_findalldevs(&alldevs, errbuf) == -1) {
        printf("Error in pcap_findalldevs: %s\n", errbuf);
        return -1;
    }

    printf("\nEthernet adapter:");
    i = 0;
    for(d = alldevs; d; d = d->next) {
        i++;
        for (a = d->addresses; a; a = a->next) {
            if ((a->addr->sa_family == AF_INET) && a->addr) {
                ipv4ch = (unsigned char *)(&(((struct sockaddr_in *)a->addr)->sin_addr.s_addr));
                printf("\n    eth%-2d : %d.%d.%d.%d",
                    i, ipv4ch[0], ipv4ch[1], ipv4ch[2], ipv4ch[3]);
            }
        }
    }
    printf("\n");

    pcap_freealldevs(alldevs);


    return 0;
}

static int send_intf(void)
{
    if (list_empty(&(CLI_VAR(intf).arg_lst))) {
        return dump_intf();
    }

    /* ###:参数有效性判断，及转换 */

    write_cfg(&(CLI_VAR(intf)));

    return 0;
}

static char *as_get_dev_by_if(char *ip)
{
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_if_t *d;
    unsigned char *ipv4ch;
    pcap_if_t *alldevs;
    pcap_addr_t *a;
    char ipaddr[sizeof("192.168.100.100")];

    /* Retrieve the device list */
    if(pcap_findalldevs(&alldevs, errbuf) == -1) {
        printf("Error in pcap_findalldevs: %s\n", errbuf);
        return(NULL);
    }

    for(d = alldevs; d; d = d->next) {
        for (a = d->addresses; a; a = a->next) {
            if ((a->addr->sa_family == AF_INET) && a->addr) {
                ipv4ch = (unsigned char *)(&(((struct sockaddr_in *)a->addr)->sin_addr.s_addr));
                sprintf(ipaddr, "%d.%d.%d.%d", ipv4ch[0], ipv4ch[1], ipv4ch[2], ipv4ch[3]);
                if (strcmp(ipaddr, ip) == 0) {
                    return(d->name);
                }
            }
        }
    }

    pcap_freealldevs(alldevs);

    return(NULL);

}

/**
 * as_send - 向指定端口发送指定长度指定次数报文
 * @if_name: 端口字符串，可以是别名，也可以是ip地址
 * @buf: 报文的内容
 * @buf_len: 报文的长度
 * @send_num: 发送次数
 *
 * 根据接口名字找到驱动中对应的端口，这里暂时不做过长过短报文的判断
 *
 * 返回：小于等于0是各种异常发生，大于0是发送成功次数
 */
static int as_send_if(char *if_name)
{
    char *devname;
    pcap_t *fp;
    char errbuf[PCAP_ERRBUF_SIZE];
    int i;

    /* Open the adapter */
    devname = as_get_dev_by_if(if_name); /* ###: 暂时只能根据ip地址识别 */
    if (devname == NULL) {
        return -2;
    }

    fp = pcap_open_live(devname, 65536, 1, 1000, errbuf); /* 数字为pcap推荐值 */
    if (fp == NULL) {
        printf("\nUnable to open the adapter. %s is not supported by WinPcap\n", if_name);
        return -3;
    }

    for (i = 0; i < as_get_sendnum(); i++) {
        if (pcap_sendpacket(fp, as_get_buf(), as_get_buflen()) != 0)  {
            printf("\nError sending the packet: %s\n", pcap_geterr(fp));
            pcap_close(fp);
            return i;
        }
        /* ###:和报文控制对接，没发送一个报文触发一次报文的修改，达到递增递减随机等处理 */
    }

    pcap_close(fp);

    return i;
}

int as_send(void)
{
    struct arg_s *pos;
    int rv;
    int send_count;

    if (CLI_VAR(intf).arg_lst.next == 0) {
        return 0;
    }
    send_count = 0;
    /* 释放已有参数列表 */
    list_for_each_entry(pos, &(CLI_VAR(intf).arg_lst), lst) {
        rv = as_send_if(pos->arg);
        if (rv > 0) {
            send_count += rv;
        }
    }

    return send_count;
}
