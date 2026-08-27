import sys
import warnings
from datetime import timedelta
from pathlib import Path

import environ

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_ROOT = PROJECT_ROOT / "obp_core"

sys.path.insert(0, str(APP_ROOT))

sys.path.insert(0, str(APP_ROOT / "base"))
sys.path.insert(0, str(APP_ROOT / "legacy_apps"))
sys.path.insert(0, str(APP_ROOT / "legacy_deps"))

env = environ.Env(
    DEBUG=(bool, False),
    DATABASE_URL=(str, "sqlite:///dev/null"),
    MEDIA_ROOT=(str, str(PROJECT_ROOT / "data" / "media")),
    ELASTICSEARCH_URL=(str, "localhost:9200"),
    #
    SITE_URL=(str, "http://obp-next.local:5000"),
    ALLOWED_HOSTS=(list, ["*"]),
    # binaries
    FFPROBE_BINARY=(str, "/usr/bin/ffprobe"),
    FFMPEG_BINARY=(str, "/usr/bin/ffmpeg"),
    LAME_BINARY=(str, "/usr/bin/lame"),
    ECHOPRINT_CODEGEN_BINARY=(str, "/usr/local/bin/echoprint-codegen"),
    # services
    MUSICBRAINZ_HOST=(str, "musicbrainz.org"),
    DISCOGS_HOST=(str, "api.discogs.com"),
    #
    MEDIA_PREFLIGHT_SERVICE_ENDPOINT=(
        str,
        "https://media-preflight-service-888119763922.europe-west6.run.app/",
    ),
    MEDIA_PREFLIGHT_SERVICE_TOKEN=(str, ""),
    #
    WAVEFORM_SERVICE_ENDPOINT=(str, "http://10.10.8.202:2001/"),
)

env.read_env(env.str("ENV_PATH", ".env"))

#######################################################################
# ?
#######################################################################
DEBUG = env("DEBUG")

SECRET_KEY = env(
    "SECRET_KEY",
    default="---secret-key---",
)

SITE_ID = 1

SITE_URL = env("SITE_URL")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "Englisch"),
]

USE_I18N = False
USE_L10N = True
DATETIME_FORMAT = "Y-m-d H:i"
DATE_FORMAT = "Y-m-d"
SHORT_DATE_FORMAT = "Y-m-d"

CONTACT_EMAIL = "jonas.ohrstrom@digris.ch"
ADMINS = (("Admin", "jonas.ohrstrom@digris.ch"),)
MANAGERS = ADMINS


#######################################################################
# django base settings
#######################################################################
ROOT_URLCONF = "config.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.syndication",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # server
    "corsheaders",
    "gunicorn",
    "django_date_extensions",
    "django_elasticsearch_dsl",
    "search",
    "addthis",
    # tools
    "django_extensions",
    "sendfile",
    # "djcelery_email",
    "el_pagination",
    "base",
    "api_base",
    #'notifications',
    "mailer",
    "django_countries",
    "l10n",
    "adv_cache_tag",
    "cacheops",
    "genericadmin",
    "hvad",
    "spurl",
    "pure_pagination",
    "crispy_forms_extra",
    "crispy_forms_vue",
    "crispy_forms",
    "floppyforms",
    "absolute",
    # asset and media handling
    "sekizai",
    "compressor",
    "easy_thumbnails",
    "versatileimagefield",
    "account",
    # navutils (to replace cms)
    "navutils",
    #
    "dajaxice",
    "dajax",
    # users / auth
    # 'avatar',
    "registration",
    "social_django",
    "captcha",
    "django_gravatar",
    "loginas",
    # api
    "tastypie",
    # api v2
    "api_extra",  # just styles for drf
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    # platform tools
    "fprint_client",
    # platform apps
    "object_actions",
    "profiles",
    "postman",
    "atracker",
    "invitation",
    "alibrary",
    "collection",
    "crawler",
    "media_asset",
    "media_preflight",
    "player",
    "importer",
    "massimporter",
    "exporter",
    "abcast",
    "autopilot",
    "arating",
    "statistics",
    "wikisyntax",
    "tagging",
    "tagging_extra",
    "ac_tagging",
    "actstream",
    "metadata_generator",
    "streaming_services",
    # platform tools
    "pushy",
    "nunjucks",
]


#######################################################################
# db
#######################################################################
DATABASES = {
    "default": {**env.db("DATABASE_URL"), "CONN_HEALTH_CHECKS": True},
    # "sync": env.db("DATABASE_URL_SYNC"),
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

#######################################################################
# static files / storage
#######################################################################
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# static
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
    "dajaxice.finders.DajaxiceFinder",
)

