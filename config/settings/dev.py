from .base import *  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "obp",
        "HOST": "127.0.0.1",
        "PORT": 3307,
        "USER": "obp",
        "PASSWORD": "obp",
        "CONN_MAX_AGE": 600,
    },
}

import pymysql

pymysql.version_info = (1, 2, 5)
pymysql.install_as_MySQLdb()


NGINX_X_ACCEL_REDIRECT = False