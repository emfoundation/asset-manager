from django.conf import settings

from django.db.models import signals
from django.dispatch import receiver

from .models import Asset, Folder

from . import s3_utils

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# logging.disable(logging.CRITICAL)

# ------------ Folder Signals ------------ #

@receiver(signals.pre_save, sender=Folder)
def generate_s3_folder_key(sender, instance, **kwargs):
    """
    When a Folder is saved, updates its s3 key based on its name and location
    in the local file system
    """
    instance.s3_key = (instance.get_path() + '/').lower()

@receiver(signals.post_save, sender=Folder)
def save_folder_to_s3(sender, instance, created, **kwargs):
    """
    When a Folder is saved, will update S3 Object, and its children, accordingly
    """
    if created:
        s3_utils.create_s3_folder(instance.s3_key)
    elif instance.tracker.has_changed('name') or instance.tracker.has_changed('parent_id'):
        instance.update_s3_keys()

@receiver(signals.post_delete, sender=Folder)
def delete_folder(sender, instance, **kwargs):
    """
    When a Folder is deleted, deletes the corresponding S3 object
    """
    s3_utils.delete_s3_object(instance.s3_key)


# ------------ Asset Signals ------------ #

@receiver(signals.pre_save, sender=Asset)
def generate_s3_file_key(sender, instance, **kwargs):
    """
    When an Asset is created, will generate an S3 Key from the Asset model's
    location in the folder structure
    """
    # TODO on creation only?
    instance.s3_key = instance.get_path().lower()

@receiver(signals.post_save, sender=Asset)
def delete_old_file_on_new_file_upload(sender, created, instance, **kwargs):
    """
    When an Asset's file is updated to point at a new file, the old file must be deleted.
    """
    if not created:
        if instance.tracker.has_changed('file'):
            old_file = instance.tracker.previous('file')
            logging.info('File changed from {0} to {1}'.format(old_file.name, instance.file.name))
            s3_utils.delete_s3_object(settings.MEDIAFILES_LOCATION + '/' + instance.tracker.previous('file').name)

@receiver(signals.post_delete, sender=Asset)
def delete_file(sender, instance, **kwargs):
    """
    When an Asset is deleted, will delete the corresponding S3 Object
    """
    s3_utils.delete_s3_object(instance.s3_key)
