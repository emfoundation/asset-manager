from django.conf import settings

# from . import models
# from itertools import chain

def get_file_directory_path(instance, filename):
    """
    Returns an updated directory path for FileField uploads
    Because boto3 knows the base root, this must be removed
    Needs to have filename as a separate argument as this is expected when
    used as a callback by the uploads_to function on a FileField
    """
    path = instance.parent.get_path() + '/' + filename
    if path.startswith(settings.MEDIAFILES_LOCATION):
        path = path.partition('/')[2]
    return path.lower()
