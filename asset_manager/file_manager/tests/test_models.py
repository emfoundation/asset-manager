from django.conf import settings
from django.test import TestCase
from django.db.models import signals

from file_manager.signals import delete_folder, save_folder_to_s3

from file_manager.models import Asset, Folder

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

# Create your tests here.
class FolderModelTests(TestCase):

    def setUp(self):
        signals.post_save.disconnect(save_folder_to_s3, sender=Folder)
        signals.post_delete.disconnect(delete_folder, sender=Folder)

    def tearDown(self):
        signals.post_save.connect(save_folder_to_s3, sender=Folder)
        signals.post_delete.connect(delete_folder, sender=Folder)

    def test_get_descendants_if_none_exist_inc_self_true(self):
        """
        get_all_descendants() should return the current_folder only, if it
        has no children and include_self is set to true
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        self.assertEqual(f1.get_all_descendants(True), [f1])
        f1.delete()

    def test_get_descendants_single_branch_inc_self_true(self):
        """
        get_all_descendants() should return the correct descendants for a single branch tree,
        including the current_folder if include_self is set to true
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f2)
        f3.save()
        self.assertEqual(set(f1.get_all_descendants(True)), set([f1, f2, f3]))
        f1.delete()

    def test_get_descendants_many_branches_inc_self_true(self):
        """
        get_all_descendants() should return the correct descendants for a multiple branch tree,
        including the current_folder if include_self is set to true
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f1)
        f3.save()
        f4 = Folder(name = 'folder4', parent = f1)
        f4.save()
        f5 = Folder(name = 'folder5', parent = f2)
        f5.save()
        f6 = Folder(name = 'folder6', parent = f2)
        f6.save()
        f7 = Folder(name = 'folder7', parent = f3)
        f7.save()
        f8 = Folder(name = 'folder8', parent = f6)
        f8.save()
        f9 = Folder(name = 'folder9', parent = f7)
        f9.save()
        f10 = Folder(name = 'folder10', parent = f7)
        f10.save()
        f11 = Folder(name = 'folder11', parent = f7)
        f11.save()
        f12 = Folder(name = 'folder12', parent = f10)
        f12.save()
        self.assertEqual(set(f1.get_all_descendants(True)), set([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]))
        f1.delete()

    def test_get_descendants_if_none_exist_inc_self_false(self):
        """
        get_all_descendants() should return empty, if it
        has no children and include_self is set to false
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        self.assertEqual(f1.get_all_descendants(), [])
        f1.delete()

    def test_get_descendants_single_branch_inc_self_false(self):
        """
        get_all_descendants() should return the correct descendants for a single branch tree,
        excluding the current_folder if include_self is set to false
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f2)
        f3.save()
        f4 = Folder(name = 'folder4', parent = f3)
        f4.save()
        self.assertEqual(set(f1.get_all_descendants()), set([f2, f3, f4]))
        f1.delete()

    def test_get_descendants_many_branches_inc_self_false(self):
        """
        get_all_descendants() should return the correct descendants for a multiple branch tree,
        excluding the current_folder if include_self is set to false
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f1)
        f3.save()
        f4 = Folder(name = 'folder4', parent = f1)
        f4.save()
        f5 = Folder(name = 'folder5', parent = f2)
        f5.save()
        f6 = Folder(name = 'folder6', parent = f2)
        f6.save()
        f7 = Folder(name = 'folder7', parent = f3)
        f7.save()
        f8 = Folder(name = 'folder8', parent = f6)
        f8.save()
        f9 = Folder(name = 'folder9', parent = f7)
        f9.save()
        f10 = Folder(name = 'folder10', parent = f7)
        f10.save()
        f11 = Folder(name = 'folder11', parent = f7)
        f11.save()
        f12 = Folder(name = 'folder12', parent = f10)
        f12.save()
        self.assertEqual(set(f1.get_all_descendants()), set([f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]))
        f1.delete()

    def test_get_descendants_single_branch_including_files_inc_self_false(self):
        """
        get_all_descendants should return the correct descendants for a single branch tree, including files,
        excluding the current_folder if include_self is set to false
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f2)
        f3.save()
        file1 = Asset(name = 'file1', parent = f3)
        file1.save()
        file2 = Asset(name = 'file2', parent = f3)
        file2.save()
        self.assertEqual(set(f1.get_all_descendants()), set([f2, f3, file1, file2]))
        f1.delete()

    def test_get_descendants_single_branch_including_files_inc_self_true(self):
        """
        get_all_descendants should return the correct descendants for a single branch tree, including files,
        including the current_folder if include_self is set to true
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f2)
        f3.save()
        file1 = Asset(name = 'file1', parent = f3)
        file1.save()
        file2 = Asset(name = 'file2', parent = f3)
        file2.save()
        self.assertEqual(set(f1.get_all_descendants(True)), set([f1, f2, f3, file1, file2]))
        f1.delete()

    def test_get_descendants_many_branch_including_files_inc_self_false(self):
        """
        get_all_descendants should return the correct descendants for a multiple branch tree, including files,
        excluding the current_folder if include_self is set to false
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f2)
        f3.save()
        f4 = Folder(name = 'folder4', parent = f1)
        f4.save()
        file1 = Asset(name = 'file1', parent = f3)
        file1.save()
        file2 = Asset(name = 'file2', parent = f3)
        file2.save()
        file3 = Asset(name = 'file3', parent = f4)
        file3.save()
        file4 = Asset(name = 'file4', parent = f4)
        file4.save()
        self.assertEqual(set(f1.get_all_descendants()), set([f2, f3, f4, file1, file2, file3, file4]))
        f1.delete()

    def test_get_descendants_many_branch_including_files_inc_self_true(self):
        """
        get_all_descendants should return the correct descendants for a multiple branch tree, including files,
        including the current_folder if include_self is set to true
        """
        f1 = Folder(name = 'folder1')
        f1.save()
        f2 = Folder(name = 'folder2', parent = f1)
        f2.save()
        f3 = Folder(name = 'folder3', parent = f2)
        f3.save()
        f4 = Folder(name = 'folder4', parent = f1)
        f4.save()
        file1 = Asset(name = 'file1', parent = f3)
        file1.save()
        file2 = Asset(name = 'file2', parent = f3)
        file2.save()
        file3 = Asset(name = 'file3', parent = f4)
        file3.save()
        file4 = Asset(name = 'file4', parent = f4)
        file4.save()
        self.assertEqual(set(f1.get_all_descendants(True)), set([f1, f2, f3, f4, file1, file2, file3, file4]))
        f1.delete()
