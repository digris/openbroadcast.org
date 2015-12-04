# -*- coding: utf-8 -*-
import os
import sys
import djcelery
from django.core.urlresolvers import reverse_lazy

djcelery.setup_loader()
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

LANGUAGES = [
    ('en', 'en'),
    ('de', 'de'),
]
DEFAULT_LANGUAGE = 0
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _(u'Englisch')),
    ('de', _(u'Deutsch')),
]

CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': _(u'Englisch'),
            'public': True,
        },
        {
            'code': 'de',
            'name': _(u'Deutsch'),
            'public': True,
        }
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
USE_I18N = True
USE_L10N = True
ROOT_URLCONF = 'project.urls'
SECRET_KEY = '0r6%7gip5tmez*vygfv+u14h@4lbt^8e2^26o#5_f_#b7%cm)u'

################################################################################
# middleware
################################################################################

MIDDLEWARE_CLASSES = (
    # sentry
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'reversion.middleware.RevisionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # cms
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'lib.middleware.xs_sharing.XsSharingMiddleware',
    'lib.middleware.profiler.ProfileMiddleware',

    #'auditlog.middleware.AuditlogMiddleware',
    'social_auth.middleware.SocialAuthExceptionMiddleware',
    'arating.middleware.AratingIpMiddleware',
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
                'url_name': 'admin:cms_page_changelist',
                'title': _('CMS Pages'),
            },
            {
                'url': 'https://lab.hazelfire.com/projects/openbroadcast-org/issues/new',
                'title': _('Issue Tracker'),
                'open_new_window': True,
                'class': 'tool',
            },
            {
                'url': 'mailto:lab@hazelfire.com?body=%0D%0A%0D%0AProject: openbroadcast-org',
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
                'url': reverse_lazy('admin:app_list', args=('alibrary',)),
                'title': _('Media Library'),
                'class': 'music',
            },
            {
                'url': reverse_lazy('admin:app_list', args=('abcast',)),
                'title': _('Broadcast App'),
                'class': 'sound',
            },
            {
                'url': reverse_lazy('admin:app_list', args=('profiles',)),
                'title': _('Profile App'),
                'class': 'user',
            },
            {
                'url': reverse_lazy('admin:app_list', args=('importer',)),
                'title': _('Import App'),
                'class': 'cloud2',
            },
            {
                'url': reverse_lazy('admin:app_list', args=('exporter',)),
                'title': _('Export App'),
                'class': 'cloud3',
            },
        ]
    },

]











SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


# profiles & co
ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/network/users/%s/" % o.username,
}




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

IMORTER_USE_CELERYD = True
EXPORTER_USE_CELERYD = True
ALIBRARY_USE_CELERYD = True
ABCAST_USE_CELERYD = True
MEDIA_ASSET_USE_CELERYD = True
PYPO_USE_CELERYD = True
