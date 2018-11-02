/*
 * Copyright(C) 2017 Ruijie Network. All rights reserved.
 * server.c
 * Original Author:  zhuximin@ruijie.com.cn, 2017-10-24
 *
 * 一、socket套接字编程：
 * 主函数中：
 * 1.socket创建
 * 2.端口重用
 * 3.地址端口绑定函数bind
 * 4.监听端口listen
 * 5.接受网络请求函数accept				   
 * 二、想要获取目录下文件的详细信息要怎么做：
 * 比如a目录下b文件的详细信息：
 * 1.使用Opendir()函数打开目录a，返回指向目录a的DIR结构体c;
 * 2.调用readdir(c)函数读取目录a下所有的文件包括目录，返回指向a下所有文件的dirent结构体d；
 * 3.遍历d，调用stat(d->name,stst *e)来获取每个文件的详细信息，存储在stst结构体e中；
 * 
 * History
 *  v1.1   zhuximin@ruijie.com.cn        2017-10-27
 *         1.减少了exit的使用，减小资源泄露的可能性
 *         2.删除了damen_y_n标志变量的使用
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h> 
#include <fcntl.h>                               /* open()函数头文件 */
#include <getopt.h>                              /* getopt_long函数头文件*/
#include <stdarg.h>                              /* 处理可变参数函数头文件 */
#include <time.h>                                /* 时间相关函数头文件 */

#define DEFAULTIP   "127.0.0.1"                  /* host对应参数 */
#define DEFAULTPORT "80"                         /* port对应参数 */
#define DEFAULTBACK "10"                         /* back对应参数 */
#define DEFAULTDIR  "/home"                      /* dirroot对应参数 */

#define MAXBUF        1024                       /* 字符串数组buffer最大长度 */
#define MAXPATH       150                        /* 目录和文件最大长度 */
#define MAXSIZE       10                         /* option结构体数组最大长度 */

struct option long_options[MAXSIZE];                                                      /*搞定局部变量*/

static char *host = 0;
static char *port = 0;
static char *back = 0;
static char *dirroot = 0;

/*
 * 查找dirpath所指目录的上一级目录
 */
char *dir_up(char *dirpath)
{
    static char path[MAXPATH];                   /* 存放上级目录的字符数组 */
	int len;                                     /* 目录长度 */
    
	strcpy(path, dirpath);	
	if (path == NULL) {
		perror("复制失败");
	}
	len = strlen(path);
	if (len > 1 && path[len - 1] == '/') {
        len--;
	}
    while (path[len - 1] != '/' && len > 1) {
        len--;
	}
    path[len] = 0;
    
	return path;
}

/*
 * response()函数:把Path所指的内容发送到client_sock去,
 * 如果Path是一个目录，则列出目录内容;
 * 如果Path是一个文件，则下载文件 
 */
