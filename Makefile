

all: clear compile upload


clear:
	- rm -r out/*

compile: clear
	./compile.py
