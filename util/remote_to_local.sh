#!/bin/bash

CONF_FILE="util/remote_to_local.conf"

# remote
APP_SERVER="<set in remote_to_local.conf>"
MEDIA_ROOT="<set in remote_to_local.conf>"
DB_HOST="<set in remote_to_local.conf>"
DB_NAME="<set in remote_to_local.conf>"
DB_USER="<set in remote_to_local.conf>"
DB_PASS="<set in remote_to_local.conf>"

# local
DB_LOCAL_NAME="com_example_local"
DB_LOCAL_USER="root"
DB_LOCAL_PASS="root"



if [ -r $CONF_FILE ]; then
  echo
  echo '*************************************************************'
  echo "* READING CONFIG FILE: $CONF_FILE"
  echo '*************************************************************'
  echo
  source $CONF_FILE
else
  echo
  echo '*************************************************************'
  echo "* UNABLE TO READ: $CONF_FILE"
  echo '*************************************************************'
  echo
  echo 'copy and adjust "sample_remote_to_local.conf"'
  echo
  exit
fi



echo
echo '*************************************************************'
echo "* REMOTE2LOCAL"
echo '*************************************************************'
echo "APP_SERVER:    $APP_SERVER"
echo "MEDIA_ROOT:    $MEDIA_ROOT"
echo "DB_HOST:       $DB_HOST"
echo "DB_NAME:       $DB_NAME"
echo "DB_USER:       $DB_USER"
echo "DB_PASS:       ************"
echo "DB_LOCAL_NAME: $DB_LOCAL_NAME"
echo "DB_LOCAL_USER: $DB_LOCAL_USER"
echo "DB_LOCAL_PASS: $DB_LOCAL_PASS"
echo '*************************************************************'
echo

echo
echo "# fetching remote database"

read -r -p "Are you sure? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then

    echo "ssh -C root@$APP_SERVER \\"
    echo "mysqldump -h $DB_HOST -u $DB_USER -p************** $DB_NAME"
    echo "mysql -h 127.0.0.1 -u $DB_LOCAL_USER -p$DB_LOCAL_PASS -D $DB_LOCAL_NAME"

    ssh -C root@$APP_SERVER \
    "mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME" \
    | mysql -h 127.0.0.1 -u $DB_LOCAL_USER -p$DB_LOCAL_PASS -D $DB_LOCAL_NAME
else
    echo "skipping database download"
fi




echo
echo "# fetching remote media"

read -r -p "Are you sure? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then

    echo "rsync -avz -e ssh root@$APP_SERVER:$MEDIA_ROOT \\"
    echo "website/media/"

    rsync -avz -e ssh root@$APP_SERVER:$MEDIA_ROOT \
    website/media/
else
    echo "skipping media download"
fi
