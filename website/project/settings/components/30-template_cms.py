# -*- coding: utf-8 -*-
import os
from django.conf import settings
BASE_DIR = getattr(settings, 'BASE_DIR')


################################################################################
# templates
################################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'base', 'templates'),
        ),
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'webpack.context_processors.webpack_devserver',
                'django.core.context_processors.i18n',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'absolute.context_processors.absolute',
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',
                # messaging
                'postman.context_processors.inbox',
                # settings
                'django_settings_export.settings_export',
                # authentication
                'social_auth.context_processors.social_auth_backends',
                'social_auth.context_processors.backends_data',
                'social_auth.context_processors.social_auth_login_redirect',
            ),
            'loaders': [
                #('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
                #]),
            ],
        },
    },
]

################################################################################
# django-cms
################################################################################

CMS_TEMPLATES = (
    ('_templates/layout_a.html', 'Base Template'),
    ('_templates/layout_b.html', 'Alternative Title'),
    ('_templates/home.html', 'Home Template'),
)

WIDTH_INNER = 960
CMS_PLACEHOLDER_CONF = {
    'main': {
        "extra_context": {"width": WIDTH_INNER},
        'name': "Main Content",
    },
    'sidebar': {
        "extra_context": {"width": 300},
        'name': "Sidebar",
    },
    'footer': {
        'name': "Footer",
    },
}

CMS_PLUGIN_PROCESSORS = ()

CMS_SEO_FIELDS = True

CMS_CACHE_DURATIONS = {
    'menus': 3600,
    'content': 600,
    'permissions': 300,
}

COLUMN_WIDTH_CHOICES = (
    ('33.33%', '33%'),
    ('50%', '50%'),
)

CMS_TOOLBAR_ANONYMOUS_ON = False


CKEDITOR_SETTINGS = {
    'startupOutlineBlocks': True,
    'uiColor': '#ffffff',
    'skin': 'moono',
}


