# -*- coding: utf-8 -*-
import os
from django.conf import settings
BASE_DIR = getattr(settings, 'BASE_DIR')
DEBUG = getattr(settings, 'DEBUG')

################################################################################
# django apps
################################################################################

INSTALLED_APPS = (

    'djangocms_admin_style',
    #'django_slick_admin',
    'admin_tools',
    'admin_shortcuts',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.syndication',
    'django.contrib.humanize',
    'django.contrib.webdesign',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'threadedcomments',
    'fluent_comments',
    'django_comments',

    # server
    'gunicorn',
    #'silk',
    'django_date_extensions',
    'haystack',
    'search',
    'djangocms_sphinxdoc',

    'addthis',

    # tools
    'django_extensions',
    'django_filters',
    'sendfile',
    'missing', # http://django-missing.readthedocs.org/
    'raven.contrib.django.raven_compat',
    'raven.contrib.django.celery',
    'djcelery_email',
    'el_pagination',


    'base',
    'platform_base',
    #
    'api_base',
    'notifications',
    'mailer',
    'djcelery',
    'django_countries',
    'l10n',
    'guardian',
    'filer',
    'adv_cache_tag',
    'cacheops',
    #'reversion',
    #'changetracker',
    #'auditlog',
    'django_badbrowser',
    'genericadmin',
    'hvad',
    'selectable',
    'genericrelations',
    'spurl',
    'lib',
    'pure_pagination',
    'crispy_forms',
    'floppyforms',
    'absolute',
    'announcements',
    'subscription',

    # asset and media handling
    'sekizai',
    'compressor',
    'easy_thumbnails',

    # cms
    'cms',
    'menus',
    'mptt',
    #'polymorphic',
    'treebeard',

    # cms plugins
    'djangocms_link',
    'djangocms_snippet',
    'djangocms_text_ckeditor',
    'djangocms_panel',
    'djangocms_column',

    'dajaxice',
    'dajax',
    'email_obfuscator',

    #'stepguide',

    # users / auth
    'avatar',
    'registration',
    'social_auth',
    'captcha',
    'django_gravatar',
    'loginas',
    'dropbox',
    'provider',
    'provider.oauth2',

    # api
    'tastypie',

    # platform apps
    'profiles',
    'postman',
    'atracker',
    'invitation',
    'alibrary',
    'collection',
    'media_asset',
    'aplayer',
    'importer',
    'massimporter',
    'exporter',
    'abcast',
    'autopilot',
    'arating',
    'backfeed',
    'statistics',
    'wikisyntax',
    'tagging',
    'tagging_extra',
    'ac_tagging',
    'actstream',
    'pageguide',
    'iptracker',
    'metadata_generator',

    # legacy & migration
    'obp_legacy',
    #'apiv1cache',

    # platform tools
    'pushy',
    'nunjucks',

    # monitoring / ops / tracking
    #'opbeat.contrib.django',

)



################################################################################
# app specific settings
################################################################################

COMMENTS_APP = 'fluent_comments'
COMMENT_MAX_LENGTH = 800
FLUENT_COMMENTS_EXCLUDE_FIELDS = ['title', 'email', 'name', 'url', ]


PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 6,
    'MARGIN_PAGES_DISPLAYED': 3,
}

FORMATS_MEDIA = {
    #'mp3': ['base', 'low'],
    'mp3': ['base', ],
}

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# filer
FILER_IS_PUBLIC_DEFAULT = True
FILER_ENABLE_PERMISSIONS = True
FILER_STATICMEDIA_PREFIX = '/static/filer/'
FILE_PROTECTION_METHOD = 'basic'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_QUALITY = 80
THUMBNAIL_BASEDIR = 'thumbnails'
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)
#THUMBNAIL_NAMER = 'easy_thumbnails.namers.hashed'

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']
BLEACH_STRIP_TAGS = True

CMS_GIT_FILE = os.path.join(BASE_DIR, 'changelog.txt')


################################################################################
# accounts / user handling
################################################################################

AUTH_PROFILE_MODULE = "profiles.Profile"
ANONYMOUS_USER_ID = -1
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/signout/'
LOGIN_REDIRECT_URL = "/"

USERENA_ACTIVATION_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True
EMAIL_CONFIRMATION_DAYS = 5

"""
socialauth
"""
ACCOUNT_ACTIVATION_DAYS = 7
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.dropbox.DropboxBackend',
    'social_auth.backends.contrib.soundcloud.SoundcloudBackend',
    #'social_auth.backends.contrib.stackoverflow.StackoverflowBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.browserid.BrowserIDBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.disqus.DisqusBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    #'social_auth.backends.contrib.vk.VKOAuth2Backend',
    #'social_auth.backends.contrib.live.LiveBackend',
    #'social_auth.backends.contrib.skyrock.SkyrockBackend',
    #'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    #'social_auth.backends.contrib.readability.ReadabilityBackend',
    #'social_auth.backends.contrib.fedora.FedoraBackend',
    #'social_auth.backends.OpenIDBackend',

    'obp_legacy.auth.backends.LegacyBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]
