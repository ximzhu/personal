/*
 * Copyright(c) 2018 Ruijie Network. All rights reserved.
 */
/*
 * check_memory_leak.c
 * original Author: zhuximin@ruijie.com.cn, 2018-5-8
 *
 * Check to see if there is a memory leak problem caused
 * by the improper use of applying for memory.
 *
 * History
 *
 */

#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <errno.h>

#define DEFAULT_FILE     "http_record.c"    /* The default filename of C file for checking */
#define DEFAULT_FUNC     "malloc"           /* The default check for resource leaks for malloc() */
#define MAX_NUM_LINE     100                /* Maximum length of a line of code */
#define LEN_BRACKETS     2                  /* The length of a pair of brackets */
#define LEN_SEMICOLON    1                  /* The length of semicolon */

static int is_annotat(char *buffer)
{
    int index;
    int flag_comment;
    int flag_tmp;

    flag_tmp = 0;
    flag_comment = 0;
    for(index = 0; index < strlen(buffer) - 1; index++) {
        if ((buffer[index] == '/') && (buffer[index + 1 == '*'])) {
            flag_tmp = 1;
            break;
        } else if ((buffer[index] == '*') && (buffer[index + 1] == '/')){
            flag_comment = 1;
            return flag_comment;
        }

    }

    if (flag_tmp) {
        while (index < (strlen(buffer) -1 )) {
            if ((buffer[index] == '*') && (buffer[index + 1] == '/')) {
                flag_comment = 2;
                printf("flag_tmp = 2\n");
                return flag_comment;
            }
            index++;
        }

        flag_comment = 1;
    }

    return flag_comment;
}

static bool is_func(char *buffer, char *func_name, int line)
{
    char *ptr_tmp;
    int col;
    int flag_func_name;
    int flag_brackets;

    ptr_tmp = buffer;
    flag_func_name = 0;
    col = 0;
    while (*(ptr_tmp + strlen(func_name) + LEN_BRACKETS + LEN_SEMICOLON) != '\n') {
        /* function name matching */
        if (strncmp(ptr_tmp, func_name, strlen(func_name)) == 0) {
            flag_func_name = 1;
            printf("line is %d\n", line);
        }
        ptr_tmp++;
        col++;

        if (flag_func_name) {
            printf("line is %d\n", line);
        }
    }

    return false;
}

static bool is_memory_leak(FILE *fp, char *func_name)
{
    int annotat;
    char buffer[MAX_NUM_LINE];
    int line;
    int ret;

    annotat = 0;
    line = 0;
    while (fgets(buffer, MAX_NUM_LINE, fp) != NULL) {
        line++;
        /* ignore comment in the code */
        ret = is_annotat(buffer);
        if (ret == 1) {
            annotat++;
            printf("annotat is %d\n", annotat);
            printf("%s", buffer);
            continue;
        } else if (ret == 2) {
            printf("%s", buffer);
            continue;
        }
        /* ignore comments in the code */
        if ((annotat % 2) != 0) {
            printf("%s", buffer);
            continue;
        }

        if (is_func(buffer, func_name, line)) {
            printf("\n");
        }

        /* XXX : wait for pefect */
    }
}

int main(int argc, char *argv[])
{
    FILE *fp;
    char *func_name;

    fp = fopen(DEFAULT_FILE, "r");
    if (fp == NULL) {
        printf("open the C file failed: %s\n", strerror(errno));
        return -1;
    }

    func_name = DEFAULT_FUNC;
    
    if (is_memory_leak(fp, func_name)) {
        printf("warning!\n");
    }

    fclose(fp);

    return 0;
}