void response(FILE * client_sock, char *path)
{
    struct dirent *dirent;
	struct stat info;
	DIR *dir;
	char filename[MAXPATH];                      /* 存放文件名的字符数组 */
	int fd;                                      /* 文件描述符 */
	int len_dir;                                 /* 目录或者文件名长度 */
	int len_port;                                /* 端口长度 */
	int len_file;                                /* 文件内容长度 */
	char *p;                                     /* 文件指针 */
	char *realpath;                              /* 实际工作目录或文件名 */
	char *realfilename;                          /* 实际文件名 */
	char *nport;                                 /* 实际工作端口 */
    
	/* 获得实际工作目录或文件名 */
    len_dir = strlen(dirroot) + strlen(path) + 1;
	realpath =(char *) malloc(len_dir + 1);
	if (realpath == NULL) {
		(void)printf("申请内存失败\n");
		return ;
	}
	bzero(realpath, len_dir + 1);                
	(void)sprintf(realpath, "%s/%s", dirroot, path);

    /* 获得实际工作端口 */
    len_port = strlen(port) + 1;
	nport = (char *)malloc(len_port + 1);
	if (nport == NULL) {
		(void)printf("申请内存失败\n");
		return ;
	}
	bzero(nport, len_port + 1);
	(void)sprintf(nport, ":%s", port);

    /* 获得实际工作目录或文件名的信息以判断是文件还是目录 */
    if (stat(realpath, &info)) {
        (void)fprintf(client_sock,
                "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n<html><head><title>%d - %s</title>"
				"</head><table >", errno,strerror(errno));
        goto out;
    }

    /* 处理浏览文件请求，即下载文件 */
    if (S_ISREG(info.st_mode)) {
		fd = open(realpath, O_RDONLY);
		if (fd<0) {
			(void)printf("打开文件失败\n");
		}
		len_file = lseek(fd, 0, SEEK_END);
		p = (char *) malloc(len_file + 1); 
		if (p == NULL) {
			(void)printf("申请内存失败\n");
			return ;
		}
		bzero(p, len_file + 1);
		(void)lseek(fd, 0, SEEK_SET);
		(void)close(fd);
		(void)fprintf(client_sock,
                "HTTP/1.1 200 OK\r\nConnection: keep-alive\r\nContent-type: application/*\r\n"
				"Content-Length:%d\r\n\r\n",len_file);
		fwrite(p, len_file, 1, client_sock);
		free(p);
		p=NULL;
    } else if (S_ISDIR(info.st_mode)){
        /* 处理浏览目录请求 */
        dir = opendir(realpath);
		(void)fprintf(client_sock,
                "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n<html><head><title>%s</title>"
				"</head><table >", path);
		(void)fprintf(client_sock,
                "<caption><font size=+3>DIR %s</font></caption>\n",
                path);
		/* 文件排版内容显示说明 */
		(void)fprintf(client_sock,
                "<tr><td>File Name</td><td> Size </td><td> Date </td></tr>\n");
        
        /* 读取目录里的所有内容 */
        while ((dirent = readdir(dir)) != 0) {
            if (strcmp(path, "/") == 0) {
                (void)sprintf(filename, "/%s", dirent->d_name);
			} else {
                (void)sprintf(filename, "%s/%s", path, dirent->d_name);
			}
            
			(void)fprintf(client_sock, "<tr>");
			len_dir = strlen(dirroot) + strlen(filename) + 1;
			realfilename =(char *) malloc(len_dir + 1);
			if (realfilename == NULL) {
				(void)printf("申请内存失败\n");
				return ;
			}
			bzero(realfilename, len_dir + 1);
			(void)sprintf(realfilename, "%s/%s", dirroot, filename);
            
			if (stat(realfilename, &info) == 0) {
                if (strcmp(dirent->d_name, "..") == 0) {
					/* 使用超链接(back)返回上级目录 */
                    (void)fprintf(client_sock,
                            "<td><a href=\"http://%s%s%s\">(back)</a></td>",
                            host, atoi(port) == 80 ? "" : nport,
                            dir_up(path));
				} else {
					/* 使用超链接获取目录下所有文件名 */
                    (void)fprintf(client_sock,
                            "<td><a href=\"http://%s%s%s\">%s</a></td>",
                            host, atoi(port) == 80 ? "" : nport, filename,
                            dirent->d_name);
				}

				/* 使用stat中st_mode来判断文件类型 */
                if (S_ISDIR(info.st_mode)) {
                    (void)fprintf(client_sock, "<td>DIR</td>");
				} else if (S_ISREG(info.st_mode)) {
                    (void)fprintf(client_sock, "<td>%ldB</td>",info.st_size);
				} else if (S_ISLNK(info.st_mode)) {
                    (void)fprintf(client_sock, "<td>LINK</td>");
				} else if (S_ISCHR(info.st_mode)) {
                    (void)fprintf(client_sock, "<td>CHARDEVICE</td>");
				} else if (S_ISBLK(info.st_mode)) {
                    (void)fprintf(client_sock, "<td>PIECE</td>");
				} else if (S_ISFIFO(info.st_mode)) {
                    (void)fprintf(client_sock, "<td>FIFO</td>");
				} else if (S_ISSOCK(info.st_mode)){
                    (void)fprintf(client_sock, "<td>Socket</td>");
				} else {
                    (void)fprintf(client_sock, "<td>(UNKNOW)</td>");
				}
				
				/* 时间输出设置 */
                (void)fprintf(client_sock, "<td>%s</td>", ctime(&info.st_ctime));
            } /* end if */
            
			(void)fprintf(client_sock, "</tr>\n");
			free(realfilename);
			realfilename=NULL;
        } /* end while */
        
		(void)fprintf(client_sock, "</table></body></html>");
    } else {
        /* 非正确情况，禁止访问 */
        (void)fprintf(client_sock,
                "HTTP/1.1 200 OK\r\nConnection: close\r\n\r\n<html><head><title>permission denied"
				"</title></head><table>");
    } /* end if */
    
	out:
	free(realpath);
	realpath=NULL;
	free(nport);
	nport=NULL;
}

/*
 * getdata - 分析取出程序的参数
 * --host IP地址 或者 -H IP地址
 * --port 端口 或者 -P 端口
 * --back 监听数量 或者 -B 监听数量
 * --dir 网站根目录 或者 -D 网站根目录
 */
