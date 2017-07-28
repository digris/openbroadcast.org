import os
import sys
import re
import raven
from django.conf import settings

BASE_DIR = getattr(settings, 'BASE_DIR')

# external modules are sylinked to dev folder. on production they are installed via pip
sys.path.insert(0, os.path.join(BASE_DIR, 'dev'))

INTERNAL_IPS = ('127.0.0.1',)
DEBUG = True
ALLOWED_HOSTS = ['*',]

EXPORTER_DEBUG = False

# non-async behaviour
# IMORTER_USE_CELERYD = False
# EXPORTER_USE_CELERYD = False
# ALIBRARY_USE_CELERYD = False
# ABCAST_USE_CELERYD = False
# MEDIA_ASSET_USE_CELERYD = True
# PYPO_USE_CELERYD = False
#CELERY_ALWAYS_EAGER = True

IMORTER_AUTOIMPORT_MB = True

EL_PAGINATION_PER_PAGE = 4


# async behaviour
IMORTER_USE_CELERYD = True
EXPORTER_USE_CELERYD = True
ALIBRARY_USE_CELERYD = True
ABCAST_USE_CELERYD = False
MEDIA_ASSET_USE_CELERYD = True
PYPO_USE_CELERYD = False

ALIBRARY_PAGINATE_BY_DEFAULT = 12

TASTYPIE_FULL_DEBUG = True

# newsletter config / subscription app
MAILCHIMP_API_KEY = ''
SUBSCRIPTION_DEFAULT_LIST_ID = 1
SUBSCRIPTION_WEBHOOK_TOKEN = 'VR-BW-XZ-BO'

#CELERY_CHORD_PROPAGATES = True


COMPRESS_OFFLINE = False
COMPRESS_ENABLED = False

NUNJUCKS_DEBUG = True
THUMBNAIL_DEBUG = False

SECRET_KEY = '0r6%7gip5tmez*vygfv+u14h@4lbt^8e2^26o#5_f_#b7%cm)u'
LEGACY_STORAGE_ROOT = '/Users/ohrstrom/sshfs/obp_legacy/'

#MUSICBRAINZ_HOST = '172.20.10.209:5000'
MUSICBRAINZ_HOST = '10.40.10.210'
MUSICBRAINZ_RATE_LIMIT = False
DISCOGS_HOST = '172.20.10.207:8099/discogs-proxy'
#DISCOGS_HOST = 'localhost:8090'
DISCOGS_RATE_LIMIT = False

AUTO_SLUG_FIELD_MAX_UNIQUE_QUERY_ATTEMPTS = 1000


SESSION_COOKIE_NAME = 'org-openbroadcast-local-session'


CELERYD_TASK_SOFT_TIME_LIMIT = 360
CELERYD_TASK_TIME_LIMIT = 240

LANGUAGES = [
    ('en', 'en'),
]


if DEBUG:
    COMPRESS_DEBUG_TOGGLE = 'uncompressed'


# locations differ on os x when installed via homebrew
LAME_BINARY = '/usr/local/bin/lame'
SOX_BINARY = '/usr/local/bin/sox'
FAAD_BINARY = '/usr/local/bin/faad'
FFPROBE_BINARY = '/usr/local/bin/ffprobe'
FFMPEG_BINARY = '/usr/local/bin/ffmpeg'
ECHOPRINT_CODEGEN_BINARY = '/usr/local/bin/echoprint-codegen'


ADDTHIS_SETTINGS = {
    'PUB_ID': 'ra-572c880b2e9ced75',
}


PLAYOUT_BROKER_URL = 'amqp://obp:obp@127.0.0.1:5672/openbroadcast.org/playout'

MEDIA_ASSET_KEEP_DAYS = 10

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'org_openbroadcast_local',
        'USER': 'root',
        'HOST': '127.0.0.1',
        'PASSWORD': 'root',

    },
}


"""
available workers:
 - default        4
 - grapher        4
 - complete       8
 - convert        4
 - import         1
 - process        4
"""

CELERY_ROUTES = {
    #'importer.util.importer_tools.mb_complete_artist_task' : {'queue': 'complete'},
    #'importer.util.importer_tools.mb_complete_media_task' : {'queue': 'complete'},
    #'importer.util.importer_tools.mb_complete_release_task' : {'queue': 'complete'},
}


