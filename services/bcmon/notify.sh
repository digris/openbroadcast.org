#!/bin/sh
############################################
# just a wrapper to call the notifyer      #
# needed here to keep dirs/configs clean   #
# and maybe to set user-rights             #
############################################
#cd ../
/srv/bcmon/bin/python bcmon_notify.py "$1" "$2" "$3" &
