import os

from os.path import (
    join,
    normpath
)

from payhere.settings.base import *

##################################################################
# Django Application configuration
##################################################################
DEBUG = True

##################################################################
# Static and Media settings
##################################################################
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = ()

##################################################################
# Databases settings
##################################################################
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'database',
        'PORT': '3306',
        'NAME': 'payhere',
        'USER': 'root',
        'PASSWORD': '12345',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
}
