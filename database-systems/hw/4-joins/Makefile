CC=g++
CFLAGS=--std=c++14

.PHONY: clean all

sort_test: test_sorter.cpp sort.hpp buffer.hpp
	$(CC) $(CFLAGS) test_sorter.cpp -o test_sorter
	./test_sorter input/R input/R.sorted
	./test_sorter input/S input/S.sorted

join_test: sort_test join.hpp
	$(CC) $(CFLAGS) test_join.cpp -o test_join
	./test_join input/R input/S


clean:
	rm -rf intermediates/*
	rm test_join
	rm test_sorter
