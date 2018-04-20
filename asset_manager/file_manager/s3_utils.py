from django.conf import settings
from . import models

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME,
    )
bucket = settings.AWS_STORAGE_BUCKET_NAME

def update_s3_key(old_s3_key, new_s3_key):
    """
    Updates a single S3 Object Key. S3 Objects cannot be renamed, so copy/delete instead
    """
    copy_s3_object(old_s3_key, new_s3_key)
    delete_s3_object(old_s3_key)

def copy_s3_object(old_s3_key, new_s3_key):
    """
    Copies an S3 Object
    """
    try:
        response = s3.copy_object(Bucket=bucket, CopySource=bucket+'/'+old_s3_key, Key=new_s3_key, ACL='public-read')
        logging.info('Copied {0} to {1}, HTTPStatusCode: {2}'.format(old_s3_key, new_s3_key, response['ResponseMetadata']['HTTPStatusCode']))
    except ClientError as e:
        logging.error("Received error: {0} \nKey: {1} New Key: {2}".format(e, old_s3_key, new_s3_key), exc_info=True)

def delete_s3_object(s3_key):
    """
    Deletes an S3 Object
    """
    try:
        response = s3.delete_object(Bucket=bucket, Key=s3_key)
        logging.info('Deleted {0}, HTTPStatusCode: {1}'.format(s3_key, response['ResponseMetadata']['HTTPStatusCode']))
    except ClientError as e:
        logging.error("Received error: {0}".format(e), exc_info=True)
