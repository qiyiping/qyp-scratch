CXX=g++
CC=gcc
CFLAGS=-O3

all: solver pymodule

two_bottle_puzzle.o: two_bottle_puzzle.c two_bottle_puzzle.h
	$(CC) $(CFLAGS) -Wall -c two_bottle_puzzle.c -o two_bottle_puzzle.o

solver: main.c two_bottle_puzzle.o
	$(CC) $(CFLAGS) -Wall main.c two_bottle_puzzle.o -o solver

pymodule: two_bottle_puzzle.o puzzle.cc
	$(CXX) $(CFLAGS) -Wall -shared -std=c++11 -undefined dynamic_lookup -fPIC `python -m pybind11 --includes` puzzle.cc two_bottle_puzzle.o -o puzzle.so

clean:
	rm solver two_bottle_puzzle.o puzzle.so

