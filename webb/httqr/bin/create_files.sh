#!/bin/bash
#
# The setup prepares for launching by creating various files needed when
# building the docker images. The steps are:
#
#   1. Create alpha and bravo services onion keys and addresses.
#   2. Create byte sequence.
#   3. Create alpha TLS key and certificate.
#   4. Create flag zip file.

SCRIPT_NAME=$(basename $0)
SCRIPT_DIR=$(dirname $(realpath -e $0))


function exit_script()
{
    local exit_code=$1
    local msg="$2"
    if [ -n "${msg}" ]
    then
    echo '*****'
    echo '*****'
    echo "***** ${msg}"
    echo '*****'
    echo '*****'
    fi
    exit $((exit_code))
}


function exit_with_usage()
{
    local exit_code=$1
    local msg="$2"
    [ -z "${msg}" ] || echo -e "${msg}\n"
    echo
    echo 'Usage:'
    echo "  $ ${SCRIPT_NAME} <config-file>"
    echo
    echo 'Output:'
    echo '  - Directories tor/services/<onion-service-name> containing the'
    echo '    keys and hostname for each Onion service.'
    echo '  - Directory webserver/ssl containing the key and certificate for'
    echo '    the Onion webserver, along with the Diffie-Hellman parameter'
    echo '    file.'
    echo
    exit $((exit_code))
}

[ $# -gt 0 ] || exit_with_usage

ZIP_CODE=12345-6789
GITHUB_USER=githubusername
GITHUB_REPO=githubreponame
CONFIG_FILE=$1
source ${CONFIG_FILE} || exit_script 2 "Unable to source config file '${CONFIG_FILE}'. Aborting."

# ----------------------------------------------------------------------------
echo 'Creating onion service keys and addresses.'

declare -A ONION_SERVICES=([alpha]='' [bravo]='')

mkdir -p tor/services
for sN in ${!ONION_SERVICES[@]}
do
    echo "Attempting to create Onion service key and files for service ${sN}."
    # Avoid mistakes by refusing to overwrite existing service files.
    (mkdir tor/services/${sN} && \
        cd tor/services/${sN} && \
        ${SCRIPT_DIR}/onionkeys.sh) || \
        exit_script 1 "Error creating Onion service files for service ${sN}. Aborting."
    ONION_SERVICES[${sN}]="$(cat tor/services/${sN}/hostname)" || \
        exit_script 1 "Error retrieving Onion service address for service ${sN}. Aborting."
done

# ----------------------------------------------------------------------------
echo "Creating byte sequence to embed."

byteseq="$(python3 ${SCRIPT_DIR}/url2seq.py -u ${ONION_SERVICES[bravo]}/java -s)" || \
    exit_script 1 'Error in creating byte sequence. Aborting.'

# ----------------------------------------------------------------------------
echo 'Creating alpha service TLS key and certificate.'

(mkdir webserver/ssl && \
    cd webserver/ssl && \
    export ZIP_CODE && \
    export GITHUB_USER && \
    export GITHUB_REPO && \
    ${SCRIPT_DIR}/sscrt.sh "${ONION_SERVICES[alpha]}" "${byteseq}" && \
    mkdir -p -m 700 private && \
    mv the.key private/server.key && \
    mv the.crt server.crt && \
    ${SCRIPT_DIR}/dh.sh) || \
    exit_script 1 "Error creating key, certificate and Diffie-Hellman parameter file for webserver. Aborting."

# ----------------------------------------------------------------------------
echo 'Creating flag zip files'

(mkdir webserver/flags && \
    cd webserver/flags && \
    (ok=true; for ((c=0; c<10; c++)); do if ! ${SCRIPT_DIR}/zipflag.sh "${ZIP_CODE}" "$(uuidgen).zip"; then ok=false; break; fi; done; ${ok}) ) || \
    exit_script 1 'Error creating flag zip files. Aborting.'

exit_script 0 "Entrypoint: https://${ONION_SERVICES[alpha]}"

# EVERYTHING BELOW HERE NEEDS ALTERING
# 
# 1. Use the zipflag script
# 2. Use the onionkeys script, which in turn uses the onionfiles script
# 3. Use the url2seq script, with the bravo service onion address.
# 4. Again, use the onionkeys script
# 5. Modify and use the sscrt script
# 
# 
# NOTE THAT THE ALPHA SERVICE WILL RUN AN APPLICATION SERVER, SERVING RANDOM
# IMAGES FOR AS WELL THE COOKIE PATH (WITH COOKIES) AS FOR ALL OTHER PATHS
# (WITH "THIS IS NOT THE SITE YOU ARE LOOKING FOR" AND A STORMTROOPER IMAGE).
# 
# NOTE THAT THE BRAVO SERVICE WILL NO LONGER RUN HTTPS!
# 
# THE BRAVO SERVICE WILL SERVE BEVERAGE PATHS (WITH 418), THE TEA PATH (WITH
# EITHER COOKIE INJECTION AND REDIRECT, OR RANDOM REDIRECT IMAGE) AND THE
# SPECIALIZED TEA PATH (WITH EITHER REDIRECT OR RANDOM ORDERED CAKE IMAGES
# AND A RANDOM FLAG IMAGE CONCATENATED WITH THE FLAG ZIP FILE).
# 
# 
# SCRIPT_NAME=$(basename $0)
# SCRIPT_DIR=$(dirname $(realpath -e $0))
# 
# function exit_script()
# {
#     local exit_code=$1
#     local msg="$2"
#     [ -z "${msg}" ] || echo "${msg}"
#     exit $((exit_code))
# }
# 
# 
# function exit_with_usage()
# {
#     local exit_code=$1
#     local msg="$2"
#     [ -z "${msg}" ] || echo -e "${msg}\n"
#     echo
#     echo 'Usage:'
#     echo "  $ ${SCRIPT_NAME} <onion-service-name> {<onion-service-name>}"
#     echo
#     echo 'Output:'
#     echo '  - Directories tor/services/<onion-service-name> containing the'
#     echo '    keys and hostname for each Onion service.'
#     echo '  - Directory webserver/ssl containing the key and certificate for'
#     echo '    the Onion webserver, along with the Diffie-Hellman parameter'
#     echo '    file.'
#     echo
#     exit $((exit_code))
# }
# 
# [ $# -gt 0 ] || exit_with_usage
# 
# SERVICE_NAMES=($@)
# 
# svc_addr=()
# mkdir -p tor/services
# for sN in ${SERVICE_NAMES[@]}
# do
#     (mkdir -p tor/services/${sN} && \
#         cd tor/services/${sN} && \
#         ${SCRIPT_DIR}/onionkeys.sh) || \
#         exit_script 1 "Error creating Onion service files for service ${sN}. Aborting."
#     svc_addr+=($(cat tor/services/${sN}/hostname)) || \
#         exit_script 1 "Error retrieving Onion service address for service ${sN}. Aborting."
# done
# 
# (mkdir -p webserver/ssl && \
#     cd webserver/ssl && \
#     ${SCRIPT_DIR}/sscrt.sh ${svc_addr[@]} && \
#     mkdir -p -m 700 private && \
#     mv the.key private/server.key && \
#     mv the.crt server.crt && \
#     ${SCRIPT_DIR}/dh.sh) || \
#     exit_script 1 "Error creating key, certificate and Diffie-Hellman parameter file for webserver. Aborting."
# 
# exit_script 0 'Execution completed successfully.'
# 
