import json
import logging
import base64
import subprocess
import time
import re
import aws_funcs

from fastapi import FastAPI

# Demo encrypted command
# AQICAHhOmVIiapsKsJ3v8MJ8YOJecymAtttFPxQnthhvMsfe3AFjGcrHYdPYTL5Z9NlF1NEYAAAAaDBmBgkqhkiG9w0BBwagWTBXAgEAMFIGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMFaT5jgEHn4AY/Yn5AgEQgCUJ+z5IzuzYXyWB7vNJ523BHqu5CLshTC3NlGlDY6Vz40m9hQyM

ENCLAVE_CID = '4'
DATA_KEY = 'encrypted_data'

tags_metadata = [
    {
        'name': 'decrypt',
        'description': 'Takes a KMS encrypted command, decrypts and processes \
            the data in the enclave, instructs the host to either update or query \
            the user\'s data.'
    }
]

app = FastAPI(
    title='Enclave Demo',
    description='Processes encrypted commands through an enclave',
    openapi_tags=tags_metadata
)

@app.get("/decrypt", tags=['decrypt'])
async def request(command: str):
    data = aws_funcs.retrieve_s3(DATA_KEY)
    status = dict()

    proc = subprocess.Popen(
        [
            "./kmstool_instance",
            "--port", "3000",
            "--cid", "4",
            "--region", "us-west-1",
            f"{data}",
            f"{command}"
        ],
        stderr=subprocess.PIPE
    )
    output = proc.communicate()
    msg = re.findall('Message": "(.*?)" }\n', output[1].decode())[0].replace('\\', '')
    if len(msg) > 1:
        aws_funcs.upload_s3('encrypted_data', msg)
        # decrypted_data = aws_funcs.decrypt_data(msg)
        status['message'] = f'Command: Data update, Result: {msg}'
        # status['debug'] = f'DEBUG: Decrypted data: {decrypted_data["Plaintext"]}'
    else:
        status['message'] = f'Command: Status Query, Result: {msg}'

    return status
