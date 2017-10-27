from django.conf import settings

from django.test import TestCase

from django.core.files.base import ContentFile

from file_manager.models import Asset, Folder, TagGroup, Tag, ContinentTagGroup, CountryTag, Contributor, Collection
from file_manager import s3_utils

import logging

logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )

class FolderModelTests(TestCase):

    # ----------- Set up ----------- #

    def setUp(self):
        for i in range(1, 10):
            Folder.objects.create(name="f%d" % i)
        Folder.objects.create(name="")
    # ----------- Tests ------------ #

    def test_create_folder(self):
        """
        Tests folder creation
        """
        logging.info('Test create folder...')

        f1 = Folder.objects.get(name="f1")
        self.assertEqual(f1.name, "f1")

        self.assertFalse(Folder.objects.filter(name="").exists(), "Folder saved without a name!")

    def test_child_deletion(self):
        """
        Tests that the children of the folder get deleted
        """
        logging.info('Test delete Folder children...')

        f2 = Folder.objects.get(name="f2")
        f3 = Folder.objects.get(name="f3")
        f2.parent = f3
        f2.save()
        f3.delete()

        self.assertFalse(Folder.objects.filter(name="f2").exists())
        # self.assertRaises(Folder.DoesNotExist, lambda: Folder.objects.get(name="f2")) --Alternative method of checking

    def test_recursive_parent(self):
        """
        Test that a folder cannot be the child & the parent of another folder
        """
        logging.info('Test setting Folder parent to be the child...')

        f4 = Folder.objects.get(name="f4")
        f5 = Folder.objects.get(name="f5")
        f4.parent = f5
        f4.save()
        f5.parent = f4
        f5.save()

        try:
            len(f4.get_all_ancestor_folders())
            len(f5.get_all_ancestor_folders())
        except RuntimeError:
            self.fail("Folder's parents are recursive!")

    def test_duplicate_folders(self):
        """
        Test that a folder cannot have the same name as another folder with the same parent
        """
        logging.info('Test same level duplicate folder names...')

        f7 = Folder.objects.get(name="f7")
        f6 = Folder.objects.get(name="f6")
        f6.parent = f7
        f6.save()

        ff6 = Folder.objects.create(name="f6", parent= f7)
        try:
            Folder.objects.get(name="f6")
        except Exception:
            self.fail("Folder has the same name as another folder in the same directory")
