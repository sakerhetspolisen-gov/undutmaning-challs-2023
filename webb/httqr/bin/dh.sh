#!/bin/bash

while ! timeout -s INT 60s openssl dhparam -out dhparam.pem 2048
do
    echo 'Retrying'
done

