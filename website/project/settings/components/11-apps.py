# -*- coding: utf-8 -*-
import os
from django.conf import settings

BASE_DIR = getattr(settings, "BASE_DIR")
DEBUG = getattr(settings, "DEBUG")

################################################################################
# django apps
################################################################################

INSTALLED_APPS = [
    #'djangocms_admin_style',
    #'django_slick_admin',
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
    "missing",  # http://django-missing.readthedocs.org/
    "raven.contrib.django.raven_compat",
    # 'raven.contrib.django.celery',
    "djcelery_email",
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
    "crispy_forms",
    "floppyforms",
    "absolute",
    # asset and media handling
    "sekizai",
    "compressor",
    "easy_thumbnails",
    "versatileimagefield",
    "account",
    # cms
    "cms",
    "menus",
    "treebeard",
    # cms plugins
    "djangocms_link",
    "djangocms_snippet",
    "djangocms_text_ckeditor",
    "djangocms_panel",
    "djangocms_column",
    "dajaxice",
    "dajax",
    "email_obfuscator",
    # users / auth
    # 'avatar',
    "registration",
    #'social_auth',
    "social_django",
    "captcha",
    "django_gravatar",
    "loginas",
    #'dropbox',
    #'provider',
    #'provider.oauth2',
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
    # legacy & migration
    "obp_legacy",
    # 'navutils',
    # platform tools
    "pushy",
    "nunjucks",
]


################################################################################
# app specific settings
################################################################################
PAGINATION_SETTINGS = {"PAGE_RANGE_DISPLAYED": 6, "MARGIN_PAGES_DISPLAYED": 3}

FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.TemporaryFileUploadHandler",)

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
################################################################################
# accounts / user handling
################################################################################
AUTH_USER_MODEL = "auth.User"
AUTH_PROFILE_MODULE = "profiles.Profile"
ANONYMOUS_USER_ID = -1
LOGIN_URL = "/account/login/"
LOGOUT_URL = "/account/logout/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_ACTIVATION_DAYS = 7
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    # "social_core.backends.soundcloud.SoundcloudOAuth2",
    # "social_core.backends.vk.VKOAuth2",
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.dropbox.DropboxOAuth2',
    # "social_core.backends.spotify.SpotifyOAuth2",
    # "obp_legacy.auth.backends.LegacyBackend",
    "django.contrib.auth.backends.ModelBackend",
)


################################################################################
# social auth
################################################################################
##################################################################
# social auth
##################################################################

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

# github
SOCIAL_AUTH_GITHUB_KEY = ""
SOCIAL_AUTH_GITHUB_SECRET = ""
SOCIAL_AUTH_GITHUB_SCOPE = ["user:email"]

# facebook
SOCIAL_AUTH_FACEBOOK_KEY = ""
SOCIAL_AUTH_FACEBOOK_SECRET = ""
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email", "public_profile"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id,name,email"}

# google oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/plus.me",
    "https://www.googleapis.com/auth/plus.login",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    #
    # 'https://www.googleapis.com/auth/contacts.readonly',
    # 'https://www.googleapis.com/auth/user.addresses.read',
    # 'https://www.googleapis.com/auth/user.birthday.read',
    # 'https://www.googleapis.com/auth/user.emails.read',
    # 'https://www.googleapis.com/auth/user.phonenumbers.read',
]

# vk
SOCIAL_AUTH_VK_OAUTH2_KEY = ""
SOCIAL_AUTH_VK_OAUTH2_SECRET = ""
# SOCIAL_AUTH_VK_OAUTH2_SCOPE = {
#     'fields': 'email',
# }

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email", "audio", "status"]

SOCIAL_AUTH_SPOTIFY_KEY = ""
SOCIAL_AUTH_SPOTIFY_SECRET = ""

SOCIAL_AUTH_SOUNDCLOUD_KEY = ""
SOCIAL_AUTH_SOUNDCLOUD_SECRET = ""


# invitation
INVITATION_INVITE_ONLY = False
INVITATION_EXPIRE_DAYS = 10
INVITATION_INITIAL_INVITATIONS = 5

LOGIN_ERROR_URL = LOGIN_URL


################################################################################
# Messaging
# https://bitbucket.org/psam/django-postman/wiki/Quick_Start_Guide
################################################################################

POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_AUTO_MODERATE_AS = True  # default is None
POSTMAN_SHOW_USER_AS = "get_full_name"

################################################################################
# wikisyntax, eg allows tor resolve [a:Artists Name] to object
################################################################################
WIKISYNTAX = (
    ("r", "alibrary.util.object_linker.WikiRelease"),
    ("a", "alibrary.util.object_linker.WikiArtist"),
    ("l", "alibrary.util.object_linker.WikiLabel"),
)
WIKISYNTAX_DISABLE_CACHE = False

"""
sendfile
"""
SENDFILE_BACKEND = "sendfile.backends.simple"


ACTSTREAM_SETTINGS = {
    "MODELS": (
        # 'account.user',
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


#######################################################################
# search
#######################################################################


#######################################################################
# search v2
#######################################################################
ELASTICSEARCH_DSL = {"default": {"hosts": "localhost:9200"}}


"""
streaming server
"""


RTMP_HOST = "127.0.0.2"
RTMP_APP = "alibrary"
RTMP_PORT = "1935"

ICECAST_HOST = "127.0.0.2"
ICECAST_PORT = "8000"

"""
api server
"""
DISCOGS_HOST = "172.20.10.207:8099"
DISCOGS_RATE_LIMIT = False


#######################################################################
# captcha
# https://github.com/mbi/django-simple-captcha/blob/master/captcha/conf/settings.py
#######################################################################
CAPTCHA_LETTER_ROTATION = (-12, 12)
# CAPTCHA_BACKGROUND_COLOR = '#fafafa'
# CAPTCHA_FOREGROUND_COLOR = '#6633CC'
CAPTCHA_BACKGROUND_COLOR = "#ffffff"
CAPTCHA_FOREGROUND_COLOR = "#333333"
CAPTCHA_CHALLENGE_FUNCT = "captcha.helpers.random_char_challenge"
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_NOISE_FUNCTIONS = ("captcha.helpers.noise_dots",)
CAPTCHA_FILTER_FUNCTIONS = ()
CAPTCHA_PUNCTUATION = """_"',.;:-"""
CAPTCHA_LENGTH = 8
CAPTCHA_IMAGE_SIZE = (160, 28)
CAPTCHA_FIELD_TEMPLATE = "captcha/field.html"


MEDIA_ASSET_KEEP_DAYS = 60

GRAVATAR_DEFAULT_IMAGE = "blank"

EL_PAGINATION_PER_PAGE = 12

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
