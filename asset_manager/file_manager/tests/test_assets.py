from django.conf import settings

from django.test import TestCase

from django.core.files.base import ContentFile

from file_manager.models import Asset, Folder

from file_manager import s3_utils

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

# Create your tests here.

class AssetModelFileNameTests(TestCase):

    # Create tests for correct Asset filename
    @classmethod
    def setUpTestData(cls):
        """
        Setup initial conditions for class test methods
        """
        cls.test_folder, created = Folder.objects.get_or_create(name='Test Folder')
        cls.test_folder.save()

    def clear_models(self):
        logging.info('Clearing models...')
        for folder in Folder.objects.filter(parent=self.test_folder):
            folder.delete()

    def tearDown(self):
        self.clear_models()

    # ------------ Tests ------------ #

    def test_filename_on_create_asset_without_file(self):
        """
        Tests filename on create Asset without file
        """
        logging.info('Test filename on create asset without a file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a = Asset(name='a', parent=f)
        a.save()

        self.assertEqual(a.file.name, '')

    # should fail pre #200 fix
    def test_filename_on_edit_parent_without_file(self):
        """
        Test filename on edit parent without file
        """
        logging.info('Test filename on edit parent without file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()

        a = Asset(name='a', parent=f)
        a.save()

        a.parent=f2
        a.save()

        self.assertEqual(a.file.name, '')

    # should fail pre #200 fix
    def test_filename_on_reverse_edit_parent_without_file(self):
        """
        Test filename on reverse edit parent without file
        """
        logging.info('Test filename on reverse edit parent without file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()

        a = Asset(name='a', parent=f)
        a.save()

        a.parent=f2
        a.save()

        a.parent=f
        a.save()

        self.assertEqual(a.file.name, '')

    def test_filename_on_add_file(self):
        """
        Test filename on add file
        """
        logging.info('Test filename on add file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        self.assertEqual(a.file.name, str(f.id) + '/file.txt')

    def test_filename_on_edit_parent_and_add_file(self):
        """
        Test filename on edit parent and add file
        """
        logging.info('Test filename on edit parent and add file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()
        a = Asset(name='a', parent=f)
        a.save()

        a.parent = f2
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))
        self.assertEqual(a.file.name, str(f2.id) + '/file.txt')

    def test_filename_on_create_asset_with_file(self):
        """
        Tests filename on create Asset
        """
        logging.info('Test filename on create asset...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        self.assertEqual(a.file.name, str(f.id) + '/file.txt')

    def test_filename_on_edit_parent_with_file(self):
        """
        Test filename on edit parent with file
        """
        logging.info('Test filename on edit parent with file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()
        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.parent = f2
        a.save()
        self.assertEqual(a.file.name, str(f2.id) + '/file.txt')

    def test_filename_on_reverse_edit_parent_with_file(self):
        """
        Test filename on reverse edit parent with file
        """
        logging.info('Test filename on reverse edit parent with file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.parent = f2
        a.save()

        a.parent = f
        a.save()

        self.assertEqual(a.file.name, str(f.id) + '/file.txt')

    def test_filename_on_remove_file(self):
        """
        Test filename on remove file
        """
        logging.info('Test filename on remove file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.file.delete()

        self.assertEqual(a.file.name, None)

    def test_filename_on_edit_parent_and_remove_file(self):
        """
        Test filename on edit parent and remove file
        """
        logging.info('Test filename on edit parent and remove file...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.parent = f2
        a.file.delete()

        self.assertEqual(a.file.name, None)

class AssetModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Setup initial conditions for class test methods
        """
        cls.test_folder, created = Folder.objects.get_or_create(name='Test Folder')
        cls.test_folder.save()

    def get_assets(self):
        """
        Returns a comma separated list of all Asset file paths
        """
        asset_list = []

        assets = Asset.objects.all()
        for asset in assets:
            asset_list.append(asset.file.name)

        return ','.join(asset_list)

    def clear_models(self):
        logging.info('Clearing models...')
        for folder in Folder.objects.filter(parent=self.test_folder):
            folder.delete()

    def tearDown(self):
        self.clear_models()

    # ------------ Tests ------------ #

    def test_create_asset(self):
        """
        Tests Asset creation
        """
        logging.info('Test create asset...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        self.assertEqual(self.get_assets(), str(a.parent.id) + '/file.txt')

    def test_update_asset_file(self):
        """
        Test update Asset file only
        """
        logging.info('Test update asset file...')
        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))
        a.file.save('file2.txt', ContentFile('Content2'.encode('utf-8')))

        self.assertEqual(self.get_assets(), str(a.parent.id) + '/file2.txt')

    def test_update_asset_parent(self):
        """
        Test update Asset parent only
        """
        logging.info('Test update asset parent...')
        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.parent = f2
        a.save()

        self.assertEqual(self.get_assets(), str(a.parent.id) + '/file.txt')

    def test_update_asset_file_and_parent(self):
        """
        Test update Asset file and parent simultaneously
        """
        logging.info('Test update asset file and parent simultaneously...')
        f = Folder(name='f', parent=self.test_folder)
        f.save()
        f2 = Folder(name='f2', parent=self.test_folder)
        f2.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.parent = f2
        a.file.save('file2.txt', ContentFile('Content2'.encode('utf-8')))

        self.assertEqual(self.get_assets(), str(a.parent.id) + '/file2.txt')

    def test_delete_asset(self):
        """
        Test delete Asset
        """
        logging.info('Test delete asset...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a = Asset(name='a', parent=f)
        a.file.save('file.txt', ContentFile('Content'.encode('utf-8')))

        a.delete()

        self.assertEqual(self.get_assets(), '')

    def test_delete_folder(self):
        """
        Test delete Folder, contained Assets and should be deleted accordingly
        """
        logging.info('Test delete folder...')

        f = Folder(name='f', parent=self.test_folder)
        f.save()

        a1 = Asset(name='a1', parent=f)
        a1.file.save('file1.txt', ContentFile('Content1'.encode('utf-8')))
        a2 = Asset(name='a2', parent=f)
        a2.file.save('file2.txt', ContentFile('Content2'.encode('utf-8')))
        a3 = Asset(name='a3', parent=f)
        a3.file.save('file3.txt', ContentFile('Content3'.encode('utf-8')))

        f.delete()

        self.assertEqual(self.get_assets(), '')
