from django.conf import settings

from django.db.models import signals
from django.dispatch import receiver

from .models import Asset

from . import s3_utils

@receiver(signals.post_delete, sender=Asset)
def delete_file(sender, instance, **kwargs):
    """
    When an Asset is deleted, will delete the corresponding S3 Object
    """
    s3_key = settings.MEDIAFILES_LOCATION + '/' + instance.file.name
    s3_utils.delete_s3_object(s3_key)
