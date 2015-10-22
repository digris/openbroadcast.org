import os
import sys
from django.conf import settings

BASE_DIR = getattr(settings, 'BASE_DIR')

# external modules are sylinked to dev folder. on production they are installed via pip
sys.path.insert(0, os.path.join(BASE_DIR, 'dev'))

INTERNAL_IPS = ('127.0.0.10',)
DEBUG = True

EXPORTER_DEBUG = DEBUG

IMORTER_USE_CELERYD = False

TASTYPIE_FULL_DEBUG = True


#CELERY_ALWAYS_EAGER = True
#CELERY_CHORD_PROPAGATES = True


COMPRESS_OFFLINE = False
COMPRESS_ENABLED = False

NUNJUCKS_DEBUG = True
THUMBNAIL_DEBUG = False

SECRET_KEY = '0r6%7gip5tmez*vygfv+u14h@4lbt^8e2^26o#5_f_#b7%cm)u'
LEGACY_STORAGE_ROOT = '/Users/ohrstrom/sshfs/obp_legacy/'

MUSICBRAINZ_HOST = '172.20.10.209:5000'
MUSICBRAINZ_RATE_LIMIT = False
DISCOGS_HOST = '172.20.10.207:8099/discogs-proxy'
#DISCOGS_HOST = 'localhost:8090'
DISCOGS_RATE_LIMIT = False


SESSION_COOKIE_NAME = 'org-openbroadcast-local-session'


CELERYD_TASK_SOFT_TIME_LIMIT = 60
CELERYD_TASK_TIME_LIMIT = 240


if DEBUG:
    COMPRESS_DEBUG_TOGGLE = 'uncompressed'

LAME_BINARY = '/usr/local/bin/lame'
SOX_BINARY = '/usr/local/bin/sox'
FAAD_BINARY = '/usr/local/bin/faad'

DATABASES = {
    
    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': 'org_openbroadcast_local',
    #    'USER': 'dev',
    #    'PASSWORD': 'dev',
    #    'HOST': '',
    #    'OPTIONS': {
    #        'autocommit': True,
    #    }
    #},
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'org_openbroadcast_local_upgrade',
        #'NAME': 'org_openbroadcast_local_full',
        #'NAME': 'dumptester',
        'USER': 'root',
        'HOST': '127.0.0.1',    
        'PASSWORD': 'root',
        'OPTIONS': {
               "init_command": "SET storage_engine=INNODB",
        },

    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'data.db'),
        'NAME': '/Users/ohrstrom/srv/openbroadcast.org/data.db',
    },
    'legacy': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'obp_legacy',                      # Or path to database file if using sqlite3.
        'NAME' : 'legacy_openbroadcast_medialibrary',
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'legacy_legacy': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'obp_legacy',                      # Or path to database file if using sqlite3.
        'NAME' : 'legacy_openbroadcast',
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
    #
    'alibrary.models.mediamodels.create_waveform_image': {'queue': 'grapher'},
    'alibrary.models.mediamodels.create_versions_task' : {'queue': 'convert'},
    'alibrary.models.mediamodels.echonest_analyze_task' : {'queue': 'convert'},
    'alibrary.models.mediamodels.update_echoprint_task' : {'queue': 'convert'},
    #
    'exporter.models.cleanup_exports' : {'queue': 'process'},
    'exporter.models.process_task' : {'queue': 'convert'},
    #
    'importer.models.import_task' : {'queue': 'import'},
    'importer.models.process_task' : {'queue': 'process'},
    'importer.models.reset_hangin_files' : {'queue': 'process'},
    #
    'importer.util.importer.mb_complete_artist_task' : {'queue': 'complete'},
    'importer.util.importer.mb_complete_media_task' : {'queue': 'complete'},
    'importer.util.importer.mb_complete_release_task' : {'queue': 'complete'},
}
# debug -> to send jobs to default worker, use just {}
CELERY_ROUTES = {
    #'importer.util.importer.mb_complete_artist_task' : {'queue': 'complete'},
    #'importer.util.importer.mb_complete_media_task' : {'queue': 'complete'},
    #'importer.util.importer.mb_complete_release_task' : {'queue': 'complete'},
}

