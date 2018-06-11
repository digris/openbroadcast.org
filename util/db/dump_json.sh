#!/bin/sh


# run from 'website' directory:
# ../util/db/dump_json.sh


# dump core apps

./manage.py dumpdata \
    auth \
    sites \
    contenttypes \
    --database default \
    --indent 4 --natural-foreign --natural-primary \
    -o ../util/db/dump/01-core.json
