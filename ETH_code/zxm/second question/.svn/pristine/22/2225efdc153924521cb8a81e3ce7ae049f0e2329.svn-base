http:http_mingw.o
	gcc -Wall -fprofile-arcs -ftest-coverage -o http http_mingw.o -lwsock32 -lws2_32

http_mingw.o:http_mingw.c
	gcc -Wall -fprofile-arcs -ftest-coverage -c http_mingw.c -lwsock32 -lws2_32
