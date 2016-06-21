import os
import sys
import re
from django.conf import settings

BASE_DIR = getattr(settings, 'BASE_DIR')

sys.path.insert(0, os.path.join(BASE_DIR, 'dev'))

DEBUG = False

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'default.sqlite3'),
    # },

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'org_openbroadcast_local',
        'USER': 'ohrstrom',
        'PASSWORD': 'sd',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            #'autocommit': True,
        }
    },

    'legacy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'legacy.sqlite3'),
    },
    'legacy_legacy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'legacy_legacy.sqlite3'),
    },
}

