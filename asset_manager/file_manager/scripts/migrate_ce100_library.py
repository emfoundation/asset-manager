import dateutil.parser
import openpyxl
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File

from file_manager.models import Asset, Folder, Collection, Contributor

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

def create_contributor(contributor_name):
    contributor = Contributor(name = contributor_name)
    contributor.save()
    print('Contributor {} created...'.format(contributor_name))
    return contributor

def get_or_create_contributors(authors):
    # For each contributor, get if exists, create otherwise, and return
    contributor_names = authors.split(',')
    contributor_names = [ contributor_name.strip() for contributor_name in contributor_names ]
    # eg ['foo', 'bar']

    contributors = []
    # to return all contributor models

    for contributor_name in contributor_names:
        contributor = Contributor.objects.filter(name__iexact=contributor_name).first()
        if contributor is None:
            # coontributor does not exist
            contributors.append(create_contributor(contributor_name))
        else:
            print('Contributor {} exists already...'.format(contributor_name))
            contributors.append(contributor)

    return contributors

def get_collection_from_resource_flag(resource_flag):
    if resource_flag == True:
        return Collection.objects.get(id=2)
    return Collection.objects.get(id=1)

def get_filename(url):
    return url.rsplit('/')[-1]

def get_folder_name(url):
    return url.rsplit('/')[-2]

def get_s3_key(url):
    return get_folder_name(url) + '/' + get_filename(url)

def get_type_code(type):
    return type_dict[type]

def download_file(s3, bucket_name, url, destination_folder):

    if not destination_folder.endswith('/'):
        destination_folder += '/'

    filename = get_filename(url)
    path = destination_folder + filename

    try:
        s3.Bucket(bucket_name).download_file(get_s3_key(url), path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    print('File {} successfully downloaded \nfrom Bucket: {}, Url: {}'.format(filename, bucket_name, url))

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
                return folder

        if not folder_exists:
            f = Folder(parent=folder_parent, name=folder_name)
            f.save()
            print('created folder {}, parent = {}'.format(f.name, f.parent))
            return f

    except ObjectDoesNotExist as e:
        print('Searching for Cello Library Folder... {}'.format(e))


# def create_asset(name, filename, folder_name, type_field, authors, created_at, active, resource):
def create_asset(insight_details):

    parent = create_folder(get_folder_name(insight_details['url']))

    # delete asset if it exists already
    assets = Asset.objects.filter(parent=parent, name=insight_details['title'])
    for a in assets:
        a.delete()

    asset = Asset(
        name=insight_details['title'],
        parent=parent,
    )
    # save must be performed before many-to-many field applied
    asset.save()

    asset.type_field = get_type_code(insight_details['insight_type'])
    asset.contributors = get_or_create_contributors(insight_details['author'])
    asset.uploaded_at = dateutil.parser.parse(insight_details['date'])
    asset.active = insight_details['active']
    asset.collections.add(get_collection_from_resource_flag(insight_details['resource']))

    asset.save()

    filename = get_filename(insight_details['url'])
    f = open(settings.BASE_DIR + '/file_manager/scripts/ce100_migration/temporary_files/{}'.format(filename), 'rb')
    asset.file.save(filename, File(f))

    # is an extra save necessary?
    # a.save()

def migrate_asset(insight_details):
    download_file(s3, SOURCE_BUCKET_NAME, insight_details['url'], 'temporary_files')
    create_asset(insight_details)

def run():
    print("Well done, ce100 library successfully migrated... well, almost :-)")

    insight_details = {
        'insight_id' : str(sheet.cell(row=2, column=1).value),
        'title' : sheet.cell(row=2, column=2).value,
        'url' : sheet.cell(row=2, column=3).value,
        'insight_type' : sheet.cell(row=2, column=4).value,
        'author' : sheet.cell(row=2, column=5).value,
        'date' : sheet.cell(row=2, column=6).value,
        'active' : str(sheet.cell(row=2, column=7).value),
        'resource' : str(sheet.cell(row=2, column=8).value),
    }

    print('Foo:\n' +
        insight_details['insight_id'] + '\n' +
        insight_details['title'] + '\n' +
        insight_details['url'] + '\n' +
        insight_details['insight_type'] + '\n' +
        insight_details['author'] + '\n' +
        insight_details['date'] + '\n' +
        insight_details['active'] + '\n' +
        insight_details['resource'] + '\n'
        )

    migrate_asset(insight_details)

    # test get_date
    # print(get_date('2017-07-04T13:44:27.013675+00:00'))

    # test download_file (again!)
    # download_file(s3, SOURCE_BUCKET_NAME, insight_details['url'], 'temporary_files')

    # print(get_or_create_contributors('foo, bar2, ray'))
    # print('resource', get_collection_from_resource_flag(True))
    # print('collection', get_collection_from_resource_flag(False))

    # test upload!
    # folder = Folder(name='folder1')
    # folder.save()
    # a = Asset(parent=folder, name='asset1')
    # f = open(settings.BASE_DIR + '/file_manager/scripts/ce100_migration/temporary_files/{}'.format('Agency-of-Design-Case-Study.pdf'), 'rb')
    # myfile = File(f)
    # a.file.save('Agency-of-Design-Case-Study.pdf', myfile)


    # a.save()
    # a.contributors = get_or_create_contributors('George Millard, Alex Wijns')

    # contributors = get_or_create_contributors('George Millard, Alex Wijns')
    # for contributor in contributors:
    #     print(contributor)

    # a.contributors = get_or_create_contributors('George Millard, Alex Wijns')
    # a.save()
    #
    # download_file(s3, SOURCE_BUCKET_NAME, KEY, 'temporary_files')
