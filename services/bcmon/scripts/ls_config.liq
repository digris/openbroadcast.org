###########################################
# liquidsoap config file                  #
###########################################

# author Jonas Ohrstrom <jonas@digris.ch>


# this file is specific to the obp 
# installation. eg it assumes that there are 
# two instances of LS running
# the "scheduler" & the "fallback" instance


###########################################
# general settings                        #
###########################################

log_file = "/var/log/obp/ls/<script>.log"
log_level = 2

# archive directory
archive_dir = "/storage/pypo/archive/"


# list pointing to the current couchcaster mountpoint 
couchcaster_list = "http://vdeb.openbroadcast.org/mod/ml/api/pypo/current_couchcaster"



###########################################
# stream settings                         #
###########################################
icecast_host = "172.16.16.128"
icecast_port = 8000
icecast_pass = "hackme"

# mountpoints
mount_scheduler = "pypo_scheduler"
mount_daypart = "pypo_daypart"
mount_live_in = "pypo_live_in"
mount_final = "pypo_final"

