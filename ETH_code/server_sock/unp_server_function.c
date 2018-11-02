/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * unp_server_function.c
 * Original Author:  zhuximin.com.cn, 2018-4-24
 *
 * Implement the function called in unp_server_main.c file.
 *
 */

#include "unp_server.h"

void get_data(int argc, char *argv[])
{
    int opt;
    int len_opt;
    char *p_tmp;

    if (argc < 2) {
        printf("Use the system default parameters!\n");
        return;
    }

    while ((opt = getopt(argc, argv, "h:p:b:d:")) != EOF) {
        if (optarg == NULL) {
            break;
        } else {
            len_opt = strlen(optarg);
        }

        switch (opt) {
        case 'h':
            host = (char *)malloc(len_opt);
            if (host == NULL) {
                printf("Specify the host parameter failed, and use the default parameter!\n");
                return;
            }
            flag_host = 1;

            p_tmp = host;
            break;
        case 'p':
            port = (char *)malloc(len_opt);
            if (port == NULL) {
                printf("Specify the port parameter failed, and use the default parameter!\n");
                return;
            }
            flag_port = 1;

            p_tmp = port;
            break;
        case 'b':
            back = (char *)malloc(len_opt);
            if (back == NULL) {
                printf("Specify the back parameter failed, and use the default parameter!\n");
                return;
            }
            flag_back = 1;

            p_tmp = back;
            break;
        case 'd':
            dir = (char *)malloc(len_opt);
            if (dir == NULL) {
                printf("Specify the dir parameter failed, and use the default parameter!\n");
                return;
            }
            flag_dir = 1;

            p_tmp = dir;
            break;
        default:
            break;
        }/* end for switch */

        bzero(p_tmp, len_opt);
        memmove(p_tmp, optarg, len_opt);
    }/* end for while */

    p_tmp = NULL;
}

void free_ptr(void)
{
    if (flag_host) {
        free(host);
    }

    if (flag_port) {
        free(port);
    }

    if (flag_back) {
        free(back);
    }

    if (flag_dir) {
        free(dir);
    }
}

void stop_program(int signo)
{
    free_ptr();
    printf("The program is forced to terminate.\n");
    exit(0);
}
