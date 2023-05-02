#!/bin/bash

SCRIPT_DIR=$(dirname $(realpath -e $0))

PRIVATE_KEY=secret.key
PUBLIC_KEY=public.key

function exit_script()
{
    local exit_code=$1
    local msg="$2"
    [ -z "${msg}" ] || echo "${msg}"
    exit $((exit_code))
}


# Generate a private ED25519 key seed.
openssl genpkey -algorithm ED25519 -outform DER -out ${PRIVATE_KEY}.der || \
    exit_script 1 "Error in creation of private key seed. Aborting."

# Get the corresponding public key
openssl pkey -pubout -in ${PRIVATE_KEY}.der -inform DER -outform DER -out ${PUBLIC_KEY}.der || \
    exit_script 1 "Error in extraction of public key. Aborting."

# Extract the actual keys.
(tail -c 32 ${PRIVATE_KEY}.der > ${PRIVATE_KEY} && \
    tail -c 32 ${PUBLIC_KEY}.der > ${PUBLIC_KEY}) || \
    exit_script "Error in key extraction. Aborting."

# Call the Onion service file generator.
(python3 ${SCRIPT_DIR}/onionfiles.py -s ${PRIVATE_KEY} -p ${PUBLIC_KEY} && \
    rm -f ${PRIVATE_KEY} ${PRIVATE_KEY}.der ${PUBLIC_KEY} ${PUBLIC_KEY}.der) || \
    exit_script 1 "Error in creation of Onion service files and removal of temporary files. Aborting."

exit_script

