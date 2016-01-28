###########################################################
# Makefile composed by Jiang Yu-Kuan 2016/1/29
# Platform: ANSI C / GCC enviroment
# Purpose: Test the generacted files of LangConvert

CC = gcc

PROG = mlang_test
OBJS = main.o mlang.o

W0 = -Wall -Wextra -pedantic -Wdeclaration-after-statement -Wundef -Wwrite-strings
W1 = -Wbad-function-cast -Wcast-qual -Wredundant-decls #-Wunreachable-code
W2 = -Wno-unused-local-typedefs
CFLAGS = -std=c99 -DDEBUG $(W0)

$(PROG): $(OBJS)
	$(CC) -o $@ $(CFLAGS) $(OBJS)

.SUFFIXES: .c .o
.c.o:
	$(CC) -c $< $(CFLAGS)

.PHONY : cleanobj cleanbin clean
cleanobj:
	rm -f *.o
cleanbin:
	rm -f *.exe
clean: cleanobj cleanbin
