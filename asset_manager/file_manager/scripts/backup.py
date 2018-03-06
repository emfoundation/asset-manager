# Backup S3 bucket and Django postgresql DB

# @TODO catch exceptions and log + email

from django.conf import settings
from datetime import datetime

import os
import pexpect
import smtplib
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError

s3 = boto3.client(
    's3',
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)
bucket = settings.AWS_STORAGE_BUCKET_NAME

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

VENV_DIR = '/Users/georgemillard/programming/projects/virtualenvs/asset_manager_venv/bin/activate'
TEMP_DIR = settings.BASE_DIR + '/file_manager/scripts/temporary_files/'
SQL_BACKUP_FILENAME = TEMP_DIR + 'sql_dbexport_temp.pgsql'
JSON_FILE_NAME = TEMP_DIR + 'json_dbexport_temp.json'

def get_bucket_contents(bucket, folder = ''):
    """
    Returns a dict of { Object Keys : ETags } for a given bucket, up to 1000 (limited by function).
    If a folder is provided (optional) will be limited to the contents of a folder.
    """
    contents = s3.list_objects_v2(Bucket=bucket, Prefix=folder)
    bucket_contents = {}
    if 'Contents' in contents:
        for obj in contents['Contents']:
            bucket_contents[obj['Key']] = obj['ETag']
            
            # append({
            #     'Key':obj['Key'],
            #     'ETag':obj['ETag']
            # })
            # bucket_contents.append([obj['Key'], obj['ETag']])

    # list_objects_v2 returns up to 1000 objects. When the number of Assets on the DAM exceeds this,
    # an alternative method will be needed. Fire a warning when we reach 800.
    if len(bucket_contents) > 800:
        send_alert_email(message='800/1000 assets stored on the DAM. Please look into alternative backup methods.')

    return bucket_contents

def backup_bucket(source_bucket, destination_bucket):
    key_prefix = ('dam-assets-backups/dams-assets ' + datetime.now().strftime('%y-%m-%d %H:%M:%S') + '/')
    object_dict = get_bucket_contents(source_bucket)

    num_items = len(object_dict)

    for index, key in enumerate(object_dict):
        try:
            s3.copy_object(Bucket=destination_bucket, Key=key_prefix+key, CopySource={
                'Bucket': source_bucket,
                'Key': key
            })
            logging.info('Copied file from {} to {}'.format(source_bucket + '/' + key, destination_bucket + '/' + key_prefix + key))
            progress = int(index/num_items * 100)
                
            print('Backing up S3 Bucket: {} to {} '.format(source_bucket, destination_bucket+'/'+key_prefix) + str(progress) + '%', end="", flush=True)
            print('\r', end='')

        except Exception as e:
            logging.error('Encountered an error: {}'.format(e))
            send_alert_email('An error has occurred: {} Please check the logs.'.format(e))

    print('Backing up S3 Bucket: {} to {} 100%'.format(source_bucket, destination_bucket+'/'+key_prefix))
    return key_prefix

def get_key_less_backup_folder(full_path, backup_folder):
    backup_folder_index = full_path.find(backup_folder)
    if(backup_folder_index == -1):
        print('Backup folder {} not found in path {}'.format(backup_folder, full_path))
    return full_path[backup_folder_index+len(backup_folder):]

def verify_bucket_backup(source_bucket, destination_bucket, destination_folder):
    source_list = get_bucket_contents(source_bucket)
    destination_list = get_bucket_contents(destination_bucket, destination_folder)

    # Destination list keys will include backup folder - this needs to be removed
    # Dictionary keys are immutable, so we will copy to new dictionary
    temp_destination_list = {}
    for key in destination_list:
        temp_destination_list[get_key_less_backup_folder(key, destination_folder)] = destination_list[key]

    destination_list = temp_destination_list

    # Now check for equality
    bucket_backup_verified = True

    print('Verifying S3 Bucket backup')
    # first check they are the same length
    if len(source_list) != len(destination_list):
        bucket_backup_verified = False
        print('foo')
    
    # # are they the same length
    # if not len(source_list) == len(destination_list):
    #     bucket_backup_verified = False
    #     # for each element in source, does its match appear in destination
    #     for obj in source_list:
    #         # 1. Check if source key appears in destination key list:
    #         if obj['Key'] in destination_key_list:
    #             # 2. Check if source key's ETag matches destination key's ETag
    #             print('>>>', obj, destination_list[obj['Key']])
    #             if obj['ETag'] != destination_list[obj['key']]:
    #                 bucket_backup_verified = False
    #         else:
    #             bucket_backup_verified = False

