# mount (needs vpn connection)

#sshfs root@172.20.10.84:/var/www/obp/data ~/sshfs/obp_legacy/

sshfs -o reconnect -o ro root@vz.obp:/nas/prod/ml ~/sshfs/obp_legacy/


# on server (vz host)
# DEPRECIATED: mounts are solved on os level (only needewd when running on a host outside obp network)
cd ~/vpn/
openvpn --config config.conf
sshfs root@172.20.10.84:/var/www/obp/data /media/obp_legacy/ -o IdentityFile=/home/ohrstrom/.ssh/id_rsa -o allow_other -o reconnect -o ro
# 
mount -n -t simfs /media/obp_legacy/ /vm/nodes/root/105/media/obp_legacy/ -o /media/obp_legacy/