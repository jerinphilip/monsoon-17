
sort: dtype.h bufio.h io.h main.cpp
	g++ main.cpp -o sort -g

test: sort
	./sort meta.txt input.txt output.txt 50 asc c0

debug:
	valgrind ./sort meta.txt input.txt output.txt asc c0

all: sort test
