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

def send_alert_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    server.starttls()
    server.login(settings.ADMIN_EMAIL_ADDRESS, settings.ADMIN_EMAIL_PASSWORD)

    COMMASPACE = ', '

    msg = MIMEMultipart()
    msg['From'] = settings.ADMIN_EMAIL_ADDRESS
    msg['To'] = COMMASPACE.join(settings.RECIPIENT_EMAIL_ADDRESS)
    msg['Subject'] = 'DAM backup has encountered an unexpected error'

    body = 'Mert! Something has broken! Go and fix it quick!!!'

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
    @TODO delete local copy.
    """

    key = ('emf-assets-backup/db_backups/'
        + 'dams_db '
        + datetime.now().strftime('%y-%m-%d %H:%M:%S')
        + ' '
        + get_code_version()
        + get_file_extension(source_file_path)
        )

    try:
        s3.upload_file(source_file_path, bucket, key)
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
    p = str(pexpect.run('python manage.py dumpdata -o ' + JSON_FILE_NAME))


def run():
    # create_sql_dump()
    # backup_to_s3(SQL_BACKUP_FILENAME)
    #
    # create_pg_dump()
    # backup_to_s3(JSON_FILE_NAME)

    send_alert_email()
