FROM alpine:3.15

RUN apk update && apk add tor
COPY conf/ /etc/tor/
COPY services/ /tor/svcs/
RUN chmod 700 /tor/svcs/* && chown -R tor /tor/svcs
USER tor
CMD ["tor", "-f", "/etc/tor/torrc"]

