from .base import *

DEBUG = True

MEDIA_URL = '/media/'


ALLOWED_HOSTS = ['127.0.0.1', '56043181.ngrok.io']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  }
}

