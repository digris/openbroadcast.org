#!/bin/sh


# create initial schema
# ./manage.py migrate auth --no-initial-data --database rebuild -v 3
# ./manage.py migrate sites --no-initial-data --database rebuild -v 3
# ./manage.py migrate auth --no-initial-data --database rebuild -v 3
# ./manage.py migrate --no-initial-data --database rebuild -v 3

# run from 'website' directory:
# ../util/db/load_json.sh

CONNECTION='default'

#######################################################################
# load core apps
#######################################################################

./manage.py loaddata \
    --database $CONNECTION \
    ../util/db/dump_json/01-core.json

./manage.py loaddata \
    --database $CONNECTION \
    ../util/db/dump_json/02-auth.json


#######################################################################
# load cms data
#######################################################################

./manage.py loaddata \
    --database $CONNECTION \
    ../util/db/dump_json/03-cms.json




#######################################################################
# load library data
#######################################################################

./manage.py loaddata \
    --database $CONNECTION \
    ../util/db/dump_json/10-library.json

