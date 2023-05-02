FROM docker.io/python:slim AS app

# https://github.com/redpwn/jail
FROM localhost/challs/redjail:latest
COPY --from=app / /srv
COPY ./container/2x_shuffle.py /srv/app/run
COPY ./container/flag.txt /srv/app/flag.txt
RUN chmod -R 555 /srv/app/
ENV JAIL_MEM=20M JAIL_TIME=600 JAIL_CONNS_PER_IP=10 JAIL_PORT=1337
