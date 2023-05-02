FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
RUN apt update -y && apt install -y wine wget xxd
RUN wine cmd.exe /c dir

RUN wget https://go.dev/dl/go1.19.5.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.5.linux-amd64.tar.gz
ENV PATH $PATH:/usr/local/go/bin

RUN mkdir ~/Downloads
WORKDIR /root/Downloads
RUN wget http://gnu.mirrors.hoobly.com/emacs/windows/emacs-28/emacs-28.2-installer.exe

WORKDIR /code
