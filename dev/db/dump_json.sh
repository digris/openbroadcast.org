#!/bin/sh


# run from 'website' directory:
# ../util/db/dump_json.sh


#######################################################################
# dump core apps
#######################################################################

./manage.py dumpdata \
    contenttypes \
    --database default \
    --indent 4 \
    -o ../util/db/dump_json/01-core.json

./manage.py dumpdata \
    auth \
    sites \
    --database default \
    --indent 4 \
    -o ../util/db/dump_json/02-auth.json


#######################################################################
# dump cms data
#######################################################################

./manage.py dumpdata \
    cms \
    menus \
    -e cms.usersettings -e menus.cachekey \
    --database default \
    --indent 4 \
    -o ../util/db/dump_json/03-cms.json

./manage.py dumpdata \
    l10n \
    --database default \
    --indent 4 \
    -o ../util/db/dump_json/04-l10n.json


#######################################################################
# dump library data
#######################################################################

./manage.py dumpdata \
    alibrary \
    --database default \
    --indent 4 \
    -o ../util/db/dump_json/10-library.json
