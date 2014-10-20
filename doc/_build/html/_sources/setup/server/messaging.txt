Messaging Server(s)
###################


Main Messaging Server
*********************

 - node03

Software in use:

 - redis
 - rabbit-mq
 - EP database


cache
==========

aptitude install memcached

.. code-block:: bash

    nano /etc/memcached.conf # -l 172.20.10.203


redis
==========

.. code-block:: bash

    wget http://download.redis.io/releases/redis-2.8.5.tar.gz
    tar xzf redis-2.8.5.tar.gz
    cd redis-2.8.5
    make
    make install

    nano /etc/redis/redis.conf # see etc/
    nano /etc/supervisor/conf.d/redis.conf # see etc/

    supervisorctl reread
    supervisorctl update
    supervisorctl status

/etc/supervisor/conf.d/redis.conf
---------------------------------

.. code-block:: bash

    [program:redis]
    directory=/root/
    command=/usr/local/bin/redis-server /etc/redis/redis.conf
    user=root
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=HOME='/root/'
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=5
    stdout_logfile=/var/log/supervisor/redis.log


rabbit-mq
==========

see: https://www.rabbitmq.com/install-debian.html

.. code-block:: bash

    rabbitmq-plugins enable rabbitmq_management

    rabbitmqctl add_user root <password>
    rabbitmqctl set_user_tags root administrator


http://172.20.10.203:15672/ # needs vpn connection


askjdhkajsd ajshd kajhsdk ajs 
============================================

askjdha ksjhdha jshdl kajhsdl kads
asd ads lagskjdagkjsdhgkajsdg 
- skdjhajshd
- asldjka kjsdh 


Echoprint server installation
==========

.. code-block:: bash

    aptitude install default-jre tokyotyrant multitail

    cd
    cd src
    git clone https://github.com/echonest/echoprint-server.git
    cd echoprint-server


    mkdir -p /srv/openbroadcast.org/service
    cp -Rp solr/solr /srv/openbroadcast.org/service/
    cd /srv/openbroadcast.org/service/solr

    # solr
    java -Dsolr.solr.home=/srv/openbroadcast.org/service/solr/solr/ -Djava.awt.headless=true -jar start.jar

    # tokyo-tyrant
    mkdir /var/ttserver/
    /usr/sbin/ttserver -port 1978 -thnum 4 -pid /var/run/ttserver.pid /var/ttserver/prod_casket.tch#bnum=1000000




/etc/supervisor/conf.d/tt.prod.openbroadcast.org.conf
---------------------------------

.. code-block:: bash

    [program:tt.prod.openbroadcast.org.conf]
    directory=/root/
    command=/usr/sbin/ttserver -port 1978 -thnum 4 -pid /var/run/ttserver.pid /var/ttserver/prod_casket.tch#bnum=1000000
    user=root
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=HOME='/root/'
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=5
    stdout_logfile=/var/log/supervisor/tt.prod.openbroadcast.org



/etc/supervisor/conf.d/solr.prod.openbroadcast.org.conf
---------------------------------

.. code-block:: bash

    [program:solr.prod.openbroadcast.org.conf]
    directory=/srv/openbroadcast.org/service/solr
    command=/usr/bin/java -Dsolr.solr.home=/srv/openbroadcast.org/service/solr/solr/ -Djava.awt.headless=true -jar start.jar
    user=root
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=HOME='/root/'
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=5
    stdout_logfile=/var/log/supervisor/solr.prod.openbroadcast.org



start it!
---------------------------------

.. code-block:: bash

    supervisorctl reread
    supervisorctl update
    supervisorctl status
