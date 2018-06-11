#!/bin/sh


# create initial schema
# ./manage.py migrate sites --no-initial-data --database rebuild -v 3
# ./manage.py migrate auth --no-initial-data --database rebuild -v 3
# ./manage.py migrate --no-initial-data --database rebuild -v 3

# run from 'website' directory:
# ../util/db/load_json.sh


# dump core apps

./manage.py dumpdata \
    auth \
    sites \
    contenttypes \
    --database default \
    --indent 4 --natural-foreign --natural-primary \
    -o ../util/db/dump/01-core.json
