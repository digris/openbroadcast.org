import os
import sys
from django.core.urlresolvers import reverse_lazy

gettext = _ = lambda s: s
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# subdirectory for apps
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0, os.path.join(BASE_DIR, "tools"))

DEBUG = False
SERVE_MEDIA = False
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = True

################################################################################
# hacks
################################################################################
# os is outdated, manual download of cacert.pem is required
# wget https://curl.se/ca/cacert.pem -O /etc/ca-manually/cacert.pem
CA_CERT_PATH = "/etc/ca-manually/cacert.pem"
if os.path.exists(CA_CERT_PATH):
    os.environ["REQUESTS_CA_BUNDLE"] = CA_CERT_PATH


################################################################################
# language settings
################################################################################
DEFAULT_LANGUAGE = 0
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("Englisch")),
    # ('de', _(u'Deutsch')),
]

TIME_ZONE = "Europe/Zurich"
SITE_ID = 1
USE_I18N = False
USE_L10N = True
ROOT_URLCONF = "project.urls"
SECRET_KEY = "test_key"

SITE_URL = "http://127.0.0.1:5000"

USE_L10N = False
DATETIME_FORMAT = "Y-m-d H:i"
DATE_FORMAT = "Y-m-d"
SHORT_DATE_FORMAT = "Y-m-d"

################################################################################
# database (defaults only, used for tests)
################################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "org_openbroadcast_local",
    }
}


################################################################################
# middleware
################################################################################

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

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"


# profiles & co
# ABSOLUTE_URL_OVERRIDES = {"auth.user": lambda o: "/network/users/%s/" % o.username}
ABSOLUTE_URL_OVERRIDES = {"auth.user": lambda u: "/network/users/%s/" % u.profile.uuid}

##################################################################
# API v1
##################################################################
TASTYPIE_DEFAULT_FORMATS = ["json"]

##################################################################
# API v2
##################################################################
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

##################################################################
# notebook / shell plus
##################################################################
NOTEBOOK_ARGUMENTS = ["--allow-root", "--ip", "0.0.0.0", "--port", "7777"]


##################################################################
# exported settings
##################################################################
SETTINGS_EXPORT = ["FACEBOOK_APP_ID", "SITE_URL"]


IMORTER_USE_CELERYD = True
EXPORTER_USE_CELERYD = True
ALIBRARY_USE_CELERYD = True
ABCAST_USE_CELERYD = True
MEDIA_ASSET_USE_CELERYD = True
PYPO_USE_CELERYD = True


##################################################################
# system checks
##################################################################
SILENCED_SYSTEM_CHECKS = ["fields.W342"]
