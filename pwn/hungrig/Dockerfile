FROM docker.io/python:slim AS compile
RUN apt update && apt upgrade
RUN apt install binutils-x86-64-linux-gnu binutils build-essential -y
RUN pip install --no-cache-dir pwntools
COPY create_hungrig.py /work/create_hungrig.py
WORKDIR /work
RUN python /work/create_hungrig.py

FROM docker.io/python:slim as app
# https://github.com/redpwn/jail
FROM localhost/challs/redjail:latest
COPY --from=app / /srv
COPY --from=compile /work/hungrig /srv/app/run
COPY ./flag.txt /srv/app/flag.txt
RUN chmod -R 555 /srv/app/
ENV JAIL_MEM=20M JAIL_TIME=600 JAIL_CONNS_PER_IP=10 JAIL_PORT=
