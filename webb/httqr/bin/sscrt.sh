#!/bin/bash

SCRIPT_NAME=$(basename $0)

function exit_script()
{
    local exit_code=$1
    local msg="$2"
    [ -z "${msg}" ] || echo "${msg}"
    exit $((exit_code))
}

function usage()
{
    echo
    echo 'Usage:'
    echo '  $ export ZIP_CODE'
    echo '  $ export GITHUB_USER'
    echo '  $ export GITHUB_REPO'
    echo "  $ ${SCRIPT_NAME} <main-domain-name> {<alt-domain-name>}"
    echo
    echo 'Output'
    echo '  the.key  - The (private) key matching the certificate.'
    echo '  the.crt  - The self-signed certificate.'
    echo
}


if [ $# -eq 0 ]
then
    usage
    exit_script 2 'You must state at least a main domain name.'
fi

ZIP_CODE=${ZIP_CODE:-thezipcode}
GITHUB_USER=${GITHUB_USER:-username}
GITHUB_REPO=${GITHUB_REPO:-reponame}

COMMON_NAME=$1
# Next line commented out: TOR Browser complains if CN is not also among alt names.
# shift
ALT_NAME_REF=
ALT_NAMES=
separator=
nix=1
for aN in $@
do
    ALT_NAMES="${ALT_NAMES}${separator}DNS.$((nix++))  = ${aN}"
    separator=$'\n'
done
if [ -n "${ALT_NAMES}" ]
then
    ALT_NAME_REF="subjectAltName    = @alt_names"
    ALT_NAMES="[ alt_names ]${separator}${ALT_NAMES}"
fi

# Create a private key. The -newkey option to req requires parameter file for ECDSA parameter,
# so it is easier to just create the key separately.
openssl ecparam -name secp384r1 -genkey -out the.key || exit_script 1 "Error in creation of key."

# Create a dual-domain self-signed certificate.
# cat << EOF
cat << EOF | openssl req -x509 -config - -days 365 -set_serial 1 -key the.key -out the.crt || exit_script 1 "Error in creation of certificate."
[ req ]
distinguished_name  = req_dn
req_extensions      = v3_req
x509_extensions     = v3_ca
prompt              = no

[ req_dn ]
C             = US
ST            = MN ${ZIP_CODE}
L             = 15705 35th Avenue North Plymouth
O             = Evil Cake Genius/Gateaux Inc.
OU            = Robert Hansen, baker
CN            = ${COMMON_NAME}
emailAddress  = ${GITHUB_REPO}@${GITHUB_USER}.github.com

[ v3_ca ]
basicConstraints  = CA:TRUE
keyUsage          = keyCertSign,cRLSign
${ALT_NAME_REF}

[ v3_req ]
# Not used for self-signing
basicConstraints  = CA:FALSE
keyUsage          = digitalSignature,nonRepudiation,keyEncipherment
${ALT_NAME_REF}

${ALT_NAMES}
EOF

exit_script 0 "Self-signed certificate created."

