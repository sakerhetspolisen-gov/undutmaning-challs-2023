FROM ubuntu
RUN apt update
RUN apt install -y python3 xinetd

RUN groupadd -g 1337 ctf
RUN useradd -r -u 1337 -g ctf ctf
RUN mkdir -p /home/ctf

COPY 2x_shuffle.py /home/ctf/
COPY flag.txt /home/ctf
COPY xinetd_config /etc/xinetd.d/

RUN chown -R root:ctf /home/ctf/
RUN chmod -R 555 /home/ctf/

WORKDIR /home/ctf/
CMD xinetd -dontfork