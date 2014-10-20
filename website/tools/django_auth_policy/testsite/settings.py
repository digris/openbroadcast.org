""" Settings to be used by tests
"""
import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_auth_policy',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_auth_policy.middleware.AuthenticationPolicyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'django_auth_policy.testsite.urls'

# Required for Django 1.4+
STATIC_URL = '/static/'

# Required for Django 1.5+
SECRET_KEY = 'abc123'

# Use test templates
TEMPLATE_DIRS = (
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
)

# Enabled Django Auth Policies
AUTHENTICATION_POLICIES = (
    ('django_auth_policy.authentication.AuthenticationBasicChecks', {}),
    ('django_auth_policy.authentication.AuthenticationDisableExpiredUsers', {}),
    ('django_auth_policy.authentication.AuthenticationLockedUsername', {}),
    ('django_auth_policy.authentication.AuthenticationLockedRemoteAddress', {}),
)
PASSWORD_STRENGTH_POLICIES = (
    ('django_auth_policy.password_strength.PasswordMinLength', {}),
    ('django_auth_policy.password_strength.PasswordContainsUpperCase', {}),
    ('django_auth_policy.password_strength.PasswordContainsLowerCase', {}),
    ('django_auth_policy.password_strength.PasswordContainsNumbers', {}),
    ('django_auth_policy.password_strength.PasswordContainsSymbols', {}),
    ('django_auth_policy.password_strength.PasswordUserAttrs', {}),
    ('django_auth_policy.password_strength.PasswordDisallowedTerms', {
        'terms': ['Testsite']
    }),
)
PASSWORD_CHANGE_POLICIES = (
    ('django_auth_policy.password_change.PasswordChangeExpired', {}),
    ('django_auth_policy.password_change.PasswordChangeTemporary', {}),
)

# Required for testing log output
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'testing': {
            'level': 'DEBUG',
            #'class': 'django_auth_policy.tests_logger.TestLoggingHandler',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'root': {
        'handlers': ['testing'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django_auth_policy': {
            'handlers': ['testing'],
            'propagate': False,
            'level': 'DEBUG',
        }
    }
}
