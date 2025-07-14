import os
from django.conf import settings

BASE_DIR = getattr(settings, "BASE_DIR")


NAVUTILS_MENU_CONFIG = {
    'CURRENT_MENU_ITEM_CLASS': 'active selected',
    'CURRENT_MENU_ITEM_PARENT_CLASS': 'active selected has-current',
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "base", "templates"),
        ),
        "APP_DIRS": False,
        "OPTIONS": {
            "string_if_invalid": "INVALID: %s",
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                # social auth
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                #
                "webpack.context_processors.webpack_devserver",
                #
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                #
                "sekizai.context_processors.sekizai",
                "navutils.context_processors.menus",
                # messaging
                "postman.context_processors.inbox",
                # settings
                "django_settings_export.settings_export",
                # authentication
            ),
            "loaders": [
                # ('django.template.loaders.cached.Loader', [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "django.template.loaders.eggs.Loader",
                # ]),
            ],
        },
    }
]