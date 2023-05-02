#!/bin/bash

SCRIPT_NAME=$(basename $0)
SCRIPT_DIR=$(dirname $(realpath -e $0))

FLAGFILE=${SCRIPT_DIR}/flag.txt

FLAGVALUE_FILE=xXx


function exit_script()
{
    local exit_code=$1
    local msg="$2"
    [ -z "${msg}" ] || echo "${msg}"
    exit $((exit_code))
}


function exit_with_usage()
{
    local exit_code=$1
    local msg="$2"
    [ -z "${msg}" ] || echo -e "${msg}\n"
    echo
    echo 'Usage:'
    echo "  $ ${SCRIPT_NAME} <zip file code> <output filename>"
    echo
    echo 'Output:'
    echo '  - The encrypted file, containing the flag value.'
    echo
    exit $((exit_code))
}

[ $# -eq 2 ] || exit_with_usage 2

ZIPCODE="$1"
OUTPUT_FILE="$2"
# echo -e "Not the flag\nThis neither\nHere comes the flag>${flag_value}<\nBack to uninteresting data\n" > flag && \

NOT_THE_FLAG_FILE=use_the_zip_code

(rm -f ${FLAGVALUE_FILE} ${NOT_THE_FLAG_FILE} ${OUTPUT_FILE}  && \
    echo 'This is the flag' > ${FLAGVALUE_FILE} && \
    grep '^undut' ${FLAGFILE} | sed -e 's/^.*undut{\([^}]\+\)}.*$/\1/' | head -n 1 >> ${FLAGVALUE_FILE} && \
    echo 'This file does not contain the flag.' >  ${NOT_THE_FLAG_FILE} &&
    tr -dc A-Za-z0-9 </dev/urandom | head -c 64 >> ${NOT_THE_FLAG_FILE} && \
    zip --quiet --password "${ZIPCODE}" ${OUTPUT_FILE} ${NOT_THE_FLAG_FILE} ${FLAGVALUE_FILE} && \
    rm -f ${FLAGVALUE_FILE} ${NOT_THE_FLAG_FILE} && \
    [ -e ${OUTPUT_FILE} ] ) || \
    exit_script 1 "Unable to create file ${OUTPUT_FILE}"

exit_script

