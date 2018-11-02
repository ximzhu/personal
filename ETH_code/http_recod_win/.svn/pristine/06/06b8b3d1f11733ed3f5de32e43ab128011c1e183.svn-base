CFLAGS=-Wall -g -fprofile-arcs -ftest-coverage  -D_STUB_OPEN_
CFLAG=-Wall
LIBS=-lws2_32
TARGET=http.exe

all:http_record.c stub.c
	gcc $(CFLAGS) -o $(TARGET) $^ $(LIBS)

release:http_record.c stub.c
	gcc $(CFLAG) -o $(TARGET) $^ $(LIBS)

gcov:
	gcov -b -f http_record.c
	gcov -b -f stub.c

.PHONY:clean
clean:
	rm -rf *.o http_record *.g*