__CELERY_ROUTES = {
    # assign import task to single-instance worker
    'importer.models.import_task': {'queue': 'import'},
    'importer.models.identify_task': {'queue': 'process'},
    'importer.util.importer_tools.mb_complete_media_task': {'queue': 'complete'},
    'alibrary.models.generate_media_versions_task': {'queue': 'convert'},
    'alibrary.models.create_waveform_image': {'queue': 'convert'},
    'media_asset.models.process_waveform': {'queue': 'grapher'},
    'media_asset.models.process_format': {'queue': 'convert'},
    'media_asset.process_format': {'queue': 'convert'},
}

CELERY_ROUTES = {

    #
    'media_asset.models.process_waveform': {'queue': 'grapher'},
    'media_asset.models.process_format': {'queue': 'convert'},
    'media_asset.process_waveform': {'queue': 'grapher'},
    'media_asset.process_format': {'queue': 'convert'},
    'media_asset.tasks.process_waveform': {'queue': 'grapher'},
    'media_asset.tasks.process_format': {'queue': 'convert'},
}


"""
celery -A project worker -Q celery -c 4
celery -A project worker -Q process -c 4
celery -A project worker -Q import -c 1
celery -A project worker -Q complete -c 4
celery -A project worker -Q grapher -c 2
celery -A project worker -Q convert -c 2
"""



CELERYD_MAX_TASKS_PER_CHILD = 1
#CELERY_TASK_SERIALIZER = "json"


#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
CELERY_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


POSTMAN_MAILER_APP = 'debug'

# streaming settings
RTMP_HOST = 'local.openbroadcast.org'
RTMP_APP = 'alibrary'
RTMP_PORT = '1935'

APLAYER_STREAM_MODE = 'html5' # or 'rtmp' 'html5'

PUSHY_SETTINGS = {
    'MODELS': (
        'alibrary.playlist',
        'alibrary.media',
        'importer.import',
        'importer.importfile',
        'abcast.emission',
        'exporter.export',
        'abcast.channel',
    ),
    'SOCKET_SERVER': '//local.openbroadcast.org:8180/',
    'CHANNEL_PREFIX': 'org_openbroadcast_prod_',
    'REDIS_HOST': '127.0.0.1',
    'DEBUG': DEBUG
}


ANALYTICS_ACCOUNT = 'UA-28856125-1'

#STATIC_URL = 'http://127.0.0.1:8000/static/'
#MEDIA_URL = 'http://127.0.0.1:8000/media/'

DEV_APPS = ()

MIDDLEWARE_CLASSES += (
    #'devserver.middleware.DevServerMiddleware',
)
# INSTALLED_APPS += (
#    'devserver',
# )

# devserver neets to come early in installed apps
INSTALLED_APPS = (
   #'devserver',
) + INSTALLED_APPS


POST_MORTEM = False


RAVEN_CONFIG = {}

# authentication settings (3rd party)
FACEBOOK_APP_ID = '213000778729132'
FACEBOOK_API_SECRET = '1e14a8932f1c71c51872ec2ad79d680e'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]

GOOGLE_OAUTH2_CLIENT_ID = '156254740327-tfocn6kqllr23vn14ggrd6nij31bmhi9.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'esB0FzmXUU_9A7iDsNH_s93V'

TWITTER_CONSUMER_KEY = 'YaIWfHDcIQGpJ8ogFZLcnnlQe'
TWITTER_CONSUMER_SECRET = 'bEso5Y4A6ZVOZvO9g4voD9HnxWvuwDRKPjkz7gFkcivx69rK2W'

SOUNDCLOUD_CLIENT_ID = '5e64699b445fdc904297f120967072c9'
SOUNDCLOUD_CLIENT_SECRET = '905f80e28509b8894746898f0d2c1520'

DROPBOX_APP_ID = 'hysrslzv780iu8n'
DROPBOX_API_SECRET = '5y9ldihkc9ot6cz'

GITHUB_APP_ID = '93b8c5a82ee21f19e4c3'
GITHUB_API_SECRET = 'a2602afb10e29096b101e3b698403996a6e86d70'



DEVSERVER_MODULES = (
    #'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    #'devserver.modules.profile.LineProfilerModule',
)

