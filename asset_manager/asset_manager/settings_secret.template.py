# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

ALLOWED_HOSTS = []

# AWS Settings

AWS_STORAGE_BUCKET_NAME = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

AWS_TEST_BUCKET_NAME = ''

# Static folder location
STATIC_ROOT = ''

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}
