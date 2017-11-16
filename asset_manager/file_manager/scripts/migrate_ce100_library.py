import openpyxl
import os

from django.conf import settings
from file_manager.models import Asset, Folder

import boto3
import botocore
s3 = boto3.resource('s3')

BUCKET_NAME = 's3-ce100-library-backup'
KEY = 'Case-Studies/Agency-of-Design-Case-Study.pdf'

os.chdir(settings.BASE_DIR + '/file_manager/scripts/ce100_migration/')
wb = openpyxl.load_workbook('ce100_insight_list_2017_11_14.xlsx')
sheet = wb.get_sheet_by_name('result')

def download_file(s3, bucket_name, key, destination_folder):

    if not destination_folder.endswith('/'):
        destination_folder += '/'

    filename = key.rsplit('/')[-1]
    path = destination_folder + filename

    try:
        s3.Bucket(bucket_name).download_file(key, path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    print('File {} successfully downloaded \nfrom Bucket: {}, Key: {}'.format(filename, bucket_name, key))

def run():
    print("Well done, ce100 library successfully migrated... well, almost :-)")

    insight_id = str(sheet.cell(row=2, column=1).value)
    title = sheet.cell(row=2, column=2).value
    url = sheet.cell(row=2, column=3).value
    insight_type = sheet.cell(row=2, column=4).value
    author = sheet.cell(row=2, column=5).value
    date = sheet.cell(row=2, column=6).value
    active = str(sheet.cell(row=2, column=7).value)
    resource = str(sheet.cell(row=2, column=8).value)

    print('Foo:\n' +
        insight_id + '\n' +
        title + '\n' +
        url + '\n' +
        insight_type + '\n' +
        author + '\n' +
        date + '\n' +
        active + '\n' +
        resource + '\n'
        )

    # f = Folder(name='folder1')
    # a = Asset(parent=f, name='asset1')

    download_file(s3, BUCKET_NAME, KEY, 'temporary_files')
