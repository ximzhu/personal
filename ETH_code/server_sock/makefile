CFLAG=-Wall
TARGET=server
LIBS=-lm

server : unp_server_main.o unp_server_function.o
	gcc $(CFLAG) -o $(TARGET) unp_server_main.o unp_server_function.o $(LIBS)

unp_server_main.o : unp_server.h unp_server_main.c
	gcc -c unp_server_main.c $(LIBS)

unp_server_function.o : unp_server.h unp_server_function.c
	gcc -c unp_server_function.c $(LIBS)

