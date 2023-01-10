"""
Production Settings
"""
import os
from .base import *

DEBUG = True
SECRET_KEY = '8)x&v&*71f!j36leq1s0czpil=!50pop7qx4e(&gyo8t_pg=lj'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# STATIC
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]

# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

