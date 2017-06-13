from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase

from file_manager import s3_utils

from file_manager.models import Asset, Folder

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

class S3_UtilsTest(TestCase):

    def clear_bucket(self):
        """
        Empty S3 Bucket to ensure no cross-contamination between tests
        """
        logging.info('clearing bucket...')
        contents = s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)
        if 'Contents' in contents:
            for obj in contents['Contents']:
                s3_utils.s3.delete_object(Bucket = settings.AWS_STORAGE_BUCKET_NAME, Key = obj['Key'])

    def get_bucket_contents(self):
        contents = s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)
        bucket_contents = []
        if 'Contents' in contents:
            for obj in contents['Contents']:
                bucket_contents.append(obj['Key'])
        return bucket_contents

    # def setUp(self):

    def tearDown(self):
        self.clear_bucket()

#  ------------- Folders ------------ #

    def test_create_folder(self):
        logging.info('test_create_folder...')
        s3_utils.create_s3_folder('media/test_folder/')

        bucket_contents = []
        for obj in s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)['Contents']:
            bucket_contents.append(obj['Key'])

        self.assertEqual(bucket_contents, ['media/test_folder/'])

    def test_update_single_folder(self):
        logging.info('test_update_single_folder...')
        s3_utils.create_s3_folder('media/test_folder/')
        s3_utils.update_s3_key('media/test_folder/', 'media/test_folder_edit/')

        bucket_contents = []
        for obj in s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)['Contents']:
            bucket_contents.append(obj['Key'])

        self.assertEqual(bucket_contents, ['media/test_folder_edit/'])

    def test_update_folder_with_subfolders(self):
        logging.info('test_update_folder_with_subfolders...')
        f1 = Folder(name='test_folder')
        f1.save()
        f2 = Folder(name='subfolder', parent=f1)
        f2.save()
        f1.name = 'test_folder_edit'
        f1.save()

        bucket_contents = []
        for obj in s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)['Contents']:
            bucket_contents.append(obj['Key'])

        self.assertEqual(bucket_contents, ['media/test_folder_edit/', 'media/test_folder_edit/subfolder/'])

    def test_delete_single_folder(self):
        logging.info('test_delete_single_folder...')
        s3_utils.create_s3_folder('media/test_folder/')
        s3_utils.delete_s3_object('media/test_folder/')

        contents = s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)

        self.assertFalse('Contents' in contents)


    def test_delete_folder_with_subfolders(self):
        logging.info('test_delete_folder_with_subfolders...')
        f1 = Folder(name='test_folder')
        f1.save()
        f2 = Folder(name='subfolder', parent=f1)
        f2.save()
        f3 = Folder(name='second_folder')
        f3.save()
        f1.delete()

        bucket_contents = []
        for obj in s3_utils.s3.list_objects(Bucket = settings.AWS_STORAGE_BUCKET_NAME)['Contents']:
            bucket_contents.append(obj['Key'])

        self.assertEqual(bucket_contents, ['media/second_folder/'])

#  ------------- Assets ------------ #

    def test_create_file(self):
        logging.info('test_create_file')
        f1 = Folder(name='test_folder')
        f1.save()
        file1 = Asset(name='file1', parent=f1)
        file1.file.save('file1.txt', ContentFile('Content'.encode('utf-8')))

        self.assertEqual(self.get_bucket_contents(), ['media/test_folder/', 'media/test_folder/file1.txt'])

    def test_update_file_name(self):
        """
        Changing the Asset Object's name property should have no effect on file stored on S3
        """
        logging.info('test_update_file_name')
        f1 = Folder(name='test_folder')
        f1.save()
        file1 = Asset(name='file1', parent=f1)
        file1.file.save('file1.txt', ContentFile('Content'.encode('utf-8')))
        file1.name = 'file1-edit'
        file1.save()

        self.assertEqual(self.get_bucket_contents(), ['media/test_folder/', 'media/test_folder/file1.txt'])

    def test_update_file(self):
        """
        Update a Asset Object with a new file (eg a new version). Old file should be deleted on S3
        """
        logging.info('test_update_file')
        f1 = Folder(name='test_folder')
        f1.save()
        myAsset = Asset(name='my-file', parent=f1)
        myAsset.file.save('file-v1.txt', ContentFile('Content'.encode('utf-8')))
        myAsset.file.save('file-v2.txt', ContentFile('Content2'.encode('utf-8')))

        self.assertEqual(self.get_bucket_contents(), ['media/test_folder/', 'media/test_folder/file-v2.txt'])

    def test_delete_file(self):
        """
        When a Asset Object is deleted, its associated S3 Object should also be deleted
        """
        logging.info('test_delete_file')
        f1 = Folder(name='test_folder')
        f1.save()
        file1 = Asset(name='file1', parent=f1)
        file1.file.save('file.txt', ContentFile('Content'.encode('utf-8')))
        file1.delete()

        self.assertEqual(self.get_bucket_contents(), ['media/test_folder/'])

