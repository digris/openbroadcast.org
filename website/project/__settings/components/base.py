# -*- coding: utf-8 -*-
import os
import sys
import posixpath

gettext = lambda s: s
_ = gettext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# add to python-path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'tools'))
sys.path.insert(0, os.path.join(BASE_DIR, 'cmsplugins'))

SECRET_KEY = 'j1odx#ji=z%r@in1k3pj4=&kwgv&4dv78^9!nymh+vhy9m4&e*'
DEBUG = True
FILER_DEBUG = DEBUG
ALLOWED_HOSTS = ['*',]

# this fixes strange behaviour when running app through gunicorn
DEBUG_TOOLBAR_PATCH_SETTINGS = False

CMS_CACHE_PREFIX = 'com_reasonifly_cms'

SITE_ID = 1

LOCALE_PATHS = ('%s/locale/' % BASE_DIR,)

# Internationalization
LANGUAGE_CODE = 'de'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


LANGUAGES = [
    ('de', _(u'Deutsch')),
    ('en', _(u'Englisch')),
    ('fr', _(u'Französisch')),
    ('it', _(u'Italienisch')),
]

CMS_LANGUAGES = {
    1: [
        {
            'code': 'de',
            'name': _(u'Deutsch'),
            'public': True,
        },
        {
            'code': 'en',
            'name': _(u'Englisch'),
            'public': True,
        },
        {
            'code': 'fr',
            'name': _(u'Französisch'),
            'public': False,
        },
        {
            'code': 'it',
            'name': _(u'Italienisch'),
            'public': False,
        },
    ],
    'default': {
        'fallbacks': ['en',],
        'redirect_on_fallback': False,
        'public': True,
        'hide_untranslated': True,
    }
}

SOLID_I18N_USE_REDIRECTS = False

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

INSTALLED_APPS = (

    # admin apps
    #'relatedadminlink',
    'djangocms_admin_style',
    'admin_shortcuts',
    'polymorphic',

    # django base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.webdesign',

    # accounts
    'cas_profile',

    # auth
    #'emailusernames',
    #'registration',

    # api
    'tastypie',

    # life-savers
    'raven.contrib.django.raven_compat',
    #'south',
    #'reversion',
    'django_mobile',


    #'badbrowser',

    # cms
    'cms',
    #'mptt',
    'treebeard',
    'menus',
    'sekizai',

    # cms extension
    'djangocms_link',
    'djangocms_snippet',
    'djangocms_column',
    'djangocms_panel',
    'djangocms_text_ckeditor',

    'cms_redirects',
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',

    #'ajax_upload',
    'django_extensions',
    'debug_toolbar',
    'compressor',
    'easy_thumbnails',
    'pagedown',
    'analytics',
    'crispy_forms',
    'absolute',
    'emailit',
    'hvad',

    'taggit',
    'base',
    'ambassador',
    'story',
    'socialfeed',
    #'userstory',
    #'geoposition',


    # migration tools
    #'modx_legacy',
    # end migration tools
)


MIDDLEWARE_CLASSES = (

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    #'badbrowser.middleware.BrowserSupportDetection',
    #'django.middleware.locale.LocaleMiddleware',
    'solid_i18n.middleware.SolidLocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms_redirects.middleware.RedirectMiddleware',
)


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data.sqlite3'),
    }
}

BROKER_URL = 'django://'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'


# auth
AUTHENTICATION_BACKENDS = (
    'django_cas_ng.backends.CASBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'cas_profile.User'

LOGIN_REDIRECT_URL = '/'

CAS_SERVER_URL = 'https://service.hazelfire.com/en/cas/'
#CAS_EXTRA_LOGIN_PARAMS = {'renew': True}
CAS_ADMIN_PREFIX = '/admin/'
CAS_LOGOUT_COMPLETELY = False
CAS_VERSION = '3'

CMS_GIT_FILE = os.path.join(BASE_DIR, 'changelog.txt')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    #'django_jenkins.tasks.django_tests',
    #'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = (
)



ADMIN_SHORTCUTS = [
    {
        'title': _('Quick Links'),
        'shortcuts': [
            {
                'url': '/',
                'title': _('Public Site'),
                'open_new_window': True,
            },
            {
                'url': 'https://lab.hazelfire.com/projects/reasonifly-com/issues/new',
                'title': _('Issue Tracker'),
                'open_new_window': True,
                'class': 'tool',
            },
            {
                'url': 'mailto:lab@hazelfire.com?body=%0D%0A%0D%0AProject: reasonifly-com',
                'title': _('New Issue by Email'),
                'open_new_window': False,
                'class': 'mail',
            },
        ]
    },
    {
        'title': _('Administration'),
        'shortcuts': [
            {
                'url_name': 'admin:cms_page_changelist',
                'title': _('CMS Pages'),
            },
        ]
    },
]

BADBROWSER_REQUIREMENTS = (
	("firefox", "22.0"),
	("chrome", "22.0"),
	("microsoft internet explorer", "11.0"),
	("opera", None),
)
BADBROWSER_SUGGEST = ('chrome', 'safari', 'ie', 'firefox', )

MIGRATION_MODULES = {
    # cms base plugins
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',

    # filer plugins
    'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
    'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
    'cmsplugin_filer_link': 'cmsplugin_filer_link.migrations_django',
    'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',

    # self maintained modules
    'cms_redirects': 'cms_redirects.migrations_django',
}
