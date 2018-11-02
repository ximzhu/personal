/* eoc_plat_ether.h */

#ifndef _EOC_PLAT_ETHER_H_
#define _EOC_PLAT_ETHER_H_

#include <pcap.h>
#include "eoc_type.h"

#define DEBUG_PLAT            0
#define ERROR_PLAT            0
#if (DEBUG_PLAT || DEBUG_ALL)
#define PPRINT(format, arg...) printf("%s(%d):"format"\n" ,__FUNCTION__ , __LINE__, ##arg)
#else
#define PPRINT(format, ...)
#endif

#if (ERROR_PLAT || DEBUG_ALL)
#define PPERROR(format, arg...) printf("%s(%d):"format"\n" ,__FUNCTION__ , __LINE__, ##arg)
#else
#define PPERROR(format, ...)
#endif


#define ETH_P_ALL           0x0003
#define NIC_MAX             16
#define RV_TIMEOUT          100
#define MIN_PACKET          60

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
#if _linux_
    int sendfd;
    int capturefd;
    sockaddr_ll_t st_tag_addr;
#else
    pcap_t *adhandle;
#endif
    u_int8_t nic_num;
    u_int8_t port;
    u_int8_t hwaddr[ETHER_ADDR_LEN];
} handle_info_t;

/* 打开设备并获取相关信息 */
int pkt_drv_open(handle_info_t **info);
/* 关闭设备 */
void pkt_drv_close(handle_info_t *info);
/* 发送报文 */
int pkt_drv_send(handle_info_t *info, u_int8_t *packet, u_int32_t pkt_sz);
/* 接收报文 */
int pkt_drv_rcv(handle_info_t *info, u_int8_t *packet, u_int32_t pkt_sz);

#endif /* _EOC_PLAT_ETHER_H_ */