# `build` -> bundler output
STATICFILES_DIRS = [
    PROJECT_ROOT / "build" / "static",
    APP_ROOT / "static",
]

# 'dist' -> ./manage.py collectstatic output
STATIC_ROOT = PROJECT_ROOT / "dist" / "static"

STATIC_URL = "/static/"

# media
MEDIA_ROOT = env.str("MEDIA_ROOT")

MEDIA_URL = "/media/"

# compressor: to be removed
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = True

# avoid in-memory files (as we need fs access)
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# MAX_UPLOAD_SIZE = 256MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 268435456

SENDFILE_BACKEND = "sendfile.backends.simple"


#######################################################################
# middleware
#######################################################################
MIDDLEWARE_CLASSES = [
    "corsheaders.middleware.CorsMiddleware",
    "webpack.middleware.WebpackDevserverMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "account.middleware.SocialAuthExceptionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "base.middleware.xs_sharing.XsSharingMiddleware",
    "arating.middleware.AratingIpMiddleware",
]

#######################################################################
# templates
#######################################################################
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (
            APP_ROOT / "templates",
            APP_ROOT / "base" / "templates",
        ),
        "APP_DIRS": False,
        "OPTIONS": {
            "string_if_invalid": "INVALID: %s",
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "webpack.context_processors.webpack_devserver",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "sekizai.context_processors.sekizai",
                "navutils.context_processors.menus",
                "postman.context_processors.inbox",
                "django_settings_export.settings_export",
            ),
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django.template.loaders.eggs.Loader",
            ]
            if DEBUG
            else [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "django.template.loaders.eggs.Loader",
                    ],
                )
            ],
        },
    }
]

NAVUTILS_MENU_CONFIG = {
    "CURRENT_MENU_ITEM_CLASS": "active selected",
    "CURRENT_MENU_ITEM_PARENT_CLASS": "active selected has-current",
}


#######################################################################
# binaries
#######################################################################
FFPROBE_BINARY = env.str("FFPROBE_BINARY")
FFMPEG_BINARY = env.str("FFMPEG_BINARY")
LAME_BINARY = env.str("LAME_BINARY")
ECHOPRINT_CODEGEN_BINARY = env.str("ECHOPRINT_CODEGEN_BINARY")


#######################################################################
# services
#######################################################################
MUSICBRAINZ_HOST = env.str("MUSICBRAINZ_HOST")
DISCOGS_HOST = env.str("DISCOGS_HOST")

MEDIA_PREFLIGHT_SERVICE_ENDPOINT = env.str("MEDIA_PREFLIGHT_SERVICE_ENDPOINT")
MEDIA_PREFLIGHT_SERVICE_TOKEN = env.str("MEDIA_PREFLIGHT_SERVICE_TOKEN")

WAVEFORM_SERVICE_ENDPOINT = env.str("WAVEFORM_SERVICE_ENDPOINT")

########################################################################
# search
#######################################################################
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": env.str("ELASTICSEARCH_URL"),
    },
}

# ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = "search.signals.CelerySignalProcessor"


#######################################################################
# exported settings
#######################################################################
SETTINGS_EXPORT = ["FACEBOOK_APP_ID", "SITE_URL"]


#######################################################################
# API v1 (to be removed)
#######################################################################
TASTYPIE_DEFAULT_FORMATS = ["json"]


#######################################################################
# API v2
#######################################################################
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}


#######################################################################
# authentication
#######################################################################
AUTH_USER_MODEL = "auth.User"
AUTH_PROFILE_MODULE = "profiles.Profile"
ANONYMOUS_USER_ID = -1
ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda u: (
        "/network/users/%s/" % u.profile.uuid if hasattr(u, "profile") else ""
    ),
}
LOGIN_URL = "/account/login/"
LOGOUT_URL = "/account/logout/"
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = LOGIN_URL
ACCOUNT_ACTIVATION_DAYS = 7
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "account.social_auth_backends.deezer.DeezerOAuth2",
    # "social_core.backends.spotify.SpotifyOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

# invitation
INVITATION_INVITE_ONLY = False
INVITATION_EXPIRE_DAYS = 10
INVITATION_INITIAL_INVITATIONS = 5

# social auth
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "account.social_auth_pipeline.user_details.get_details",
)

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_EMAIL_FORM_URL = "account:login"

# google oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/plus.me",
    "https://www.googleapis.com/auth/plus.login",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# deezer oauth2
