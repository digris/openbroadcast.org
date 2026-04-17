import os
import sys
from django.conf import settings

BASE_DIR = getattr(settings, "BASE_DIR")

# external modules are sylinked to dev folder. on production they are installed via pip
sys.path.insert(0, os.path.join(BASE_DIR, "dev"))

INTERNAL_IPS = ("127.0.0.11",)

DEBUG = True
ALLOWED_HOSTS = ["*"]

SITE_URL = "http://local.openbroadcast.org:8888"
# SITE_URL = 'http://ohrstrom-local.anorg.net'

EXPORTER_DEBUG = False


USE_I18N = False
USE_L10N = False

NGINX_X_ACCEL_REDIRECT = False

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"


# non-async behaviour
# IMORTER_USE_CELERYD = False
# EXPORTER_USE_CELERYD = False
# ALIBRARY_USE_CELERYD = False
# ABCAST_USE_CELERYD = False
# MEDIA_ASSET_USE_CELERYD = True
# PYPO_USE_CELERYD = False
# CELERY_ALWAYS_EAGER = True

IMORTER_AUTOIMPORT_MB = False

EL_PAGINATION_PER_PAGE = 4

# async behaviour
IMORTER_USE_CELERYD = False
EXPORTER_USE_CELERYD = True
ALIBRARY_USE_CELERYD = True
ABCAST_USE_CELERYD = False
MEDIA_ASSET_USE_CELERYD = True
PYPO_USE_CELERYD = False

ALIBRARY_PAGINATE_BY_DEFAULT = 12

TASTYPIE_FULL_DEBUG = True


# CELERY_CHORD_PROPAGATES = True


COMPRESS_OFFLINE = False
COMPRESS_ENABLED = False

NUNJUCKS_DEBUG = True
# NUNJUCKS_DEBUG = False
THUMBNAIL_DEBUG = False

NUNJUCKS_BIN = "/Users/ohrstrom/Documents/Code/openbroadcast.org/node_modules/nunjucks/bin/precompile"

SECRET_KEY = "0r6%7gip5tmez*vygfv+u14h@4lbt^8e2^26o#5_f_#b7%cm)u"

# MUSICBRAINZ_HOST = '172.20.10.209:5000'
# MUSICBRAINZ_HOST = '10.40.10.210'
# MUSICBRAINZ_HOST = 'musicbrainz.digris.net'
MUSICBRAINZ_HOST = "10.10.8.201"
MUSICBRAINZ_RATE_LIMIT = False
# DISCOGS_HOST = '172.20.10.207:8099/discogs-proxy'
# DISCOGS_HOST = '10.40.10.211:8000'
DISCOGS_HOST = "10.10.8.113:8000"
# DISCOGS_HOST = 'localhost:8090'
DISCOGS_RATE_LIMIT = False

# FPRINT_API_BASE_URL = 'http://172.20.10.240:8000/api/v1/'
# FPRINT_API_BASE_URL = 'http://10.40.10.214:8000/api/v1/'
FPRINT_API_BASE_URL = "http://127.0.0.1:7777/api/v1/"
# TODO: implement token on fprint API (only running in internal LAN)
# FPRINT_API_AUTH_TOKEN = 'f7b5f5abb5741505c70229f073bd85446658a842'
MIXDOWN_API_BASE_URL = "http://127.0.0.1:7778/api/v1/"
MIXDOWN_API_AUTH_TOKEN = "f7b5f5abb5741505c70229f073bd85446658a842"


# preflight api service
# MEDIA_PREFLIGHT_API_BASE_URL = "http://127.0.0.1:7779/api/v1/"  # depreciated
# MEDIA_PREFLIGHT_API_AUTH_TOKEN = "782b0b5795861e45a8087516734ff485e1b8a0d0"  # depreciated
MEDIA_PREFLIGHT_SERVICE_ENDPOINT = "http://127.0.0.1:5000/"
MEDIA_PREFLIGHT_SERVICE_TOKEN = "AAABBBCCC"

AUTO_SLUG_FIELD_MAX_UNIQUE_QUERY_ATTEMPTS = 1000
# changed in django-extensions 1.7.9
EXTENSIONS_MAX_UNIQUE_QUERY_ATTEMPTS = 1000


# radioplayer
RADIOPLAYER_API_STATION_ID = 155
RADIOPLAYER_API_USER = "ing_ob"
RADIOPLAYER_API_PASSWORD = "Swissradio1"


SESSION_COOKIE_NAME = "org-openbroadcast-local-session"


CELERYD_TASK_SOFT_TIME_LIMIT = 360
CELERYD_TASK_TIME_LIMIT = 240


LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", "Englisch"),
    # ('de', u'Deutsch'),
]


if DEBUG:
    COMPRESS_DEBUG_TOGGLE = "uncompressed"


# locations differ on os x when installed via homebrew
LAME_BINARY = "/opt/homebrew/bin/lame"
SOX_BINARY = "/opt/homebrew/bin/sox"
FAAD_BINARY = "/opt/homebrew/bin/faad"
FFPROBE_BINARY = "/opt/homebrew/bin/ffprobe"
FFMPEG_BINARY = "/opt/homebrew/bin/ffmpeg"
# ECHOPRINT_CODEGEN_BINARY = "/opt/homebrew/bin/echoprint-codegen"
ECHOPRINT_CODEGEN_BINARY = "/usr/bin/whoami"


ADDTHIS_SETTINGS = {"PUB_ID": "ra-572c880b2e9ced75"}

BROKER_URL = "amqp://obp:obp@127.0.0.1:5672/obp"
PLAYOUT_BROKER_URL = "amqp://obp:obp@127.0.0.1:5672/obp/playout"

MEDIA_ASSET_KEEP_DAYS = 10

CORS_ORIGIN_ALLOW_ALL = True


INSTALLED_APPS += [
    # 'debug_toolbar',
    # "dev"
]

MIDDLEWARE_CLASSES += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # "querycount.middleware.QueryCountMiddleware",
]

QUERYCOUNT = {
    "THRESHOLDS": {
        "MEDIUM": 30,
        "HIGH": 80,
        "MIN_TIME_TO_LOG": 0,
        "MIN_QUERY_COUNT_TO_LOG": 5,
    },
    "IGNORE_REQUEST_PATTERNS": [r"^/static/", r"^/admin/", r"^/jsi18n/"],
    "IGNORE_SQL_PATTERNS": [r"django_"],
    "DISPLAY_DUPLICATES": 1,
    "RESPONSE_HEADER": "X-QueryCount",
}

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.timer.TimerPanel",
    #'debug_toolbar.panels.settings.SettingsPanel',
    #'debug_toolbar.panels.headers.HeadersPanel',
    #'debug_toolbar.panels.request.RequestPanel',
    "debug_toolbar.panels.sql.SQLPanel",
    #'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    "debug_toolbar.panels.templates.TemplatesPanel",
    #'debug_toolbar.panels.cache.CachePanel',
    #'debug_toolbar.panels.signals.SignalsPanel',
    #'debug_toolbar.panels.logging.LoggingPanel',
    #'debug_toolbar.panels.redirects.RedirectsPanel',
]


DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "org_openbroadcast_local",  # local mariadb instance
    #     # 'NAME': 'org_openbroadcast_local_blank',
    #     "HOST": "10.35.30.231",
    #     "USER": "root",
    #     "PASSWORD": "root",
    #     "CONN_MAX_AGE": 600,
    # },
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "org_openbroadcast_full",
        "HOST": "127.0.0.1",
        "PORT": 3307,
        "USER": "root",
        "PASSWORD": "root",
        "CONN_MAX_AGE": 600,
    },
}

import pymysql
pymysql.version_info = (1, 2, 5)
pymysql.install_as_MySQLdb()


"""
available workers:
 - default        4
 - grapher        4
 - complete       8
 - convert        4
 - import         1
 - process        4
 - index        4
"""

# CELERY_ROUTES = {
#     'importer.util.importer_tools.mb_complete_artist_task' : {'queue': 'complete'},
#     'importer.util.importer_tools.mb_complete_media_task' : {'queue': 'complete'},
#     'importer.util.importer_tools.mb_complete_release_task' : {'queue': 'complete'},
# }
#
# CELERY_ROUTES = {
#     # assign import task to single-instance worker
#     'importer.models.import_task': {'queue': 'import'},
#     'importer.models.identify_task': {'queue': 'process'},
#     'importer.util.importer_tools.mb_complete_media_task': {'queue': 'complete'},
#     'alibrary.models.generate_media_versions_task': {'queue': 'convert'},
#     'alibrary.models.create_waveform_image': {'queue': 'convert'},
#     'media_asset.models.process_waveform': {'queue': 'grapher'},
#     'media_asset.models.process_format': {'queue': 'convert'},
#     'media_asset.process_format': {'queue': 'convert'},
# }

