/*
 * Copyright(C) 2013 Ruijie Network. All rights reserved.
 */
/*
 * eoc_plat_ether.c
 * Original Author:  huanghongwu@ruijie.com.cn, 2013-10-8
 *
 * 收发原始的报文，超时等待
 *
 * History
 *
 */
#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pcap.h>
#include <packet32.h>
#include <ntddndis.h>
#include <conio.h>
#include <assert.h>

#include "eoc_plat_ether.h"
#include "eoc_log.h"

static int pkt_drv_get_hwaddr(LPADAPTER lpadapter, char *smac_info)
{
    PPACKET_OID_DATA oid_data;
    int ret;

    assert(smac_info != NULL);
	PPRINT("Enter");
    oid_data = (PPACKET_OID_DATA)malloc(ETHER_ADDR_LEN + sizeof(PACKET_OID_DATA));
    if (oid_data == NULL) {
		PPERROR("no enough memory")
        return -EOC_E_MEMORY;
    }

    memset(oid_data, 0, ETHER_ADDR_LEN + sizeof(PACKET_OID_DATA));
    oid_data->Oid = OID_802_3_CURRENT_ADDRESS;
    oid_data->Length = ETHER_ADDR_LEN;

    ret = PacketRequest(lpadapter, FALSE, oid_data);
    if (!ret) {
        free(oid_data);
		PPERROR("PacketRequest Fail")
        return -EOC_E_OPEN;
    }
    memcpy(smac_info, oid_data->Data, ETHER_ADDR_LEN);

    free(oid_data);
	PPRINT("EXIT");

    return 0;
}

static int pkt_drv_getifname(char name[][100])
{
    signed count;
    pcap_if_t *dev;
    pcap_if_t *devices;
    char errbuf[PCAP_ERRBUF_SIZE];

    count = 0;
    devices = NULL;
	PPRINT("Enter");
    if (pcap_findalldevs (&devices, errbuf) == -1) {
        return count;
    }
    for (dev = devices; dev; dev = dev->next, count++) {
        memcpy(name[count], dev->name, strlen(dev->name) + 1);
    }
    pcap_freealldevs (devices);
    return count;
}

/**
 * 报文发送函数
 * @info 包含描述符信息
 * @packet 报文内容
 * @pkt_sz 报文实际大小
 * @return 小于0 出错，成功返回0
 */
int pkt_drv_send(handle_info_t *info, u_int8_t *packet, u_int32_t pkt_sz)
{
    if (info == NULL || packet == NULL) {
        return -EOC_E_PARAM;
    }
	PPRINT("Enter");
    if (pkt_sz < MIN_PACKET) {
        pkt_sz = MIN_PACKET;
    }
    if (pcap_sendpacket(info->adhandle, packet, pkt_sz) != 0) {
        printf("\nError sending the packet: %s\n", pcap_geterr(info->adhandle));
        return -EOC_E_SEND;
    }
    return EOC_E_NONE;
}

/**
 * 报文接收函数
 * @info 包含描述符信息
 * @packet 缓存空间
 * @pkt_sz 缓存空间大小
 * @return 小于0 出错，否则实际报文大小
 */
int pkt_drv_rcv(handle_info_t *info, u_int8_t *packet, u_int32_t pkt_sz)
{
    struct pcap_pkthdr *header;
    const unsigned char *data;
    signed status;
	u_int16_t lenth;

    if (info == NULL || packet == NULL) {
        return -EOC_E_PARAM;
    }

    memset (packet, 0, pkt_sz);
    status = pcap_next_ex(info->adhandle, &header, &data);
    if (status < 0) {
        printf("pcap_next_ex error");
        return -EOC_E_RCV;
    }
    if (status > 0) {
		lenth = header->caplen;
		if (lenth > pkt_sz) {
			lenth = pkt_sz;
		}
        memcpy(packet, data, lenth);
    }
	
    return lenth;
}

/**
 * 获取所有设备描述符和ether 地址
 * @info 包含设备描述符和地址，由调用者提供空间
 * @return 正常返回EOC_E_NONE ，否则返回小于0 的值
 */
int pkt_drv_open(handle_info_t **info)
{
    int i;
    int nic_num;
    LPADAPTER lpadapter;
    char name[NIC_MAX][100]; /* 每个名字的长度 */
    char errbuf[PCAP_ERRBUF_SIZE];
    handle_info_t *tmp;

    if (info == NULL) {
        return -EOC_E_PARAM;
    }
	PPRINT("Enter");
    nic_num = pkt_drv_getifname(name);
    if (nic_num == 0) {
		PPERROR("pkt_drv_getifname Fail");
        return -EOC_E_FAIL;
    }

    *info = (handle_info_t *)calloc(nic_num, sizeof(handle_info_t));
    tmp = *info;
    for (i = 0; i < nic_num; i++) {
        tmp[i].nic_num = nic_num;
        lpadapter =  PacketOpenAdapter(name[i]);
        if (!lpadapter) {
            goto error;
        }

        if (pkt_drv_get_hwaddr(lpadapter, (char *)tmp[i].hwaddr) == -1) {
            PacketCloseAdapter(lpadapter);
            goto error;
        }
        PacketCloseAdapter(lpadapter);

        /* 开启混杂模式,超时, 65536 表示接收完整报文 */
        tmp[i].adhandle = pcap_open_live(name[i], 65536, 1, RV_TIMEOUT, errbuf);
        if (tmp[i].adhandle == NULL) {
            goto error;
        }
		tmp[i].port = i;
    }
	PPRINT("EXIT");
    return EOC_E_NONE;
error:
    i--;
    for (; i != -1; i--) {
        pcap_close(tmp[i].adhandle);
    }
	PPERROR("init Fail");
    return -EOC_E_FAIL;
}

/**
 * 关闭设备描述符，无返回值
 * @info 包含设备描述符信息
 */
void pkt_drv_close(handle_info_t *info)
{
    int i;

    if (info == NULL) {
        return;
    }
	PPRINT("Enter");
    for (i = 0; i < info[0].nic_num; i++) {
        pcap_close(info[i].adhandle);
    }
    free(info);
	PPRINT("EXIT");
}


