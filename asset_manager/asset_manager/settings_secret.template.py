# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

ALLOWED_HOSTS = []


#--- AWS Settings ---#

# Default settings for S3 storage bucket, used by django-storages on the Asset file field
AWS_STORAGE_BUCKET_NAME = ''
AWS_S3_REGION_NAME = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

# Additional settings for backup and test buckets accessed directly
AWS_BACKUP_BUCKET_NAME = ''
AWS_BACKUP_BUCKET_REGION_NAME = ''

AWS_TEST_BUCKET_NAME = ''
AWS_TEST_BUCKET_REGION_NAME = ''


#--- Email settings ---#

ADMIN_EMAIL_ADDRESS = ''
ADMIN_EMAIL_PASSWORD = ''
RECIPIENT_EMAIL_ADDRESS = ''


#--- Database settings ---#

DATABASE_USER = ''
DATABASE_USER_PASSWORD = ''
DATABASE_NAME = ''


#--- Environment settings - development/staging/leave blank for production ---#

ENVIRONMENT = ''
