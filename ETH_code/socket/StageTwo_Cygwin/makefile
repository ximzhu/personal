# Makefile for cygwin gcc
#PCAP_LIB_PATH = driver/win/Lib
#PCAP_PATH = driver/win/Include
#LIBS = -L ${PCAP_LIB_PATH} -lwpcap
#ELF := test
#SRC := check_qq_online.c
#OBJ := $(SRC:%.c=%.o)
#EXTRA_CFLAGS = -g -Wall -I ${PCAP_PATH} -I ./
#LDFLAGS += 
#
#.PHONY:$(OBJ) $(ELF) clean
#$(OBJ):
#	gcc -o $(OBJ) $(SRC) -I$(PCAP_PATH) -I./ -L $(PCAP_LIB_PATH) -lwpcap
#$(ELF): $(OBJ)
##gcc $^ -o $@ $(LDFLAGS) $(LIBS) $(EXTRA_CFLAGS)
#	gcc $^ -o $@ -g -Wall -I$(PCAP_PATH) -I./ -L $(PCAP_LIB_PATH) -lwpcap 
#
#clean:
#	@-rm -rf ${OBJ} ${ELF}
PCAP_PATH = driver/win/lib
CFLAGS = -g -Wall -I driver/win/include -I ./
LIBS = -L ${PCAP_PATH} -lwpcap
TEST_CFILE = check_qq_online.c

all:
	gcc ${CFLAGS} $(TEST_CFILE) -o test ${LIBS}

clean:
	rm -f *.o test
