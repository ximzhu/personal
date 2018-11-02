#include <stdio.h>
#include<stdlib.h>
#include<string.h>  
#include <ws2tcpip.h>
#include <windows.h>
#include <WinSock2.h>
#define   SIO_RCVALL   _WSAIOW(IOC_VENDOR,1)
#pragma comment(lib,"ws2_32.lib")
 
typedef struct _iphdr
{
    unsigned char h_lenver;          //4位首部长度+4位IP版本号
    unsigned char tos;               //8位服务类型TOS
    unsigned short total_len;            //16位总长度（字节）
    unsigned short ident;            //16位标识
    unsigned short frag_and_flags;       //16位偏移量
    unsigned char ttl;               //8位生存时间 TTL
    unsigned char proto;             //8位协议 (TCP, UDP 或其他)
    unsigned short checksum;         //16位IP首部校验和
    unsigned int sourceIP;           //32位源IP地址
    unsigned int destIP;                 //32位目的IP地址
}IP_HEADER;
typedef struct _tcphdr               //定义TCP首部
{
    USHORT th_sport;                //16位源端口
    USHORT th_dport;               //16位目的端口
    unsigned int th_seq;                  //32位序列号
    unsigned int th_ack;               //32位确认号
    unsigned char th_lenres;              //4位首部长度/6位保留字
    unsigned char th_flag;            //6位标志位
    USHORT th_win;                 //16位窗口大小
    USHORT th_sum;              //16位校验和
    USHORT th_urp;                 //16位紧急数据偏移量
}TCP_HEADER;
 
 
//////////////////////////////////////////////////////////////////////////
//初始化套接字
bool InitSocket()
{
    WSADATA wsdata={0};
    return !WSAStartup(MAKEWORD(2,2),&wsdata);
}
//解析TCP头部
void DecodeTcpPacket(char *pData)
{
    TCP_HEADER *pTcp;
    pTcp=(TCP_HEADER *)pData;
    printf("端口:%d\n",ntohs(pTcp->th_sport));
}
//解码IP头部
void DecodeIpPacket(char *pData)
{
    IP_HEADER *pIp;
    in_addr Sip,Dip;
    char szDip[32]={0},szSip[32]={0};
    pIp = (IP_HEADER *)pData;
    Sip.S_un.S_addr = pIp->sourceIP;
    Dip.S_un.S_addr=pIp->destIP;
    strcpy(szDip,inet_ntoa(Dip));
    strcpy(szSip,inet_ntoa(Sip));
    printf("源IP：%s\n目标IP:%s\n",szSip,szDip);
    switch (pIp->proto)
    {
    case IPPROTO_TCP:
        printf("协议:TCP\n");
        DecodeTcpPacket(&pData[sizeof(TCP_HEADER)]);
        break;
    case IPPROTO_UDP:
        printf("协议:UDP\n");
        break;
    case  IPPROTO_ICMP:
        printf("协议:ICMP\n");
        break;
    default:
        break;
    }
}
//////////////////////////////////////////////////////////////////////////
int _tmain(int argc, _TCHAR* argv[])
{
    if (!InitSocket())
    {
        printf("初始化Socket库失败!\n");
        getchar();
    }
    /////   变量      /////
    SOCKET  sock;
    SOCKADDR_IN SourceAddr={0};        //源地址
    char HostName[MAX_PATH]={0};   //主机名
    char DataBuffer[1024]={0};     //数据缓冲区
    ////    代码      ////
    sock=socket(AF_INET,SOCK_RAW,IPPROTO_IP);
    if(sock==INVALID_SOCKET)
    {
        printf("创建套接字失败!\n");
        getchar();
    }
    if(SOCKET_ERROR==gethostname(HostName,sizeof(HostName)))
    {
herr:
 
        printf("获取主机名失败!\n");
        closesocket(sock);
        getchar();
    }
    printf("主机名:%s\n",HostName);
    HOSTENT *host=gethostbyname(HostName);
    if(!host)goto herr;
    memcpy(&SourceAddr.sin_addr.S_un.S_addr,host->h_addr_list[0],host->h_length);
    SourceAddr.sin_port=0;
    SourceAddr.sin_family=AF_INET;
    //打印主机IP
    printf("IP:%s\n",inet_ntoa(SourceAddr.sin_addr));
    //绑定
    if(SOCKET_ERROR==bind(sock,(PSOCKADDR)&SourceAddr,sizeof(SOCKADDR_IN)))
    {
        printf("绑定失败!\n");
        closesocket(sock);
        getchar();
    }
    //// 设置混杂模式
    DWORD dw=1;
    if(ioctlsocket(sock,SIO_RCVALL,&dw)!=0)
    {
        printf("设置混杂模式失败!\n");
        closesocket(sock);
        getchar();
    }
 
    while (true)
    {
        DWORD DataLen;
        DataLen=recv(sock,DataBuffer,1024,0);
        if (DataLen>0)
        {
            printf("------------------------------------\n");
            DecodeIpPacket(DataBuffer);
        }
    }
 
    return 0;
}