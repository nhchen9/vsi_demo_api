#!/bin/bash

set -e

docker build --target kmstool-instance -t kmstool-instance -f src/aws-nitro-enclaves-sdk-c/containers/Dockerfile.al2 src/aws-nitro-enclaves-sdk-c
CONTAINER_ID=$(docker create kmstool-instance)
docker cp $CONTAINER_ID:/kmstool_instance ./
docker cp $CONTAINER_ID:/usr/lib64/libnsm.so ./
docker rm $CONTAINER_ID


mv kmstool_instance src/kmstool_instance

docker build -t enclave-app .