from django.conf import settings

from django.db.models import signals
from django.dispatch import receiver

from .models import Folder

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
