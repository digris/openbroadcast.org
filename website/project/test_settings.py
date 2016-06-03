import os
import sys
import re
from django.conf import settings

BASE_DIR = getattr(settings, 'BASE_DIR')

sys.path.insert(0, os.path.join(BASE_DIR, 'dev'))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'default.sqlite3'),
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

