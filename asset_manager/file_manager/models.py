from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from model_utils import FieldTracker

from . import utils
from . import s3_utils

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

# Create your models here.
class S3_Object(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# ------------ Folders ------------#

class Folder(S3_Object):

    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    tracker = FieldTracker()

    def __str__(self):
        return self.get_path()

    def get_path(self):
        if not self.parent:
            return settings.MEDIAFILES_LOCATION + '/' + self.name
        else:
            return self.parent.get_path() + '/' + self.name

    def get_files(self):
        return self.file_set.all()

# ------------ Tags ------------#

class TagGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=64)
    group = models.ForeignKey(TagGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# ------------ Assets ------------#

class Asset(S3_Object):

    def get_s3_key(self, filename):
        return str(self.parent.id) + '/' + filename

    parent = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_s3_key)
    tags = models.ManyToManyField('Tag', blank=True)
    uploaded_by = models.ForeignKey(User, null=True)
    uploaded_at = models.DateTimeField(null=True)
    tracker = FieldTracker()

    def __str__(self):
        return self.parent.get_path() + '/' + self.name

    def save(self, *args, **kwargs):

        # if first save
        if not self.id:
            pass

        # if a new file is uploaded, will update filename even if parent has also changed...
        elif self.tracker.has_changed('file'):
            old_s3_key = settings.MEDIAFILES_LOCATION + '/' + self.tracker.previous('file').name
            s3_utils.delete_s3_object(old_s3_key)

        # but if file has not changed and parent has, must be handled manually
        elif self.tracker.has_changed('parent_id'):
            old_file_name = self.file.name
            self.file.name = str(self.parent.id) + '/' + self.get_filename()
            logging.info('Filename changed from {0} to {1}'.format(old_file_name, self.file.name))

            media_dir = settings.MEDIAFILES_LOCATION

            s3_utils.update_s3_key(media_dir + '/' + old_file_name, media_dir + '/' + self.file.name)

        super(Asset, self).save(*args, **kwargs)

    def get_path(self):
        return self.parent.get_path() + '/' + self.name
    get_path.short_description = 'Path'

    def get_filename(self):
        """
        Asset.file.name contains the full filepath, relative to MEDIAFILES_LOCATION ie 'parent_id/filename'
        To get just the filename, we split the string from the right, once, on first '/'
        """
        filename = self.file.name
        if '/' in filename:
            return filename.rsplit('/',1)[1]
        return filename