SOCIAL_AUTH_DEEZER_KEY = ""
SOCIAL_AUTH_DEEZER_SECRET = ""
SOCIAL_AUTH_DEEZER_SCOPE = [
    "manage_library",
    "delete_library",
    "offline_access",
]


#######################################################################
# system checks
#######################################################################
SILENCED_SYSTEM_CHECKS = [
    "fields.W342",
]


#######################################################################
# use celery (make configurable via ENV)
#######################################################################
IMORTER_USE_CELERYD = True
EXPORTER_USE_CELERYD = True
ALIBRARY_USE_CELERYD = True
ABCAST_USE_CELERYD = True
MEDIA_ASSET_USE_CELERYD = True
PYPO_USE_CELERYD = True


#######################################################################
# email
#######################################################################
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_CONFIRMATION_DAYS = 5
EMAIL_DEBUG = DEBUG


#######################################################################
# messages
#######################################################################
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"


#####################################################################################
# celery / rabbitmq
#####################################################################################
CELERYD_MAX_TASKS_PER_CHILD = 1
CELERY_ACCEPT_CONTENT = ["pickle", "json"]
CELERY_TASK_SERIALIZER = "pickle"


CELERY_BROKER_URL = "amqp://obp:obp@127.0.0.1:5672/obp"
CELERY_RESULT_BACKEND = None

PLAYOUT_BROKER_URL = "amqp://obp:obp@127.0.0.1:5672/obp/playout"


CELERY_IMPORTS = (
    "importer.util.importer_tools",
    "base.pypo.gateway",
    # 'djcelery_email.tasks',
    #'media_asset.tasks',
    #'search.tasks',
)

CELERY_ROUTES = {
    "importer.models.import_task": {"queue": "import"},
    "importer.models.identify_task": {"queue": "process"},
    "importer.util.importer_tools.mb_complete_media_task": {"queue": "complete"},
    "importer.util.importer_tools.mb_complete_release_task": {"queue": "complete"},
    "importer.util.importer_tools.mb_complete_artist_task": {"queue": "complete"},
    "alibrary.models.generate_media_versions_task": {"queue": "convert"},
    "alibrary.models.create_waveform_image": {"queue": "convert"},
    "media_asset.tasks.process_assets_for_media": {"queue": "convert"},
    "media_asset.models.process_waveform": {"queue": "grapher"},
    "media_asset.models.process_format": {"queue": "convert"},
    "media_asset.process_waveform": {"queue": "grapher"},
    "media_asset.process_format": {"queue": "convert"},
    "media_asset.tasks.process_waveform": {"queue": "grapher"},
    "media_asset.tasks.process_format": {"queue": "convert"},
    "exporter.models.process_task": {"queue": "export"},
    "search.signals.handle_save_task": {"queue": "index"},
    "search.tasks.update_index": {"queue": "index"},
}

CELERYBEAT_SCHEDULE = {
    "exporter-cleanup": {
        "task": "exporter.models.cleanup_exports",
        "schedule": timedelta(seconds=660),
    },
    "importer-cleanup": {
        "task": "importer.models.reset_hanging_files",
        "schedule": timedelta(seconds=300),
    },
    "asset-cleanup": {
        "task": "media_asset.models.clean_assets",
        "schedule": timedelta(hours=24),
    },
}

CELERY_EMAIL_TASK_CONFIG = {"queue": "celery", "rate_limit": "50/m"}


#######################################################################
# pushy
#######################################################################
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
    "SOCKET_SERVER": "//localhost:5001/",
    "CHANNEL_PREFIX": "pushy_",
    "DEBUG": DEBUG,
}


#######################################################################
# 3rd party keys, ids etc
#######################################################################
RADIOPLAYER_API_STATION_ID = "obp"  # to be removed
RADIOPLAYER_API_USER = "obp"  # to be removed
RADIOPLAYER_API_PASSWORD = "obp"  # to be removed

# google related
GOOGLE_MAPS_API_KEY = "ABQIAAAAOHPJc2-0TzaYgfOquRJgtRR2_LvdznTgfqpGEUf18uq-dm_lmhSjdzKrt5n5UfFjwviK9F39LyXJng"

# facebook oauth settings
FACEBOOK_APP_ID = "108235479287674"
FACEBOOK_SECRET_KEY = "a5b0a3ce9f47d1eadaf004ffd9da4e1f"
FACEBOOK_API_SECRET = "a5b0a3ce9f47d1eadaf004ffd9da4e1f"
FACEBOOK_EXTENDED_PERMISSIONS = ["email", "publish_stream"]

