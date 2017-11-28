import openpyxl
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from file_manager.models import Asset, Folder

import boto3
import botocore
s3 = boto3.resource('s3')

SOURCE_BUCKET_NAME = 's3-ce100-library-backup'
KEY = 'Case-Studies/Agency-of-Design-Case-Study.pdf'

os.chdir(settings.BASE_DIR + '/file_manager/scripts/ce100_migration/')
wb = openpyxl.load_workbook('ce100_insight_list_2017_11_14.xlsx')
sheet = wb.get_sheet_by_name('result')

type_dict = {
    'CASE STUDY' : 'CS',
    'CO.PROJECT' : 'CP',
    'IMAGE' : 'IM',
    'LINK' : 'LN',
    'PAPER' : 'PA',
    'PRESENTATION' : 'PR',
    'REPORT' : 'RT',
    'VIDEO' : 'VI',
    'WORKSHOP SUMMARY' : 'WS'
}

def get_contributors(authors):
    pass

def get_filename(key):
    return key.rsplit('/')[-1]

def get_folder_name(key):
    return key.rsplit('/')[-2]

def get_type_code(type):
    return type_dict[type]

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

def create_folder(folder_name):

    try:
        folder_parent = Folder.objects.get(name='Cello Library')

        folders = Folder.objects.filter(parent=folder_parent)
        print('current folders: {}'.format(folders))

        folder_exists = False

        for folder in folders:
            if folder.name == folder_name:
                folder_exists = True
                print('Folder {} already exists'.format(folder_name))
                break

        if not folder_exists:
            f = Folder(parent=folder_parent, name=folder_name)
            f.save()
            print('created folder {}, parent = {}'.format(f.name, f.parent))

    except ObjectDoesNotExist as e:
        print('Searching for Cello Library Folder... {}'.format(e))


def create_asset(name, filename, folder_name, type_field, authors, created_at, active, resource):
    create_folder(folder_name)
    asset = Asset(
        name=name,
        parent=folder_name,
        type_field=get_type_code(type_field),
        contributors=get_contributors(authors)
        # created_at
        # active
        # resource
    )


def migrate_asset():
    download_file()
    create_asset()

def run():
    print("Well done, ce100 library successfully migrated... well, almost :-)")

    # insight_id = str(sheet.cell(row=2, column=1).value)
    # title = sheet.cell(row=2, column=2).value
    # url = sheet.cell(row=2, column=3).value
    # insight_type = sheet.cell(row=2, column=4).value
    # author = sheet.cell(row=2, column=5).value
    # date = sheet.cell(row=2, column=6).value
    # active = str(sheet.cell(row=2, column=7).value)
    # resource = str(sheet.cell(row=2, column=8).value)
    #
    # print('Foo:\n' +
    #     insight_id + '\n' +
    #     title + '\n' +
    #     url + '\n' +
    #     insight_type + '\n' +
    #     author + '\n' +
    #     date + '\n' +
    #     active + '\n' +
    #     resource + '\n'
    #     )
    #
    # # f = Folder(name='folder1')
    # # a = Asset(parent=f, name='asset1')
    #
    # download_file(s3, SOURCE_BUCKET_NAME, KEY, 'temporary_files')