LINKEDIN_CONSUMER_KEY = ''
LINKEDIN_CONSUMER_SECRET = ''
GOOGLE_OAUTH2_CLIENT_ID = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''
FOURSQUARE_CONSUMER_KEY = ''
FOURSQUARE_CONSUMER_SECRET = ''
YAHOO_CONSUMER_KEY = ''
YAHOO_CONSUMER_SECRET = ''
GITHUB_APP_ID = ''
GITHUB_API_SECRET = ''
DROPBOX_APP_ID = ''
DROPBOX_API_SECRET = ''
SOUNDCLOUD_CLIENT_ID = ''
SOUNDCLOUD_CLIENT_SECRET = ''

# invitation
INVITATION_INVITE_ONLY = False
INVITATION_EXPIRE_DAYS = 10
INVITATION_INITIAL_INVITATIONS = 5

SOCIAL_AUTH_SLUGIFY_USERNAMES = True
# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/signout/'
LOGIN_REDIRECT_URL = "/"

LOGIN_ERROR_URL = LOGIN_URL

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'base.social_auth_extra.pipeline.post_connect_tasks',
)

################################################################################
# Messaging
# https://bitbucket.org/psam/django-postman/wiki/Quick_Start_Guide
################################################################################

POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
# POSTMAN_DISALLOW_COPIES_ON_REPLY = True  # default is False
# POSTMAN_DISABLE_USER_EMAILING = True  # default is False
POSTMAN_AUTO_MODERATE_AS = True  # default is None
POSTMAN_SHOW_USER_AS = 'get_full_name'
# POSTMAN_NOTIFIER_APP = None  # default is 'notification'
# POSTMAN_MAILER_APP = 'mailer'



# other...
PRETTIFY = True


SELECTABLE_MAX_LIMIT = 10

"""
wikisyntax, eg allows tor resolve [a:Artists Name] to object
"""
WIKISYNTAX = (
    ('r', 'alibrary.util.object_linker.WikiRelease'),
    ('a', 'alibrary.util.object_linker.WikiArtist'),
    ('l', 'alibrary.util.object_linker.WikiLabel'),
)
WIKISYNTAX_DISABLE_CACHE = False

"""
sendfile, delivers bought relases/tracks
"""
SENDFILE_BACKEND = 'sendfile.backends.simple'

BADBROWSER_REQUIREMENTS = (
    ("firefox", "3.0"),
    ("chrome", "10.0"),
    ("microsoft internet explorer", "8"),
    ("opera", None), # None indicates no support for the given browser, whatever the version
)
BADBROWSER_SUGGEST = ("firefox", "chrome", "safari", "opera", "microsoft internet explorer")
#BADBROWSER_BASE_TEMPLATE = "base.html"




ACTSTREAM_SETTINGS = {
    'MODELS': (
        'auth.user',
        'auth.group',
        'alibrary.release',
        'alibrary.playlist',
        'alibrary.artist',
        'alibrary.media',
        'alibrary.label',
        'abcast.emission',
        'abcast.station'
    ),
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

"""
stream - defaults to: mp3, highest available bitrate.
would theoretically be possible to implement bitrate-switching
depending on users connection.
"""
FORMATS_STREAM = {
    'mp3': [128],
}
FORMATS_DOWNLOAD = {
    'mp3': [192],
    'flac': ['base'],
    'wav': ['base'],
}

WAVEFORM_SIZES = {
    's': [100, 20],
    'm': [300, 30],
    'l': [600, 100],
}


"""
Search
"""
HAYSTACK_CONNECTIONS = {
    'default': {
        #'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr',
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'search.signals.SearchIndexProcessor'






"""
streaming server
"""

APLAYER_STREAM_MODE = 'html5'

RTMP_HOST = '127.0.0.2'
RTMP_APP = 'alibrary'
RTMP_PORT = '1935'

ICECAST_HOST = '127.0.0.2'
ICECAST_PORT = '8000'

"""
api server
"""
MUSICBRAINZ_HOST = 'mb.anorg.net'
MUSICBRAINZ_RATE_LIMIT = False

DISCOGS_HOST = '172.20.10.207:8099'
DISCOGS_RATE_LIMIT = False



"""
captcha
https://github.com/mbi/django-simple-captcha/blob/master/captcha/conf/settings.py
"""



CAPTCHA_LETTER_ROTATION = (-10, 10)
CAPTCHA_BACKGROUND_COLOR = '#fafafa'
CAPTCHA_FOREGROUND_COLOR = '#6633CC'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_FILTER_FUNCTIONS = ()
CAPTCHA_PUNCTUATION = '''_"',.;:-'''
CAPTCHA_LENGTH = 6
CAPTCHA_IMAGE_SIZE = (120, 30)
CAPTCHA_FIELD_TEMPLATE = 'captcha/field.html'


MEDIA_ASSET_KEEP_DAYS = 60



"""
ajax lookups
"""
AJAX_LOOKUP_CHANNELS = {
    'aliases': {'model': 'alibrary.artist', 'search_field': 'name'}
}
# AJAX_SELECT_BOOTSTRAP = True
# AJAX_SELECT_INLINES = 'inline'


CHANGETRACKER_TRACKED_MODELS = (
    # {
    #     'model': 'alibrary.label',
    #     'diff_function': 'bla',
    # },
)

#GRAVATAR_DEFAULT_IMAGE = '/static/img/base/defaults/listview.artist.xl.png'
GRAVATAR_DEFAULT_IMAGE = 'identicon'


EL_PAGINATION_PER_PAGE = 12