from .base import *

DEBUG = True

TEST_MODE = True

LOGGING = {}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
STATIC_ROOT = PROJECT_ROOT / "build"

MEDIA_ROOT = PROJECT_ROOT / "data" / "test" / "media"

DATABASES = {
    "null": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/dev/null",
    },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db-test.sqlite3",
    },
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
