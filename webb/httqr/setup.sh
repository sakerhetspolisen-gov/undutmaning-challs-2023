#!/bin/bash

SCRIPT_NAME=$(basename $0)
SCRIPT_DIR=$(dirname $(realpath -e $0))

ARG1="$1"

function exit_script()
{
    local exit_code=$1
    local msg="$2"
    [ -z "${msg}" ] || echo "${msg}"
    exit $((exit_code))
}

if [ "x${ARG1}" == 'xclean' ]
then
    read -s -p 'Removing previously created files (Enter to continue, ctrl-C to abort)'
    echo
    rm -rf tor/services/ webserver/ssl/ webserver/flags/
    exit_script $?
fi


(cd ${SCRIPT_DIR} && \
    cp ${SCRIPT_DIR}/flag.txt ${SCRIPT_DIR}/bin/ && \
    docker build -t httqr-setup ./bin/ && \
    rm ${SCRIPT_DIR}/bin/flag.txt && \
    docker run --rm -it -v ${SCRIPT_DIR}:/output httqr-setup) || \
    exit_script 1 'Failure in running setup container. Aborting.'

exit_script

