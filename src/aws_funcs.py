import boto3
import json
import base64

from botocore.exceptions import ClientError
from botocore.config import Config

KMS_KEY_ARN = 'arn:aws:kms:us-west-1:779619664536:key/0438229a-5d2f-49ab-9b69-d8e2f5688d02'
# KMS_KEY_ARN = 'arn:aws:kms:us-west-1:779619664536:key/bd199a4c-b7d4-42a3-9b9e-816e9f4155e2'
BUCKET = 'enclave-testing-721f5e9d-2b0c-46b7-8128-411a764cb8de'

def retrieve_s3(s3_key, bucket=BUCKET):
    session = boto3.session.Session(region_name='us-west-1')
    s3_client = session.client('s3')
    kms_client = session.client('kms')

    try:
        response = s3_client.get_object(Bucket=BUCKET, Key=s3_key)
        data = json.loads(response['Body'].read())['encrypted_data']
    except ClientError as e:
        #logging.error(e)
        data = kms_client.encrypt(KeyId=KMS_KEY_ARN, Plaintext="{}")
        data = base64.b64encode(data['CiphertextBlob']).decode()
        return data

    return data


def upload_s3(s3_key, value, data_key='encrypted_data', bucket=BUCKET):
    session = boto3.session.Session(region_name='us-west-1')
    s3_client = session.client('s3')

    data = json.dumps({data_key: value})

    try:
        response = s3_client.put_object(Bucket=bucket, Key=s3_key, Body=bytes(data.encode('utf-8')))
    except ClientError as e:
        #logging.error(e)
        return False
    
    return True


# DEBUG FUNCTION
def encrypt_data(data, arn=KMS_KEY_ARN):
    session = boto3.session.Session(region_name='us-west-1')
    kms_client = session.client('kms')

    encrypted_data = kms_client.encrypt(KeyId=arn, Plaintext=f'{data}')
    b64_encrypted_data = base64.b64encode(encrypted_data['CiphertextBlob']).decode()

    return b64_encrypted_data

# DEBUG FUNCTION
def decrypt_data(data, arn=KMS_KEY_ARN):
    session = boto3.session.Session(region_name='us-west-1')
    kms_client = session.client('kms')

    b64_encrypted_data = base64.b64decode(data)
    decrypted_data = kms_client.decrypt(CiphertextBlob=b64_encrypted_data, KeyId=arn)
    
    return decrypted_data