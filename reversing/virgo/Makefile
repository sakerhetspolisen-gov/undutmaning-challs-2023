DOCKER_IMAGE=packad-image
RUN_IN_DOCKER=docker run --rm --name packad-container -v $(realpath .):/code $(DOCKER_IMAGE)

.PHONY: all
all: recept.doc.exe

.PHONY: run
run: recept.doc.exe
	$(RUN_IN_DOCKER) ./run.sh


.PHONY: $(DOCKER_IMAGE)
$(DOCKER_IMAGE): Dockerfile
	docker build -t $@ .

settings.go: $(DOCKER_IMAGE)
	$(RUN_IN_DOCKER) bash -c 'cat ~/Downloads/emacs-28.2-installer.exe | xxd -i -s 1337 -l 16 -c 1000 | python3 create-settings-go.py flag.txt'

recept.doc.exe: vir.go settings.go $(DOCKER_IMAGE)
	$(RUN_IN_DOCKER) bash -c 'export GOOS=windows; export GOARCH=amd64; go build -ldflags "-s -w" -trimpath vir.go settings.go'
	mv vir.exe $@

.PHONY: clean
clean:
	rm -rf recept.doc.exe
