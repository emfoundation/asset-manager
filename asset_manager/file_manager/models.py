from django.conf import settings
from django.db import models

from model_utils import FieldTracker

from . import utils
from . import s3_utils

# Create your models here.
class S3_Object(models.Model):
    name = models.CharField(max_length=64)
    s3_key = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.s3_key

class Folder(S3_Object):

    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    tracker = FieldTracker()

    def get_path(self):
        if not self.parent:
            return settings.MEDIAFILES_LOCATION + '/' + self.name
        else:
            return self.parent.get_path() + '/' + self.name

    def get_files(self):
        return self.file_set.all()

    def get_all_descendants(self, include_self=False):

        descendants=[]

        def get_descendants(self):
            descendants.append(self)
            for asset in self.asset_set.all():
                descendants.append(asset)
            child_folders = self.folder_set.all()
            for folder in child_folders:
                get_descendants(folder)

        get_descendants(self)

        if not include_self:
            descendants.remove(self)

        return descendants

    def update_s3_keys(self):
        """
        When a Folder model has been updated, this function will
        update the s3_keys of it and its children
        """
        # first update folder
        old_s3_key = self.tracker.previous('s3_key')
        # generate and set new s3_key from current name + file tree position
        new_s3_key = (self.get_path() + '/').lower()
        self.s3_key = new_s3_key

        s3_utils.update_s3_key(old_s3_key, new_s3_key)

        # then update descendants
        objects = self.get_all_descendants()
        for object in objects:
            old_s3_key = object.s3_key

            if type(object) is Folder:
                new_s3_key = (object.get_path() + '/').lower()
                object.s3_key = new_s3_key

            elif type(object) is Asset:
                new_s3_key = object.get_path().lower()
                object.s3_key = new_s3_key
                object.file.name = utils.get_file_directory_path(object, object.filename())

            s3_utils.update_s3_key(old_s3_key, new_s3_key)
            object.save()

class Asset(S3_Object):
    parent = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=utils.get_file_directory_path)
    tracker = FieldTracker()

    def __str__(self):
        return self.parent.get_path() + '/' + self.name

    def get_path(self):
        return self.parent.get_path() + '/' + self.filename()

    # @TODO this must return JUST filename!
    def filename(self):
        # Asset.file.name contains the filename, until the model has been saved, then
        # it contains the full filepath, relative to MEDIAFILES_LOCATION
        # to get just the file name, we split the string from the right, once, on first '/'
        # if it contains any /'s
        filename = self.file.name
        if '/' in filename:
            return filename.rsplit('/',1)[1]
        return filename
