FROM nginx

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    supervisor && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -U pip
RUN python3 -m pip install uvicorn[standard]

COPY supervisor/ /etc/supervisor/conf.d/
COPY uvicorn/ /etc/uvicorn/
COPY bin/ /usr/local/bin/

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
WORKDIR /etc/nginx
SHELL ["/bin/bash", "-c"]

RUN rm -rf /etc/nginx/conf.d
COPY nginx/ /etc/nginx/

COPY src/requirements.txt /webapp/src/
RUN python3 -m pip install -r /webapp/src/requirements.txt

COPY ssl/ /etc/nginx/ssl/
COPY flags/ /bravo/flags/
COPY templates/common/ /alpha/templates/
COPY templates/alpha/ /alpha/templates/
COPY templates/common/ /bravo/templates/
COPY templates/bravo/ /bravo/templates/
COPY src/ /webapp/src/
RUN cd /webapp/src && python3 setup.py install

