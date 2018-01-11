# Backup S3 bucket and Django postgresql DB

# @TODO catch exceptions and log + email

from django.conf import settings
from datetime import datetime

import os
import pexpect
import smtplib
import sys

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

backup_filename = settings.BASE_DIR + '/file_manager/scripts/temporary_files/dbexport.pgsql'

def send_alert_email():
    server = smtplib.SMTP_SSL('aspmx.l.google.com')
    # server.ehlo()
    # server.starttls()
    server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)

    msg=" \
    Mert! Something has broken! Go and fix it quick!!!"

    server.sendmail(settings.EMAIL_ADDRESS, settings.EMAIL_ADDRESS, msg)

def get_code_version():
    # child = pexpect.spawn('git rev-parse --abbrev-ref HEAD')
    # child.expect(pexpect.EOF)

    git_branch = str(pexpect.run('git rev-parse --abbrev-ref HEAD'))
    end_of_line_index = git_branch.find('\\r')
    git_branch = git_branch[2:end_of_line_index]

    commit_hash = str(pexpect.run('git rev-parse --short HEAD'))
    end_of_line_index = commit_hash.find('\\r')
    commit_hash = commit_hash[2:end_of_line_index]

    return git_branch + ' ' + commit_hash

def backup_to_s3(pgSqlFileName):
    """
    Backup .pgsql file to S3, then delete local copy.
    """

    key = ('emf-assets-backup/db_backups/'
        + 'dams_db '
        + datetime.now().strftime('%y-%m-%d %H:%M:%S')
        + ' '
        + get_code_version())

    try:
        s3.upload_file(backup_filename, bucket, key)
        logging.info('Uploaded file {} to S3 Bucket {}, Key {}'.format(pgSqlFileName, bucket, key))
    except Exception as e:
        logging.error('Encountered an error: {}'.format(e))


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
        + backup_filename
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


def delete_local_file(file_path):
    os.remove(file_path)


def run():
    create_sql_dump()
    backup_to_s3(backup_filename)
    # delete_local_file(backup_filename)

    # send_alert_email()
    # get_code_version()
