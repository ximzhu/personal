/* ICMP协议的请求和响应数据报文头C语言描述在<netinet/ip_icmp.h>中的定义
 * 联合体三个成员echo，gateway和frag分别用于echo报文，回应网关地址和查找
 * MTU路径（发现一条具有最大传输单元的路径）。在echo结构中包含两个成员：
 * id用于作为本报文的标识，sequence作为这个报文的序列号。id常常被设置成发
 * 送报文的进程号，用于标识发送报文的进程。而sequence将在每次发送一个报文
 * 后加1。
 */
struct icmphdr
{
	u_int8_t type;           /* message type */
	u_int8_t code;           /* type sub-code */
	u_int16_t checksum;
	union
	{
		struct
		{
			u_int16_t id;
			u_int16_t sequence;
		}echo;               /* echo datagram */
		u_int32_t gateway;   /* gateway address */
		struct
		{
			u_int16_t __unused;
			u_int16_t mtu;
		}frag;               /* path mtu discovery */
	}un;
};


/*IP数据包头部的形式定义*/
struct ip
{
#if_BYTE_ORDER == __LITTLE_ENDIAN
   unsigned int ip_hl:4;     /* header length */
   unsigned int ip_v:4;      /* version */
#endif
#if__BYTE_ORDER == __BIG_ENDIAN
   unsigned int ip_v:4       /* version */
   unsigned int ip_hl:4      /* header length */
#endif  
   u_int8_t ip_tos;          /* type of service */
   u_short ip_len;           /* total length */
   u_short ip_id;            /* identification */
   u_short ip_off;           /* fragment offset field */
#define IP_RF 0x8000         /* reserved fragment flag */
#define IP_DF 0x4000         /* dont fragment flag */
#define IP_MF 0x2000         /* more fragments flag */
#define IP_OFFMASK 0x1fff    /* mask for fragmenting bits */
   u_int8_t ip_ttl;          /* time to live */
   u_int8_t ip_p;            /* protocol */
   u_short ip_sum;           /* checksum */
struct in_addr ip_src,ip_dst;/*source and dest address */
/*the options start here. */
};


/*时间戳选项C语言描述
 *Time stamp option structure.
 */