CELERY_ROUTES = {
    "media_asset.models.process_waveform": {"queue": "grapher"},
    "media_asset.models.process_format": {"queue": "convert"},
    "media_asset.process_waveform": {"queue": "grapher"},
    "media_asset.process_format": {"queue": "convert"},
    "media_asset.tasks.process_waveform": {"queue": "grapher"},
    "media_asset.tasks.process_format": {"queue": "convert"},
    "search.signals.handle_save_task": {"queue": "index"},
    #'search.tasks.update_index': {'queue': 'index'},
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
# CELERY_TASK_SERIALIZER = "json"


EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# DEFAULT_FROM_EMAIL = "Open Broadcast <webmaster@openbroadcast.org>"
# EMAIL_HOST = "mail.infomaniak.com"
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "smtp@digris.ch"
# EMAIL_HOST_PASSWORD = "5iDHLj3CR5KY"
# EMAIL_TIMEOUT = 120


POSTMAN_MAILER_APP = "debug"

# streaming settings
RTMP_HOST = "local.openbroadcast.org"
RTMP_APP = "alibrary"
RTMP_PORT = "1935"

PUSHY_SETTINGS = {
    "MODELS": (
        "alibrary.playlist",
        "alibrary.media",
        "importer.import",
        "importer.importfile",
        "abcast.emission",
        "exporter.export",
        "abcast.channel",
    ),
    # "SOCKET_SERVER": "//local.openbroadcast.org:8180/",  # running on localhost
    "SOCKET_SERVER": "/",  # running via docker compose
    "CHANNEL_PREFIX": "org_openbroadcast_dev_",
    "REDIS_HOST": "127.0.0.1",
    "DEBUG": DEBUG,
}


ANALYTICS_ACCOUNT = "UA-28856125-1"

# STATIC_URL = 'http://127.0.0.1:8000/static/'
# MEDIA_URL = 'http://127.0.0.1:8000/media/'

# MEDIA_URL = '{}{}'.format(SITE_URL, '/media/')

RAVEN_CONFIG = {}

# authentication settings (3rd party)
# FACEBOOK_APP_ID = '213000778729132'
# FACEBOOK_API_SECRET = '1e14a8932f1c71c51872ec2ad79d680e'
# FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]
#
# GOOGLE_OAUTH2_CLIENT_ID = '156254740327-tfocn6kqllr23vn14ggrd6nij31bmhi9.apps.googleusercontent.com'
# GOOGLE_OAUTH2_CLIENT_SECRET = 'esB0FzmXUU_9A7iDsNH_s93V'
#
# TWITTER_CONSUMER_KEY = 'YaIWfHDcIQGpJ8ogFZLcnnlQe'
# TWITTER_CONSUMER_SECRET = 'bEso5Y4A6ZVOZvO9g4voD9HnxWvuwDRKPjkz7gFkcivx69rK2W'
#
# SOUNDCLOUD_CLIENT_ID = '5e64699b445fdc904297f120967072c9'
# SOUNDCLOUD_CLIENT_SECRET = '905f80e28509b8894746898f0d2c1520'
#
# DROPBOX_APP_ID = 'hysrslzv780iu8n'
# DROPBOX_API_SECRET = '5y9ldihkc9ot6cz'
#
# GITHUB_APP_ID = '93b8c5a82ee21f19e4c3'
# GITHUB_API_SECRET = 'a2602afb10e29096b101e3b698403996a6e86d70'


# google oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "156254740327-tfocn6kqllr23vn14ggrd6nij31bmhi9.apps.googleusercontent.com"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "esB0FzmXUU_9A7iDsNH_s93V"

SOCIAL_AUTH_FACEBOOK_KEY = "213000778729132"
SOCIAL_AUTH_FACEBOOK_SECRET = "1e14a8932f1c71c51872ec2ad79d680e"

SOCIAL_AUTH_SOUNDCLOUD_KEY = "f009f9ca05053570a2c05d55f08f3dc8"
SOCIAL_AUTH_SOUNDCLOUD_SECRET = "ad689159fcecc12e14664084ab495874"


SOCIAL_AUTH_TWITTER_KEY = "vZ7nv4cgmF4CoazDx1cnQEFnS"
SOCIAL_AUTH_TWITTER_SECRET = "xh4nDx8PjcyX7dxMlSfo7Xhoy0tuwnGq1ljAwUz3GNL7CYNEut"

SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = "eec4v5yc42gsrwd"
SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = "pzktnbhyug705ah"

# testing deezer
SOCIAL_AUTH_DEEZER_KEY = "402044"
SOCIAL_AUTH_DEEZER_SECRET = "188a0faf34e829e6ae8b7acf8c03ad1f"

SOCIAL_AUTH_DEEZER_SCOPE = [
    "basic_access",
    "email",
    "manage_library",
    "delete_library",
    "offline_access",
]


# file delivery
# SENDFILE_BACKEND = 'sendfile.backends.nginx'
SENDFILE_BACKEND = "sendfile.backends.simple"

SENDFILE_ROOT = "/Users/ohrstrom/Documents/Code/openbroadcast.org/app/media/private"
SENDFILE_URL = "/media/private"


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"

ADV_CACHE_BACKEND = "template_cache"

CACHEOPS_REDIS = {"host": "localhost", "port": 6379, "db": 1, "socket_timeout": 3}

CACHEOPS = {
    "auth.user": {"ops": "get", "timeout": 60 * 15},
    "auth.group": {"ops": {"fetch", "get", "count"}, "timeout": 60 * 60 * 24},
    "alibrary.*": {"ops": {"fetch", "get", "count"}, "timeout": 60 * 60 * 24},
    "alibrary.artist": {
        "ops": {"fetch", "get", "count"},
        "timeout": 60 * 60 * 24,
        "cache_on_save": False,
    },
    "alibrary.media": {
        "ops": {"fetch", "get", "count"},
        "timeout": 60 * 60 * 24,
        "cache_on_save": False,
    },
    "alibrary.playlist": {
        "ops": {"fetch", "get", "count"},
        "timeout": 60 * 60 * 24,
        "cache_on_save": False,
    },
    "alibrary.license": {"ops": {"fetch", "get", "count"}, "timeout": 1},
    "tagging.*": {"ops": {"fetch", "get", "count"}, "timeout": 60 * 60},
    "arating.*": {"ops": {"fetch", "get", "count"}, "timeout": 60 * 60 * 24},
    "notifications.notification": {"ops": {"count"}, "timeout": 60 * 60 * 24},
    "easy_thumbnails.*": {"ops": {"fetch", "get"}, "timeout": 60 * 60},
}

CACHEOPS_DEGRADE_ON_FAILURE = False
CACHEOPS_FAKE = False


# caches:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     },
#     'template_cache': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     },
#     'crawler': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     },
#     "sessions": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/4",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     },
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "template_cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "crawler": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
}


