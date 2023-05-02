FROM nginx:1.23.3-alpine-slim

WORKDIR /var/www/html

RUN apk update && apk upgrade --no-cache

RUN apk add --no-cache curl nginx php81 php81-fpm php81-intl php81-opcache php81-sqlite3 php81-json supervisor


COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/fpm-pool.conf /etc/php81/php-fpm.d/www.conf
COPY config/php.ini /etc/php81/conf.d/custom.ini
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chown -R nobody.nobody /var/www/html /run /var/log/nginx

USER nobody

COPY --chown=nobody src/ /var/www/html/
RUN chmod -R a-w /var/www/html

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

HEALTHCHECK --timeout=15s CMD curl --silent --fail http://127.0.0.1:8080/ping-health
