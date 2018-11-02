from .base import *

DEBUG = True

MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'), # test_db
        'USER': config('DB_USER'), # test_user
        'PASSWORD': config('DB_PASSWORD'), # test_password
        'HOST': config('DB_HOST'), # 127.0.0.1 
        'PORT': '5432',
    }
}