#######################################################################
# search v2
#######################################################################
ELASTICSEARCH_DSL = {
    "default": {
        'hosts': 'localhost:9200',
        # "hosts": "10.35.30.231:9200"
        # 'hosts': '10.10.8.107:9200' # !! WARNING: this is the production instance !!
    }
}

# ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = "search.signals.CelerySignalProcessor"


NOTEBOOK_ARGUMENTS = [
    "--allow-root",
    "--ip",
    "0.0.0.0",
    "--port",
    "7777",
    #'--notebook-dir', '_notebooks',
]


DOCS_ROOT = "/Users/ohrstrom/code/openbroadcast/documentation/doc/_build/html/"
# DOCS_ROOT = '/Users/ohrstrom/code/service.valleyelectronics.me/docs/_build/html/'
DOCS_ACCESS = "login_required"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(lineno)-4s%(name)-24s %(levelname)-8s %(message)s"}
    },
    "handlers": {
        "graylog": {
            "level": "INFO",
            "class": "graypy.GELFHandler",
            "formatter": "standard",
            "host": "gojo.hazelfire.com",
            "port": 12201,
            "localname": "doga.obp-local-dev",
            "hostname": "local.openbroadcast.org",
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": os.path.join(os.path.dirname(BASE_DIR), "logs", "app-debug.log"),
        },
    },
    "loggers": {
        "": {"level": "WARNING", "handlers": ["default"], "propagate": True},
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "urllib3": {"level": "WARNING", "handlers": ["default"], "propagate": False},
        "elasticsearch": {"level": "INFO", "handlers": ["default"], "propagate": False},
        "social_django": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "django_elasticsearch_dsl": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        # platform applications
        "abcast": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "alibrary": {
            "level": "DEBUG",
            "handlers": ["default", "file"],
            "propagate": False,
        },
        "arating": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "autopilot": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "collection": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "crawler": {"level": "INFO", "handlers": ["default"], "propagate": False},
        "exporter": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "fprint_client": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "importer": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "massimporter": {"level": "DEBUG", "handlers": ["default"], "propagate": True},
        "media_asset": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "media_preflight": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "metadata_generator": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "object_actions": {
            "level": "DEBUG",
            "handlers": ["default"],
            "propagate": False,
        },
        "profiles": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "search": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "lib.icecast": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "pushy": {"level": "INFO", "handlers": ["default"], "propagate": False},
        "statistics": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "postman": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "base.audio": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "base.tunein": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "base.icecast": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
        "base.pypo": {"level": "DEBUG", "handlers": ["default"], "propagate": False},
    },
}