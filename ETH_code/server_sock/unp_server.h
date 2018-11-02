/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * unp_server.h
 * Original Author:  zhuximin.com.cn, 2018-4-24
 *
 * The header file of unp_server_function.c file ,The related
 * header files are included,and defines the command line op-
 * -tion parameters used by the program as global variables.
 *
 */

/* unp_server.h */

#ifndef _UNP_SERVER_H_
#define _UNP_SERVER_H_

#include <stdio.h>
#include <unistd.h>
#include <getopt.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <stdbool.h>
#include <errno.h>
#include <signal.h>

#define DEFAULTHOST "127.0.0.1"    /* IP address of server */
#define DEFAULTPORT "80"           /* port of server */
#define DEFAULTBACK "10"           /* maximum number of client connections */
#define DEFAULTDIR "/home"         /* the path to display the contents
                                      of the current host */
#define MAXSIZE 4                  /* the maximum number of the comma-
                                      -nd-line argumrnts */
#define MAXBUF 50                  /* connect address information */
#define MAXPATH 100

char *host;                        /* pointer to host */
char *port;                        /* pointer to port */
char *back;                        /* pointer to back */
char *dir;                         /* pointer to dir */

/* determines whether the parameter is specified */
int flag_host;
int flag_port;
int flag_back;
int flag_dir;

int sock_fd;    /* the socket of server */

void get_data(int argc, char *argv[]);
void free_ptr(void);
void stop_program(int signo);
void response(FILE *client_sock, char *req);

#endif /* _UNP_SERVER_H_ */
