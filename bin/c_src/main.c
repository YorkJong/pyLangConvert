/**
 * @file main.c
 *      Unit test of the mlang module
 * @author Jiang Yu-Kuan, yukuan.jiang@gmail.com
 * @version 1.0
 * @date 2012/12/03 (initial version)
 * @date 2012/12/03 (last revision)
 */
#include <stdio.h>

#include "mlang.h"


int main(int argc, const char * argv[])
{
    Char *str;
    size_t len;
    int i;

    ML_setLang(L_English);
    ML_getMsgStr(MSG_English, &str, &len);
    printf("len: %d\n", (int)len);
    printf("str: ");
    for (i=0; i<len; ++i) {
        printf("%d,", str[i]);
    }
    printf("\n");

    return 0;
}

