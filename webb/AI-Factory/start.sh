#!/bin/bash
app="ml_ctf"

sudo docker build -t ${app} .

sudo docker run -it -p --rm 8501:8501 --name=${app} ${app}
