# This image can be used for running setup.sh if you do not have
# a Linux host with openssl and Python 3 installed.
FROM python:3.9

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    uuid-runtime \
    zip && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /setup/

RUN python3 -m pip install -U pip && python3 -m pip install -r /setup/requirements.txt

COPY . /setup/

# Map the /output directory to the top-level directory of the repository
# to get the generated data at the right places, such as in
#
#     $ docker run --rm -it -v ${PWD}:/output thesetupimage
#
RUN mkdir -p /output

WORKDIR /output
USER 1000
CMD ["/setup/create_files.sh",  "/setup/setup.conf"]

