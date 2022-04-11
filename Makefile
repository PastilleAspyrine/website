

all: clear compile upload gitupload


clear:
	- rm -r out/*

compile: clear
	./compile.py


upload:
	rsync --delete --recursive --compress --progress --partial --update --rsh 'ssh -p $(PORT)' out/* $(USER)@$(SERVER):$(DEST_PATH)

gitupload:
	git push
