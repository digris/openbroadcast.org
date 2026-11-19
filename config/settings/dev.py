from .base import *  # noqa


# NOTE: defaults target the published ports of devsupport/compose.yml, the
#       containers get their in-network urls from the compose environment.
DATABASES = {
    "default": {
        **env.db("DATABASE_URL", default="mysql://obp:obp@127.0.0.1:3307/obp"),
        "CONN_MAX_AGE": 600,
    },
}

import pymysql

pymysql.version_info = (1, 2, 5)
pymysql.install_as_MySQLdb()


NGINX_X_ACCEL_REDIRECT = False