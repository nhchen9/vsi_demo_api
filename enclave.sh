#!/bin/bash

set -e
ENCLAVE_ID=$(nitro-cli describe-enclaves | jq -r .[0].EnclaveID)

if [ $ENCLAVE_ID = "null" ]; then
    echo "Enclave not found, continuing..."
else
    echo $ENCLAVE_ID
    nitro-cli terminate-enclave --enclave-id $ENCLAVE_ID   
fi

docker build --target kmstool-enclave -t kmstool-enclave -f src/aws-nitro-enclaves-sdk-c/containers/Dockerfile.al2 src/aws-nitro-enclaves-sdk-c

nitro-cli build-enclave --docker-uri kmstool-enclave --output-file kmstool.eif

nitro-cli run-enclave --eif-path kmstool.eif --memory 512 --cpu-count 2 --debug-mode --enclave-cid 4

NEW_ID=$(nitro-cli describe-enclaves | jq -r .[0].EnclaveID)

nitro-cli console --enclave-id $NEW_ID
