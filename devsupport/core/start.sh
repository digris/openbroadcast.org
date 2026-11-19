#!/bin/sh

# NOTE: no automatic `migrate` - the dev database is loaded from a dump (see README)

./manage.py runserver "0.0.0.0:${PORT:-5000}" &

celery -A config.celery_app worker \
    -n default@%h \
    -B -s /tmp/celerybeat-schedule \
    -l info &

wait
