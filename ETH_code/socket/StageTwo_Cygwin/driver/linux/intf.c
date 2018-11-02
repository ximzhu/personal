/*
 * Copyright(C) 2013 Ruijie Network. All rights reserved.
 */
/*
 * intf.c
 * Original Author: huanghongwu@ruijie.com.cn, 2013-12-25
 *
 * 实现对网络设备的扫描，并以IP形式显示出来
 *
 * History
 *  v1.1 zhangdexin@ruijie.com.cn, 2014-01-02
 *  添加接口发送报文统计通知
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <linux/if.h>
#include <arpa/inet.h>
#include <errno.h>
#include <linux/if_packet.h>
#include <assert.h>
#include <cli.h>
#include <send.h>
#include "../../list.h"

static int dump_intf(void);

#define ETH_P_ALL   0x0003

CLI_DEF(intf, "Display all interface", dump_intf);

typedef struct {
    unsigned short int sll_family;
    unsigned short int sll_protocol;
    int sll_ifindex;
    unsigned short int sll_hatype;
    unsigned char sll_pkttype;
    unsigned char sll_halen;
    unsigned char sll_addr[8];  /* 外部代码:该值没有用到 */
} sockaddr_ll_t;

typedef struct {
    int pkt_count;
    char *intf_name;
    struct list_head list;
} intf_info_node_t;

static sockaddr_ll_t st_tag_addr;

static int select_net_card(const char *name, int fd)
{
    int ret;
    struct ifreq req;

    strncpy(req.ifr_name, name, strlen(name) + 1);
    /* 打印IP信息 */
    ret = ioctl(fd, SIOCGIFADDR, &req);
    if (ret == -1) {
       return -1;
    }
    printf("%s : %s\n", name,inet_ntoa(((struct sockaddr_in *)&(req.ifr_addr))->sin_addr));
    
    return 0;
}

static int get_alldev_info(int fd)
{
    int i;
    int count;
    struct ifconf ifc;
    struct ifreq ifr[16];   /* 最多16张网卡 */
    struct ifreq *req;

    /* get nics */
    ifc.ifc_len = sizeof(ifr);
    ifc.ifc_req = ifr;
    if (ioctl(fd, SIOCGIFCONF, &ifc) < 0) {
        perror("socket");
        return -1;
    }

    /* get nic info */
    count = ifc.ifc_len / sizeof(struct ifreq);
    for (i = 0; i < count; i++) {
        req = &ifr[i];
        if (select_net_card(req->ifr_name, fd) != 0) {
            return -1;
        }
    }

    return 0;
}

/**
 * dump_intf - 获取所有设备描述符和ether 地址
 *
 * 返回值: 正常返回1 ，否则返回0
 */
int dump_intf(void)
{
    int socket_fd;

    /* 消除警告 */
    CLR_WARNING(intf);
    /* 创建原始数据的socket */
    socket_fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (socket_fd == -1) {
        printf("create the packet socket error!\n");
        return 1;
    }

    if (get_alldev_info(socket_fd) != 0) {
        close(socket_fd);
        return 1;
    }

    return 0;
}

static int dev_is_exist(const char *name, int fd, char *ip)
{
    int ret;
    struct ifreq req;
    char ipaddr[sizeof("192.168.100.100")];

    strncpy(req.ifr_name, name, strlen(name) + 1);
    /* 打印IP信息 */
    ret = ioctl(fd, SIOCGIFADDR, &req);
    if (ret == -1) {
       return 0;
    }
    sprintf(ipaddr, "%s", inet_ntoa(((struct sockaddr_in *)&(req.ifr_addr))->sin_addr));
    if (memcmp(ipaddr, ip, strlen(ip)) == 0) {
        memset(&st_tag_addr, 0, sizeof(st_tag_addr));
        ret = ioctl(fd, SIOCGIFINDEX, &req);
        if (ret == -1) {
           return 0;
        }
        st_tag_addr.sll_ifindex = req.ifr_ifindex;
        st_tag_addr.sll_family = PF_PACKET;
        st_tag_addr.sll_protocol = htons(ETH_P_ALL);
        return 1;
    }

    return 0;
}

