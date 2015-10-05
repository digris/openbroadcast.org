# start local development servers


# django
source ~/srv/openbroadcast.org-upgrade/bin/activate
cd ~/code/openbroadcast.org/website/
./manage.py runserver_plus 0.0.0.0:8080

# rabbitmq
sudo rabbitmq-server -detached

# celeryd
source ~/srv/openbroadcast.org-upgrade/bin/activate
cd ~/code/openbroadcast.org/website/
./manage.py celeryd -c 1 --purge -Q celery,import


# tokyo-tyrant
sudo rm /var/ttserver/pid # in case not cleaned
sudo ttservctl start

# solr
cd ~/srv/echoprint-server/solr
./run.sh

# musicbrainz (local instance, vmware)
ssh 172.16.82.130 -l musicbrainz
cd
screen
./run_server.sh --listen 0.0.0.0:5000



# haystack backend (solr)
cd ~/srv/openbroadcast.org-upgrade/services/apache-solr-3.6.2/example
java -jar start.jar



# dumping and restore/fixtures
./manage.py dumpdata cms text link menus sites > fixtures/initial.json

# snapshot (dev, osx)
mysqldump5 -h 127.0.0.1 -u root -proot org_openbroadcast_local > ~/tmp/org_openbroadcast_local.sql
mysql5 -h 127.0.0.1 -u root -proot org_openbroadcast_local < ~/tmp/org_openbroadcast_local.sql

# pushy
cd ~/code/openbroadcast/pushy/server/
node pushy.js






# playout startup
parts running on playout server:
 - pypo (python scripts)
 - liqudsoap (sound server)
 
ssh 172.16.82.134 -l root
cd /home/pypo/pypo/liquidsoap_scripts
sudo -u pypo /usr/bin/airtime-liquidsoap --verbose -f ls_script.liq

cd /home/pypo/pypo
sudo -u pypo env/bin/python pypo.py
 
  

# varnish
sudo /usr/local/Cellar/varnish/3.0.3/sbin/varnishd -F -a 0.0.0.0:88 -f ~/code/openbroadcast.org/conf/openbroadcast.org.vcl




# sass/compass setup
sudo gem install sass --pre
sudo gem install compass --pre

"""
Go to chrome://flags/ and Enable Developer Tools experiments, then restart Chrome.
Open Devtools and check Enable source maps in General tab and Support for Sass in Experimental tab.
Download latest Sass from the console: gem install sass --pre (you might need sudo)
Just adding sass_options = {:sourcemap => true} to config.rb in Compass won’t work (just yet) and you can even get Compass conflicts with the aforementioned Sass alpha version. In my case, Compass 0.12.2 (Alnilam) does not get on very well with Sass 3.3.0.alpha.103 (Bleeding Edge), though it might be some other gem conflict.
For that reason, we will have to watch changes using Sass directly, using sourcemap option: sass --watch --sourcemap sources/compass:public/css which generates a .map file for each source. This is the information Devtools will use to let you trace/edit original Sass files directly in the browser.
"""

# run sass compiler with sourcemap
cd /website/site-static/sass/
sass --watch --sourcemap _wip.sass:../css/wip.css
