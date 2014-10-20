#!/bin/sh

# export home dir
export HOME=/home/liquidsoap/

# update stations file
#rm include_stations.liq*
#wget web.devel.obp.ch/api/bcmon/include_stations.liq

# start liquidsoap with corresponding user & scrupt
sudo -u service /usr/bin/liquidsoap ls_script.liq
