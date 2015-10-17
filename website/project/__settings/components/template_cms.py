# -*- coding: utf-8 -*-
import os

gettext = lambda s: s
_ = gettext

CRISPY_TEMPLATE_PACK = 'foundation-5'

FLAVOURS = ('full', 'mobile', 'tablet', 'experiment')

CMS_REDIRECTS = True
CMS_SEO_FIELDS = True
CMS_SHOW_START_DATE = True
CMS_SHOW_END_DATE = True

CMS_TEMPLATES = (
    ('_cms/single-column.html', 'Single Column - Standard Template'),
    ('_cms/two-columns.html', 'Two Columns'),
    ('_cms/home.html', 'Home Template'),
)

CONTENT_PLUGINS = [
    'TextPlugin',
    'LinkPlugin'
]
CONTENT_PLUGINS.extend([
    'AppshotPlugin',
    'BoxedPlugin',
    'FAQMultiListPlugin',
    'FilerFilePlugin',
    'FilerImagePlugin',
    'FilerSVGPlugin',
    'MapPlugin',
    'SingleProductPlugin',
    'SnippetPlugin',
    'TextPlugin',
    'YouTubePlugin',
])

CMS_PLACEHOLDER_CONF = {
    'content': {
        #'plugins': ['TextPlugin', 'PicturePlugin'],
        #'text_only_plugins': ['LinkPlugin'],
        'extra_context': {"width": 1280},
        'name': _("Content"),
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body':'<p>Lorem ipsum dolor sit amet... <br><em>(Double-click me to edit!)</em></p>',
                },
            },
        ],
    },
    'sidebar': {
        #"plugins": ['TextPlugin', 'LinkPlugin'],
        "extra_context": {"width": 540},
        'name': _("Right Column"),
        'limits': {
            'global': 4,
            'TeaserPlugin': 1,
            'LinkPlugin': 1,
        },
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body':'<p>Lorem ipsum dolor sit amet... <br><em>(Double-click me to edit!)</em></p>',
                },
            },
        ],
    },


    # app based placeholders
    'chapter_content': {
        'name': "Article Content",
        'plugins': [
            'TextPlugin',
            'YouTubePlugin',
        ],
        'text_only_plugins': [
            'LinkPlugin',
            'PicturePlugin',
            'FilerFilePlugin',
            'FilerImagePlugin',
            'FilerSVGPlugin',
            'YouTubePlugin',
        ],
        #'child_classes': {
        #    'TextPlugin': ['PicturePlugin', 'LinkPlugin'],
        #},
        'language_fallback': True,
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body':'<p>(( Edit me! ))</p>',
                },
            },
        ],

    },




}

COLUMN_WIDTH_CHOICES = (
    ('3', "1/4"),
    ('4', "1/3"),
    ('6', "1/2"),
    ('8', "2/3"),
    ('9', "3/4"),
    ('12', "1/1")
)


CMS_PLUGIN_PROCESSORS = (
    'base.cms_plugin_processors.wrap_text',
)

########## TEXT EDITOR CONFIGURATION
CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'uiColor': '#ffffff',
    'toolbar_CMS': [
        ['Undo', 'Redo'],
        ['cmsplugins', 'ShowBlocks'],
        #['Format', 'Styles'],
        ['Styles',],
        ['Cut','Copy','Paste','PasteText', '-', 'Find','Replace'],
        ['NumberedList', 'BulletedList',],
        ['Source',],
        ['Bold',]
        #['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
    ],
    'startupOutlineBlocks': True,
    'skin': 'moono',

    'stylesSet': [

        # alternative to 'format' selector
        {'name': 'Paragraph', 'element': 'p',},
        {'name': 'Heading 1 (only _one_ per page!)', 'element': 'h1',},
        {'name': 'Heading 2', 'element': 'h2',},
        {'name': 'Heading 3', 'element': 'h3',},
        #{'name': 'Heading 4', 'element': 'h4',},
        {'name': 'Highlight', 'element': 'p', 'attributes': { 'class': 'marker highlight' }},
        #{'name': 'Dimmed', 'element': 'p', 'attributes': { 'class': 'dimmed' }},
        #{'name': 'Address', 'element': 'address',},

        #{'name': 'Cited Work', 'element': 'cite',},
        #{'name': 'Inline Quotation', 'element': 'q',},



        # custom elements
        #{'name': 'Italic Title',
        #'element': 'h2',
        #'styles': {
        #    'font-style': 'italic'
        #}},

    ]

}




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
                'django.core.context_processors.i18n',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'absolute.context_processors.absolute',
                'cms.context_processors.cms_settings',
                'django_mobile.context_processors.flavour',
                'sekizai.context_processors.sekizai',
            ),
            'loaders': [
                'django_mobile.loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ],
        },
    },
]


"""
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)
"""