CELERYD_MAX_TASKS_PER_CHILD = 1


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
""""""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.anorg.net'
EMAIL_HOST_USER = 'smtp@anorg.net'
EMAIL_HOST_PASSWORD = 's3ndd@m@IL'

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
    'SOCKET_SERVER': 'http://local.openbroadcast.org:8180/',
    'CHANNEL_PREFIX': 'org_openbroadcast_prod_',
    'REDIS_HOST': '127.0.0.1',
    'DEBUG': DEBUG
}




SOLR_SERVER = {
    'host': 'localhost',
    'port': 8502,
}
TT_SERVER = {
    'host': 'localhost',
    'port': 1978,
}


ANALYTICS_ACCOUNT = 'UA-28856125-1'

#STATIC_URL = 'http://127.0.0.1:8000/static/'
#MEDIA_URL = 'http://127.0.0.1:8000/media/'

DEV_APPS = ()
DEBUG_APPS = (
              'debug_toolbar',
              'devserver',
              )

DEBUG_MIDDLEWARE = (
              'debug_toolbar.middleware.DebugToolbarMiddleware',
              )

POST_MORTEM = False


RAVEN_CONFIG = {
    'dsn': 'https://c534f44cc9aa4064ad1710e82bf8aeae:2bf75bd4de75406881e6b77d47fcb341@sentry.pbi.io/2',
}

# authentication settings (3rd party)
FACEBOOK_APP_ID = '213000778729132'
FACEBOOK_API_SECRET = '1e14a8932f1c71c51872ec2ad79d680e'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]

GOOGLE_OAUTH2_CLIENT_ID = '156254740327-tfocn6kqllr23vn14ggrd6nij31bmhi9.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'esB0FzmXUU_9A7iDsNH_s93V'

TWITTER_CONSUMER_KEY = 'YaIWfHDcIQGpJ8ogFZLcnnlQe'
TWITTER_CONSUMER_SECRET = 'bEso5Y4A6ZVOZvO9g4voD9HnxWvuwDRKPjkz7gFkcivx69rK2W'

#SOUNDCLOUD_CLIENT_ID = '5e64699b445fdc904297f120967072c9'
#SOUNDCLOUD_CLIENT_SECRET = '905f80e28509b8894746898f0d2c1520'

DROPBOX_APP_ID = 'hysrslzv780iu8n'
DROPBOX_API_SECRET = '5y9ldihkc9ot6cz'



DEVSERVER_MODULES = (
    #'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    #'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)
DEVSERVER_DEFAULT_ADDR = '0.0.0.0'
DEVSERVER_DEFAULT_PORT = '8080'


# debug settings
DEBUG_TOOLBAR_PANELS = (
    #'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    #'debug_toolbar.panels.headers.HeaderDebugPanel',
    #'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    #'debug_toolbar.panels.sql.SQLDebugPanel',
    #'debug_toolbar.panels.sql.SQLPanel',
    #'debug_toolbar.panels.logger.LoggingPanel',
    #'debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel',
    #'debug_toolbar_memcache.panels.memcache.MemcachePanel',
    ### below the ones used often!
    'debug_toolbar.panels.sql.SQLPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
)


# file delivery
#SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_BACKEND = 'sendfile.backends.simple'

SENDFILE_ROOT = '/Users/ohrstrom/Documents/Code/openbroadcast.org/website/media/private'
SENDFILE_URL = '/media/private'



__CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'org_openbroadcast_default',
        'TIMEOUT': 600,
    },
    'template_cache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'org_openbroadcast_template',
        'TIMEOUT': 600,
    },
}


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
    }
}

#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_CACHE_ALIAS = "default"
SESSION_ENGINE = "django.contrib.sessions.backends.db"


__CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'template_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
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
    #'alibrary.media': {'ops': ('fetch', 'get', 'count'), 'timeout': 1},
    #'cms.*': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60},
    #'menu.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},
    'tagging.*': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60},
    'arating.*': {'ops': ('fetch', 'get', 'count'), 'timeout': 60*60*24},
    #'postman.message': {'ops': ('count', 'fetch', 'get'), 'timeout': 60*60*24},
    'notifications.notification': {'ops': ('count'), 'timeout': 60*60*24},
}
CACHEOPS_DEGRADE_ON_FAILURE=False
CACHEOPS_FAKE = False




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

from colorlog import ColoredFormatter
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
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
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'colored'
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
            #'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False
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
        'media_asset': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'social_auth': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False
        },
        'requests': {
            'handlers': ['null'],
            'level': 'ERROR',
            'propagate': False
        },
        'template_timings_panel': {
            'handlers': ['null'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}