static int as_get_dev_by_if(int fd, char *ip)
{
    int i;
    int count;
    struct ifconf ifc;
    struct ifreq ifr[16];   /* 最多16张网卡 */
    struct ifreq *req;

    /* get nics */
    ifc.ifc_len = sizeof(ifr);
    ifc.ifc_req = ifr;
    if (ioctl(fd, SIOCGIFCONF, &ifc) < 0) {
        perror("socket");
        return 0;
    }

    /* get nic info */
    count = ifc.ifc_len / sizeof(struct ifreq);
    for (i = 0; i < count; i++) {
        req = &ifr[i];
        if (dev_is_exist(req->ifr_name, fd, ip)) {
            return 1;
        }
    }

    return 0;
}

static int as_send_if(char *if_name)
{
    int socket_fd;
    int i;
    int ret;

    /* 创建原始数据的socket */
    socket_fd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (socket_fd == -1) {
        printf("create the packet socket error!\n");
        return -1;
    }

    if (!as_get_dev_by_if(socket_fd, if_name)) {
        close(socket_fd);
        return -2;
    }

    for (i = 0; i < as_get_sendnum(); i++) {
        ret = sendto(socket_fd, as_get_buf(), as_get_buflen(), 0,
            (const struct sockaddr*)&(st_tag_addr), sizeof(sockaddr_ll_t));
        if (ret == -1) {
            close(socket_fd);
            return i;
        }
    }

    close(socket_fd);

    return i;
}

static intf_info_node_t *creat_an_intf_node(char *intf_name)
{
    intf_info_node_t *p_new_intf_node;
    char *tmp_intf_name;

    p_new_intf_node = (intf_info_node_t *)malloc(sizeof(intf_info_node_t));
    if (p_new_intf_node == NULL) {
        return NULL;
    }
    memset(p_new_intf_node, 0, sizeof(intf_info_node_t));
    tmp_intf_name = (char *)malloc(strlen(intf_name) + 1);
    if (tmp_intf_name == NULL) {
        free(p_new_intf_node);
        return NULL;
    }
    memcpy(tmp_intf_name, intf_name, strlen(intf_name) + 1);
    p_new_intf_node->intf_name = tmp_intf_name;

    return p_new_intf_node;
}

static intf_info_node_t *find_an_intf_info(char *intf_name, struct list_head *head)
{
    intf_info_node_t *pos;

    list_for_each_entry(pos, head, list) {
        if (strcmp(pos->intf_name, intf_name) == 0) {
            return pos;
        }
    }

    return NULL;
}

/* 接口发送报文数统计 */
static void intf_pkt_statistics(char *intf_name, int count, struct list_head *head)
{
    intf_info_node_t *tmp_intf_info;

    tmp_intf_info = find_an_intf_info(intf_name, head);
    if (tmp_intf_info != NULL) {
        tmp_intf_info->pkt_count += count;
        return;
    }
    tmp_intf_info = creat_an_intf_node(intf_name);
    if (tmp_intf_info == NULL) {
        return;
    }
    tmp_intf_info->pkt_count = count;
    list_add_tail(&tmp_intf_info->list, head);
}

/* 打印接口发送报文数 */
static void intf_pkt_statistics_print(struct list_head *head)
{
    intf_info_node_t *tmp_intf_info;

    if (list_empty(head)) {
        return;
    }

    list_for_each_entry(tmp_intf_info, head, list) {
        printf("%s send %d pkts totally.\n", tmp_intf_info->intf_name, tmp_intf_info->pkt_count);
    }
}

/* 释放接口发送报文统计信息链表 */
static void free_intf_info_list(intf_info_node_t *intf_info_head)
{
    intf_info_node_t *intf_info_pos, *tmp_intf_info;

    list_for_each_entry_safe(intf_info_pos, tmp_intf_info, &intf_info_head->list, list) {
        list_del_init(&intf_info_pos->list);
        free(intf_info_pos->intf_name);
        free(intf_info_pos);
    }
}

int as_send(void)
{
    struct arg_s *pos;
    int rv;
    int send_count;
    intf_info_node_t intf_info_head;

    if (CLI_VAR(intf).arg_lst.next == 0) {
        return 0;
    }

    send_count = 0;
    INIT_LIST_HEAD(&intf_info_head.list);
    list_for_each_entry(pos, &(CLI_VAR(intf).arg_lst), lst) {
        rv = as_send_if(pos->arg);
        if (rv > 0) {
            send_count += rv;
            intf_pkt_statistics(pos->arg, rv, &intf_info_head.list);
        }
    }
    intf_pkt_statistics_print(&intf_info_head.list);
    free_intf_info_list(&intf_info_head);
    
    return send_count;
}