# echonest analyzer
ECHONEST_API_KEY = "DC7YKF3VYN7R0LG1M"


#######################################################################
# app specific settings
#######################################################################

# pagination
PAGINATION_SETTINGS = {
    "PAGE_RANGE_DISPLAYED": 6,
    "MARGIN_PAGES_DISPLAYED": 3,
}

# thumbnails
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.filters",
    "easy_thumbnails.processors.scale_and_crop",
)
THUMBNAIL_QUALITY = 80
THUMBNAIL_BASEDIR = "thumbnails"
THUMBNAIL_PRESERVE_EXTENSIONS = ("png",)
THUMBNAIL_ALIASES = {
    "": {
        "thumbnail_240": {
            "size": (240, 240),
            "upscale": True,
            "crop": True,
            "quality": 80,
        }
    }
}

# postman
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_SHOW_USER_AS = "get_full_name"

# wikisyntax
WIKISYNTAX = (
    ("r", "alibrary.util.object_linker.WikiRelease"),
    ("a", "alibrary.util.object_linker.WikiArtist"),
    ("l", "alibrary.util.object_linker.WikiLabel"),
)
WIKISYNTAX_DISABLE_CACHE = False

# actstream
ACTSTREAM_SETTINGS = {
    "MODELS": (
        "auth.user",
        "auth.group",
        "alibrary.release",
        "alibrary.playlist",
        "alibrary.artist",
        "alibrary.media",
        "alibrary.label",
        "abcast.emission",
        "abcast.station",
    ),
    "FETCH_RELATIONS": True,
    "USE_PREFETCH": True,
    "GFK_FETCH_DEPTH": 1,
}

# date extension
DATE_EXTENSIONS_DATE_INPUT_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d.%m.%Y",
    "%d/%m/%y",  # '2006-10-25', '25/10/2006', '13/11/2020'
    "%b %d %Y",
    "%b %d, %Y",  # 'Oct 25 2006', 'Oct 25, 2006'
    "%d %b %Y",
    "%d %b, %Y",  # '25 Oct 2006', '25 Oct, 2006'
    "%B %d %Y",
    "%B %d, %Y",  # 'October 25 2006', 'October 25, 2006'
    "%d %B %Y",
    "%d %B, %Y",  # '25 October 2006', '25 October, 2006'
)

# captcha
CAPTCHA_LETTER_ROTATION = (-12, 12)
CAPTCHA_BACKGROUND_COLOR = "#ffffff"
CAPTCHA_FOREGROUND_COLOR = "#333333"
CAPTCHA_CHALLENGE_FUNCT = "captcha.helpers.random_char_challenge"
CAPTCHA_NOISE_FUNCTIONS = ("captcha.helpers.noise_dots",)
CAPTCHA_FILTER_FUNCTIONS = ()
CAPTCHA_PUNCTUATION = """_"',.;:-"""
CAPTCHA_LENGTH = 8
CAPTCHA_IMAGE_SIZE = (160, 28)
CAPTCHA_FIELD_TEMPLATE = "captcha/field.html"


#######################################################################
# to be checked - already marked as depreciated ~10 years ago :)
# but maybe still in use...
#######################################################################
FORMATS_MEDIA = {"mp3": ["base"]}
AJAX_LOOKUP_CHANNELS = {"aliases": {"model": "alibrary.artist", "search_field": "name"}}
BLEACH_ALLOWED_TAGS = ["p", "b", "i", "u", "em", "strong", "a"]
BLEACH_STRIP_TAGS = True
FORMATS_STREAM = {"mp3": [128]}
FORMATS_DOWNLOAD = {"mp3": [192], "flac": ["base"], "wav": ["base"]}
WAVEFORM_SIZES = {"s": [100, 20], "m": [300, 30], "l": [600, 100]}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True
EMAIL_CONFIRMATION_DAYS = 5


#######################################################################
# logging
#######################################################################
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(lineno)-4s%(name)-24s %(levelname)-8s %(message)s"}
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
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
            "handlers": ["default"],
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


#######################################################################
# silence known warnings
# see: pyproject.toml
#######################################################################
warnings.filterwarnings(
    "ignore",
    message=r"pkg_resources is deprecated as an API.*",
    category=UserWarning,
    module=r"adv_cache_tag",
)

warnings.filterwarnings(
    "ignore",
    message=r"Unable to import floppyforms\.gis.*",
    category=UserWarning,
    module=r"floppyforms",
)