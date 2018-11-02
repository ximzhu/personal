/*
 * Copyright(C) 2018 Ruijie Network. All rights reserved.
 */
/*
 * unp_server_main.c
 * Original Author:  zhuximin.com.cn, 2018-4-24
 *
 * Displays files in a local directory on the server interface
 * and supports user downloads.
 *
 */

#include "unp_server.h"

int main(int argc, char *argv[])
{
    struct sockaddr_in addr;
    int new_fd;
    int addr_len;
    char buffer[MAXBUF];
    FILE *client_sock;
    char req[MAXPATH];

    host = DEFAULTHOST;
    port = DEFAULTPORT;
    back = DEFAULTBACK;
    dir = DEFAULTDIR;

    get_data(argc, argv);

    printf("The arguments of the server is: host = %s port = %s back = %s dir = %s\n",
        host, port, back, dir);

    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd < 0) {
        printf("Create socket failed :%s\n", strerror(errno));
        free_ptr();
        return -1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(port));
    addr.sin_addr.s_addr = inet_addr(host);

    if (bind(sock_fd, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)) < 0) {
        printf("Bind failed: %s\n", strerror(errno));
        close(sock_fd);
        free_ptr();
        return -1;
    }

    if (listen(sock_fd, atoi(back)) < 0) {
        printf("Listen failed: %s\n", strerror(errno));
        close(sock_fd);
        free_ptr();
        return -1;
    }

    signal(SIGINT, stop_program);
    printf("Build server successful!\n");
    while (1) {
        addr_len = sizeof(struct sockaddr_in);
        new_fd = accept(sock_fd, (struct sockaddr *)&addr,
            (socklen_t *)&addr_len);
        if (new_fd < 0) {
            printf("Accept failed: %s\n", strerror(errno));
            close(sock_fd);
            free_ptr();
            return -1;

        }

        printf("Connect from :%s:%d\n", inet_ntoa(addr.sin_addr), ntohs(addr.sin_port));

        if (recv(new_fd, buffer, MAXBUF, 0) < 0) {
            continue;
        }

        client_sock = fdopen(new_fd, "w");
        if (client_sock == NULL) {
            printf("Failed to open the stream resource: %s\n", strerror(errno));
            continue;
        }

        if (sscanf(buffer, "GET %s HTTP", req) == EOF) {
            printf("Failed to read the requet resource path from the data stream: %s\n",
                strerror(errno));
            continue;
        }
        printf("Request for file : \"%s\"\n", req);

        /* XXX: response(client_sock, req); */
        if (fclose(client_sock) == EOF) {
            printf("Failed to close the stream resource : %s\n", strerror(errno));
            continue;
        }
    }

    return 0;
}

