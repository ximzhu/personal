/*
 * Copyright(C) 2013 Ruijie Network. All rights reserved.
 */
/*
 * check_qq_online.h
 * Original Author: wujincheng@ruijie.com.cn 2013-12-23
 *
 * 检查同网段中某ip是否使用qq的头文件
 *
 * History
 */

#ifndef _CHECK_QQ_ONLINE_H_
#define _CHECK_QQ_ONLINE_H_

#define ARP_REQUEST                             1
#define ARP_REPLY                               2
#define ARP_DEF_HARDW                           1
#define DEF_HLEN                                6
#define DEF_PLEN                                4
#define DEF_OICQ_NLEN                           4
#define OICQ_PORT                               0x1f40
#define OICQ_FLAG                               0x02
#define UDP_PRO                                 0x11
#define ARP_PACKET_LEN                          42
#define DEF_ETH_NAME                            200
#define REC_PACKET_LEN                          1500
#define ETH_TYPE_IP                             0x0800 /* IP */
#define ETH_TYPE_ARP                            0x0806 /* Address resolution */

#define uchar                                   unsigned char
#define ushort                                  unsigned short

typedef struct host_msg {
    int hmsg_ifindex;                           /* 接口类型 */
    char hmsg_name[DEF_ETH_NAME];
    uchar hmsg_mac[DEF_HLEN];
    uchar hmsg_ip[DEF_PLEN];
} host_msg_t;

typedef struct eth_layer {
    uchar dmac_addr[DEF_HLEN];
    uchar smac_addr[DEF_HLEN];
    ushort ether_type;
} eth_layer_t;

typedef struct ip_layer {
    uchar versi_hlen;
    uchar type_of_serv;
    ushort total_length;
    ushort id;
    ushort flags;
    uchar ttl;
    uchar protocol;
    ushort checksum;
    uchar src_ip[DEF_PLEN];
    uchar dst_ip[DEF_PLEN];
} ip_layer_t;

typedef struct arp_packet {
    uchar dmac_addr[DEF_HLEN];
    uchar smac_addr[DEF_HLEN];
    ushort ether_type;
    ushort hardware;
    ushort protocol;
    uchar hardwlen;
    uchar protolen;
    ushort operation;
    uchar send_mac[DEF_HLEN];
    uchar send_ip[DEF_PLEN];
    uchar targ_mac[DEF_HLEN];
    uchar targ_ip[DEF_PLEN];
} arp_packet_t;

typedef struct udp_h_layer {
    ushort sour_port;
    ushort desti_port;
    ushort udp_len;
    ushort checksum;
} udp_h_layer_t;

typedef struct oicq_packet {
    struct eth_layer eth_header;
    struct ip_layer ip_header;
    struct udp_h_layer udp_header;
    uchar oicq_flag;
    ushort oicq_ver;
    ushort oicq_cmd;
    ushort oicq_seq;
    uchar oicq_num[DEF_OICQ_NLEN];
} oicq_packet_t;

bool check_qq_online(char *listen_ip, char *gateway_ip);

#endif /* _CHECK_QQ_ONLINE_H_ */