void getdata(int argc, char *argv[])
{
    int c;                                       /* getopt_long函数返回值 */
	int len_opt;                                 /* 程序参数长度 */
	char *p ;                                    /* 程序参数指针 */
	int option_index;                            /* 表示当前长参数在long_options中的索引值 */
	
	while (1) {
		struct option long_options[MAXSIZE]= {
            {"host", 1, 0, 0},
            {"port", 1, 0, 0},
            {"back", 1, 0, 0},
            {"dir", 1, 0, 0},
        };                                       /* 选项字符串，告知getopt_long可以处理那个选项以及哪个选项需要参数 */
	    option_index=0;
		/* 长选项的命令解析,解析完成时返回-1 */
		c = getopt_long(argc, argv, "H:P:B:D:L",long_options, &option_index);  
		if (c == -1 || c == '?') {
            break;                               /* 解析完成退出 */
		}

        if(optarg) {                             /* optarg是选项的参数指针 */
			len_opt = strlen(optarg);
		} else {
			len_opt = 0;
		}

        if ((!c && !(strcasecmp (long_options[option_index].name, "host")))
			    || c == 'H') {
            p = (char *)malloc(len_opt + 1);
			if (p == NULL) {
				(void)printf("申请内存失败\n");
			    return ;
		    }
			p = host;
		} else if ((!c && !(strcasecmp (long_options[option_index].name, "port")))
                       || c == 'P') {
            p = port = malloc(len_opt + 1);
			if (p == NULL) {
				(void)printf("申请内存失败\n");
				return ;
		    }
		} else if ((!c && !(strcasecmp (long_options[option_index].name, "back")))
                       || c == 'B') {
            p = back = malloc(len_opt + 1);
			if (p == NULL) {
				(void)printf("申请内存失败\n");
				return ;
			}
		} else if ((!c && !(strcasecmp (long_options[option_index].name, "dir")))
                       || c == 'D') {
            p = dirroot = malloc(len_opt + 1);
			if (p == NULL) {
				(void)printf("申请内存失败\n");
				return ;
		    }
		} else {
            break;
		}
        
		bzero (p, len_opt + 1) ;
		memcpy (p, optarg, len_opt) ;            /* 拷贝optarg所指资源内存到p所指的目标内存 */
    }
}

/*
 * 分配空间并把d所指的内容复制
 */
void content(char *s[], int l, char *d)
{
    *s = malloc(l + 1);
    if (*s == NULL) {
        (void)printf("申请内存失败\n");
	    return ;
	}
	bzero(*s, l + 1);
	memcpy(*s, d, l);                            /* 拷贝d所指资源内存到s所指的目标内存 */
}
 
int main(int argc, char *argv[])
{
    struct sockaddr_in addr;                     /* sockaddr_in结构体包含有sin_family、sin_port、sin_addr等属性 */
	int sock_fd;                                 /* socket套接字描述符 */
	int addrlen;                                 /* 各个参数长度 */
	char buffer[MAXBUF + 1];                     /* 字符串数组buffer */
    int len;
	int new_fd;
	FILE *ClientFP;
	char req[MAXPATH + 1];
	
    getdata(argc, argv);                         /* 获得程序工作基本参数*/
    if (!host) {
        addrlen = strlen(DEFAULTIP);
		content(&host, addrlen, DEFAULTIP);      /* 获取主机号 */
    } 
	if (!port) {
        addrlen = strlen(DEFAULTPORT);
		content(&port, addrlen, DEFAULTPORT);    /* 获取端口号 */
    }
	if (!back) {
        addrlen = strlen(DEFAULTBACK);
		content(&back, addrlen, DEFAULTBACK);    /* 获取监听数量 */
    }
    if (!dirroot) {
        addrlen = strlen(DEFAULTDIR);
		content(&dirroot, addrlen, DEFAULTDIR);  /* 获取显示文件根目录:从DEFAULTDIR也就是/home开始 */
    }
    (void)printf("当前服务器参数为：host=%s port=%s back=%s dirroot=%s \n",
         host, port, back, dirroot);             /* 输出当前服务器参数 */

    /* 创建socket() */
    if ((sock_fd = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
		perror("socket");
    }

    /* 设置端口快速重用，防止一些原因造成socket()创建不成功 */
    addrlen = 1;
	setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &addrlen,sizeof(addrlen));
    addr.sin_family = AF_INET;
	addr.sin_port = htons(atoi(port));
	addr.sin_addr.s_addr = inet_addr(host);
	addrlen = sizeof(struct sockaddr_in);
    
	/* bind()绑定地址、端口等信息 */
    if (bind(sock_fd, (struct sockaddr *) &addr, addrlen) < 0) {
        perror("bind");
    }

    /* listeb()开启临听 */
    if (listen(sock_fd, atoi(back)) < 0) {
        perror("listen");
    }
	
    while (1) {
		addrlen = sizeof(struct sockaddr_in);
		/* 接受新连接请求 */
        new_fd = accept(sock_fd, (struct sockaddr *) &addr, (socklen_t *)&addrlen);
		if (new_fd < 0) {
			perror("accept");
        }
        bzero(buffer, MAXBUF + 1);
        (void)sprintf(buffer, "Connect from : %s:%d\n",
        inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));
		(void)fputs(buffer, stdout);
        
		/* 产生一个子进程去处理请求，当前进程继续等待新的连接到来 */
        if (!fork()) {
            bzero(buffer, MAXBUF + 1);
            
			if ((len = recv(new_fd, buffer, MAXBUF, 0)) > 0) {
                ClientFP = fdopen(new_fd, "w");
                
				if (ClientFP == NULL) {
                    printf("打开文件失败\n");
                } else {
					(void)sscanf(buffer, "GET %s HTTP", req);
					bzero(buffer, MAXBUF + 1);
					(void)sprintf(buffer, "Request for file : \"%s\"\n", req);
					(void)fputs(buffer, stdout);
                    response(ClientFP, req);     /* 处理用户请求 */
					(void)fclose(ClientFP);
                }
            }
        }
        
		(void)close(new_fd);
    }
    
	(void)close(sock_fd);
	return 0;
}