DEVSERVER_IGNORED_PREFIXES = [
    '/media',
    '/uploads',
    '/static',
]

DEVSERVER_FILTER_SQL = (
    re.compile('alibrary_\w+'),  # Filter all queries related to Celery
)

DEVSERVER_DEFAULT_ADDR = '0.0.0.0'
DEVSERVER_DEFAULT_PORT = '8080'


# file delivery
#SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_BACKEND = 'sendfile.backends.simple'

SENDFILE_ROOT = '/Users/ohrstrom/Documents/Code/openbroadcast.org/website/media/private'
SENDFILE_URL = '/media/private'


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = 'sessions'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "template_cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

ADV_CACHE_BACKEND = 'template_cache'

CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
    'socket_timeout': 3,
}

CACHEOPS = {
    'auth.user': ('get', 60*15),
    'auth.group': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60*24},
    'alibrary.*': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60*24},
    'alibrary.media': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60*24, 'cache_on_save': True},
    'alibrary.playlist': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60*24, 'cache_on_save': True},
    'alibrary.license': {'ops': ('fetch', 'get', 'count'), 'timeout': 1},
    'tagging.*': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60},
    'arating.*': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60*24},
}
CACHEOPS_DEGRADE_ON_FAILURE=False
CACHEOPS_FAKE = False


# to disable caches:
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'template_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
CACHEOPS_FAKE = True

# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'org_openbroadcast',
#         'INCLUDE_SPELLING': False,
#     },
# }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'search.backends.UnstemmedElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'org_openbroadcast_aaa',
    },
}

# filer
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'media/filer'),
                'base_url': '/media/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'media/filer_thumbnails'),
                'base_url': '/media/filer_thumbnails/',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'smedia/filer'),
                'base_url': '/smedia/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.join(BASE_DIR, 'smedia/filer_thumbnails'),
                'base_url': '/smedia/filer_thumbnails/',
            },
        },
    },
}

DEFAULT_FILER_SERVERS = {
    'private': {
        'main': {
            'ENGINE': 'filer.server.backends.default.DefaultServer',
        },
        'thumbnails': {
            'ENGINE': 'filer.server.backends.default.DefaultServer',
        }
    }
}

DOCS_ROOT = '/Users/ohrstrom/code/openbroadcast/documentation/doc/_build/html/'
#DOCS_ROOT = '/Users/ohrstrom/code/service.valleyelectronics.me/docs/_build/html/'
DOCS_ACCESS = 'login_required'



OPBEAT = {
    'ORGANIZATION_ID': '8e0a58b5230a4f809a910e0dd967a837',
    'APP_ID': '24231efd3c',
    'SECRET_TOKEN': 'bdfccf865a357f5c499083d0802af92b431ffe97',
}

def skip_static_requests(record):
    if record.args[0].startswith('GET /static/'):  # filter whatever you want
        return False
    return True


from colorlog import ColoredFormatter
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        # use Django's built in CallbackFilter to point to your filter
        'skip_static_requests': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_static_requests
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
        'debug': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(lineno)-4s%(name)-24s %(levelname)-8s %(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'bold_green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'colored'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {
                'custom-tag': 'django-error',
            },
        },
    },
    'loggers': {
        'root': {
            'level': 'ERROR',
            'handlers': ['sentry'],
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['null',],
            'propagate': False
        },
        'django': {
            'handlers': ['null',],
            'level': 'DEBUG',
            'propagate': True,
            'filters': ['skip_static_requests'],
        },
        'basehttp': {
            'handlers': ['null',],
            'level': 'DEBUG',
            'propagate': True,
            'filters': ['skip_static_requests'],
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['skip_static_requests'],
        },
        'caching': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False
        },
        'alibrary': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'abcast': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'importer': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'exporter': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'media_asset': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'metadata_generator': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'social_auth': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False
        },
        'obp_legacy': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'lib.icecast': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'pushy': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'changetracker': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'postman': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'requests': {
            'handlers': ['null'],
            'level': 'ERROR',
            'propagate': False
        },
        'devserver': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'autopilot': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'elasticsearch': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        'base': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'ep': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(lineno)-4s%(name)-24s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console',],
            'propagate': False
        },
        'urllib3': {
            'level': 'WARNING',
            'handlers': ['console',],
            'propagate': False
        },
    },
}
