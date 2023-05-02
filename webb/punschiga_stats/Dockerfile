FROM docker.io/python:3.9.2-alpine

COPY requirements.txt /requirements.txt

RUN apk update && apk upgrade && apk add build-base libffi-dev && rm -rf /var/cache/apk/*
RUN pip install -r /requirements.txt

WORKDIR /app
ADD app /app
RUN chmod -R a-w /app
RUN adduser -D appuser
USER appuser
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