def send_alert_email(message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    server.starttls()
    server.login(settings.ADMIN_EMAIL_ADDRESS, settings.ADMIN_EMAIL_PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = settings.ADMIN_EMAIL_ADDRESS
    msg['To'] = settings.RECIPIENT_EMAIL_ADDRESS
    msg['Subject'] = 'DAM backup has encountered an unexpected error'

    body = message

    msg.attach(MIMEText(body, 'plain'))

    txt = msg.as_string()
    server.sendmail(settings.ADMIN_EMAIL_ADDRESS, settings.ADMIN_EMAIL_ADDRESS, txt)
    server.quit()

def get_code_version():
    git_branch = str(pexpect.run('git rev-parse --abbrev-ref HEAD'))
    end_of_line_index = git_branch.find('\\r')
    git_branch = git_branch[2:end_of_line_index]

    commit_hash = str(pexpect.run('git rev-parse --short HEAD'))
    end_of_line_index = commit_hash.find('\\r')
    commit_hash = commit_hash[2:end_of_line_index]

    return git_branch + ' ' + commit_hash


def get_file_extension(filename):

    return '.' + filename.rsplit('.', 1)[1]


def delete_local_file(file_path):
    os.remove(file_path)


def backup_to_s3(source_file_path):
    """
    Backup file to S3
    """

    key = ('dam-db-backups/'
        + 'dams_db '
        + datetime.now().strftime('%y-%m-%d %H:%M:%S')
        + ' '
        + get_code_version()
        + get_file_extension(source_file_path)
        )

    try:
        s3.upload_file(source_file_path, settings.AWS_BACKUP_BUCKET_NAME, key)
        logging.info('Uploaded file {} to S3 Bucket {}, Key {}'.format(source_file_path, bucket, key))
    except Exception as e:
        logging.error('Encountered an error: {}'.format(e))

    #--- Comment out to allow the system to keep a copy of latest backup ---#
    # delete_local_file(source_file_path)

def create_sql_dump():
    """
    Creates a .pgsql file dump of Django's postgres DB
    """
    child = pexpect.spawn(
        'pg_dump -U '
        + settings.DATABASE_USER
        + ' '
        + settings.DATABASE_NAME
        + ' -f '
        + SQL_BACKUP_FILENAME
    )

    # Only turn on logs to debug. Note your db user password will be logged to
    # this file!

    # f = open(settings.BASE_DIR + '/file_manager/scripts/logs/backup_log.txt', 'wb')
    # child.logfile = f

    # Uncomment for further debug info
    # print(str(child))

    child.expect('Password:')
    child.sendline(settings.DATABASE_USER_PASSWORD)
    child.expect(pexpect.EOF)


def create_pg_dump():
    """
    creates a .json file dump of Django's postgres DB
    """
    pexpect.run('python manage.py dumpdata -o ' + JSON_FILE_NAME)


def run():
    # create_sql_dump()
    # backup_to_s3(SQL_BACKUP_FILENAME)
    
    # create_pg_dump()
    # backup_to_s3(JSON_FILE_NAME)
    # print(get_bucket_contents(settings.AWS_STORAGE_BUCKET_NAME))
    
    # backup_bucket(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_BACKUP_BUCKET_NAME)
    # verify_bucket_backup(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_BACKUP_BUCKET_NAME, 'foo')
    # print(get_media_path('jkh/media/foo'))

    backup_folder = backup_bucket(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_BACKUP_BUCKET_NAME)
    verify_bucket_backup(settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_BACKUP_BUCKET_NAME, backup_folder)

    # print(remove_backup_folder_from_path('a b c/foo', 'a b c/'))
    # print(remove_backup_folder_from_path('bar-rum/foo', 'rum/'))
    # print(remove_backup_folder_from_path('kjh kjh kjh/foo/bar', 'kjh kjh kjh/'))