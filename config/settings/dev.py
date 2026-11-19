from .base import *  # noqa


# NOTE: defaults target the published ports of devsupport/compose.yml, the
#       containers get their in-network urls from the compose environment.
DATABASES = {
    "default": {
        **env.db("DATABASE_URL", default="mysql://obp:obp@127.0.0.1:3307/obp"),
        # NOTE: no persistent connections. runserver handles every request in a new
        #       thread, kept connections are dropped (not closed) when it ends:
        #       mariadb logs "Aborted connection ..." for each of them.
        "CONN_MAX_AGE": 0,
    },
}

import pymysql

pymysql.version_info = (1, 2, 5)
pymysql.install_as_MySQLdb()


NGINX_X_ACCEL_REDIRECT = False