import os
from project.settings import *

gettext = lambda s: s
_ = gettext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FILER_SUBJECT_LOCATION_IMAGE_DEBUG = False

DEBUG = True
FILER_DEBUG = DEBUG
USE_CAS_LOGIN = True

CMS_CACHE_PREFIX = 'com_reasonifly_cms'

ANALYTICS_CODE = 'aaa'
ANALYTICS_SITE = 'bbb'

RAVEN_CONFIG = {
    'dsn': 'https://43ca708796e04e148848fdd62922bdbe:a9a2d5f5f5cc49af9f0842215ff85887@sentry.pbi.io/13',
}

BRANDLINK = {
    'de': 'http://www.reasonifly.com/de/',
    'en': 'http://www.reasonifly.com/en/',
    'fr': 'http://www.reasonifly.com/fr/',
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'com_reasonifly_local',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
                    'init_command': 'SET storage_engine=INNODB',
                    }
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'debug': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {

        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['null',],
            'propagate': False
        },
        '': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False
        },
        'caching': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
