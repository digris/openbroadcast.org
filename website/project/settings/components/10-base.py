# -*- coding: utf-8 -*-
import os
import sys
from django.core.urlresolvers import reverse_lazy

gettext = _ = lambda s: s
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# subdirectory for apps
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tools'))
sys.path.insert(0, os.path.join(BASE_DIR, 'cmsplugins'))
sys.path.insert(0, os.path.join(BASE_DIR, 'legacy'))

DEBUG = False
SERVE_MEDIA = False
COMPRESS_OFFLINE = False
COMPRESS_ENABLED = True


################################################################################
# language settings
################################################################################


DEFAULT_LANGUAGE = 0
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _(u'Englisch')),
    # ('de', _(u'Deutsch')),
]

CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': _(u'Englisch'),
            'public': True,
        },
        # {
        #     'code': 'de',
        #     'name': _(u'Deutsch'),
        #     'public': True,
        # }
    ],
    'default': {
        'fallbacks': ['en',],
        'redirect_on_fallback': False,
        'public': True,
        'hide_untranslated': True,
    }
}




TIME_ZONE = 'Europe/Zurich'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
ROOT_URLCONF = 'project.urls'
SECRET_KEY = 'test_key'

SITE_URL = 'http://127.0.0.1:8080'





################################################################################
# database (defaults only, used for tests)
################################################################################

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'org_openbroadcast_local',
    },
}


################################################################################
# middleware
################################################################################

MIDDLEWARE_CLASSES = [

    'corsheaders.middleware.CorsMiddleware',
    'webpack.middleware.WebpackDevserverMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    # cms
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',

    'base.middleware.xs_sharing.XsSharingMiddleware',
    'arating.middleware.AratingIpMiddleware',
]



SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# profiles & co
ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/network/users/%s/" % o.username,
}



##################################################################
# API v2
##################################################################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}

##################################################################
# notebook / shell plus
##################################################################
NOTEBOOK_ARGUMENTS = [
    '--allow-root',
    '--ip', '0.0.0.0',
    '--port', '7777',
]


MIGRATION_MODULES = {
    # cms base plugins
    # 'djangocms_snippet': 'djangocms_snippet.migrations_django',
    # 'djangocms_link': 'djangocms_link.migrations_django',

    # self maintained modules
    'cms_redirects': 'cms_redirects.migrations_django',

}


##################################################################
# exported settings
##################################################################
SETTINGS_EXPORT = [
    'FACEBOOK_APP_ID',
]



IMORTER_USE_CELERYD = True
EXPORTER_USE_CELERYD = True
ALIBRARY_USE_CELERYD = True
ABCAST_USE_CELERYD = True
MEDIA_ASSET_USE_CELERYD = True
PYPO_USE_CELERYD = True