# ------------ Folders and Assets ------------ #

    def test_update_folder_with_files(self):
        """
        When a Folder name is updated, should update the S3 keys of it and all its Assets
        """
        logging.info('test_update_folder_with_files')
        f1 = Folder(name='my-folder')
        f1.save()
        file1 = Asset(name='file1', parent=f1)
        file1.file.save('file1.txt', ContentFile('Content'.encode('utf-8')))
        file2 = Asset(name='file2', parent=f1)
        file2.file.save('file2.txt', ContentFile('Content'.encode('utf-8')))
        file3 = Asset(name='file3', parent=f1)
        file3.file.save('file3.txt', ContentFile('Content'.encode('utf-8')))
        file4 = Asset(name='file4', parent=f1)
        file4.file.save('file4.txt', ContentFile('Content'.encode('utf-8')))
        file5 = Asset(name='file5', parent=f1)
        file5.file.save('file5.txt', ContentFile('Content'.encode('utf-8')))
        file6 = Asset(name='file6', parent=f1)
        file6.file.save('file6.txt', ContentFile('Content'.encode('utf-8')))

        f1.name='my-folder-edit'
        f1.save()

        self.assertEqual(self.get_bucket_contents(), [
            'media/my-folder-edit/',
            'media/my-folder-edit/file1.txt',
            'media/my-folder-edit/file2.txt',
            'media/my-folder-edit/file3.txt',
            'media/my-folder-edit/file4.txt',
            'media/my-folder-edit/file5.txt',
            'media/my-folder-edit/file6.txt',
        ])

    def test_update_folder_with_subfolders_and_files(self):
        """
        When a Folder name is updated, its own S3 key, along with the S3 keys of its subfolders and files, should be updated
        """
        logging.info('test_update_folder_with_subfolders_and_files')
        f1 = Folder(name='f1')
        f1.save()
        f2 = Folder(name='f2', parent=f1)
        f2.save()
        f3 = Folder(name='f3', parent=f1)
        f3.save()
        f4 = Folder(name='f4', parent=f1)
        f4.save()
        f5 = Folder(name='f5', parent=f2)
        f5.save()
        f6 = Folder(name='f6', parent=f2)
        f6.save()
        f7 = Folder(name='f7', parent=f4)
        f7.save()

        file1 = Asset(name='file1', parent=f1)
        file1.file.save('file1.txt', ContentFile('Content'.encode('utf-8')))
        file2 = Asset(name='file2', parent=f1)
        file2.file.save('file2.txt', ContentFile('Content'.encode('utf-8')))
        file3 = Asset(name='file3', parent=f2)
        file3.file.save('file3.txt', ContentFile('Content'.encode('utf-8')))
        file4 = Asset(name='file4', parent=f2)
        file4.file.save('file4.txt', ContentFile('Content'.encode('utf-8')))
        file5 = Asset(name='file5', parent=f6)
        file5.file.save('file5.txt', ContentFile('Content'.encode('utf-8')))
        file6 = Asset(name='file6', parent=f6)
        file6.file.save('file6.txt', ContentFile('Content'.encode('utf-8')))
        file7 = Asset(name='file7', parent=f6)
        file7.file.save('file7.txt', ContentFile('Content'.encode('utf-8')))
        file8 = Asset(name='file8', parent=f7)
        file8.file.save('file8.txt', ContentFile('Content'.encode('utf-8')))
        file9 = Asset(name='file9', parent=f7)
        file9.file.save('file9.txt', ContentFile('Content'.encode('utf-8')))

        f2.name = 'f2-edit'
        f2.save()

        self.assertEqual(set(self.get_bucket_contents()), set([
            'media/f1/',
            'media/f1/file1.txt',
            'media/f1/file2.txt',
            'media/f1/f2-edit/',
            'media/f1/f2-edit/file3.txt',
            'media/f1/f2-edit/file4.txt',
            'media/f1/f2-edit/f5/',
            'media/f1/f2-edit/f6/',
            'media/f1/f2-edit/f6/file5.txt',
            'media/f1/f2-edit/f6/file6.txt',
            'media/f1/f2-edit/f6/file7.txt',
            'media/f1/f3/',
            'media/f1/f4/',
            'media/f1/f4/f7/',
            'media/f1/f4/f7/file8.txt',
            'media/f1/f4/f7/file9.txt',
        ]))

    def test_delete_folder_with_files(self):
        """
        When a Folder is deleted, all its Assets should also be deleted
        """
        logging.info('test_delete_folder_with_files')
        f1 = Folder(name='f1')
        f1.save()
        f2 = Folder(name='f2', parent=f1)
        f2.save()
        f3 = Folder(name='f3', parent=f1)
        f3.save()

        file1 = Asset(name='file1', parent=f2)
        file1.file.save('file1.txt', ContentFile('Content'.encode('utf-8')))
        file2 = Asset(name='file2', parent=f2)
        file2.file.save('file2.txt', ContentFile('Content'.encode('utf-8')))
        file3 = Asset(name='file3', parent=f2)

        f2.delete()

        self.assertEqual(set(self.get_bucket_contents()), set([
            'media/f1/',
            'media/f1/f3/'
        ]))

    def test_delete_folder_with_subfolders_and_files(self):
        """
        When a Folder is deleted, all its subfolders and Assets should also be deleted
        """
        logging.info('test_delete_folder_with_subfolders_and_files')
        f1 = Folder(name='f1')
        f1.save()
        f2 = Folder(name='f2', parent=f1)
        f2.save()
        f3 = Folder(name='f3', parent=f1)
        f3.save()
        f4 = Folder(name='f4', parent=f1)
        f4.save()
        f5 = Folder(name='f5', parent=f2)
        f5.save()
        f6 = Folder(name='f6', parent=f2)
        f6.save()
        f7 = Folder(name='f7', parent=f4)
        f7.save()
        f8 = Folder(name='f8', parent=f6)
        f8.save()

        file1 = Asset(name='file1', parent=f1)
        file1.file.save('file1.txt', ContentFile('Content'.encode('utf-8')))
        file2 = Asset(name='file2', parent=f1)
        file2.file.save('file2.txt', ContentFile('Content'.encode('utf-8')))
        file3 = Asset(name='file3', parent=f2)
        file3.file.save('file3.txt', ContentFile('Content'.encode('utf-8')))
        file4 = Asset(name='file4', parent=f2)
        file4.file.save('file4.txt', ContentFile('Content'.encode('utf-8')))
        file5 = Asset(name='file5', parent=f6)
        file5.file.save('file5.txt', ContentFile('Content'.encode('utf-8')))
        file6 = Asset(name='file6', parent=f6)
        file6.file.save('file6.txt', ContentFile('Content'.encode('utf-8')))
        file7 = Asset(name='file7', parent=f6)
        file7.file.save('file7.txt', ContentFile('Content'.encode('utf-8')))
        file8 = Asset(name='file8', parent=f7)
        file8.file.save('file8.txt', ContentFile('Content'.encode('utf-8')))
        file9 = Asset(name='file9', parent=f7)
        file9.file.save('file9.txt', ContentFile('Content'.encode('utf-8')))

        f2.delete()

        self.assertEqual(set(self.get_bucket_contents()), set([
            'media/f1/',
            'media/f1/file1.txt',
            'media/f1/file2.txt',
            'media/f1/f3/',
            'media/f1/f4/',
            'media/f1/f4/f7/',
            'media/f1/f4/f7/file8.txt',
            'media/f1/f4/f7/file9.txt',
        ]))
