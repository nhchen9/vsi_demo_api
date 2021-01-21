#!/bin/bash

docker run -it -v ~/enclave-app/src/:/src/ --network host enclave-app bash