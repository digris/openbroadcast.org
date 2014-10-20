App Server(s)
#############


Main Application Server
*********************

 - node04: stage.openbroadcast.org
 - node05: prod.openbroadcast.org

both share the same setup



Chromaprint / AcoustID
==========

.. code-block:: bash

    aptitude install install libchromaprint-tools libchromaprint-dev


Echoprint installation
==========

.. code-block:: bash

    aptitude install  ffmpeg libboost-dev libtag1-dev zlib1g-dev

    cd
    cd src
    git clone https://github.com/echonest/echoprint-codegen.git
    cd echoprint-codegen/src
    make
    make install

    echoprint-codegen # test...




Echoprint server installation
==========

Only used on stage server. Echoprint server for production is located on node03.

.. code-block:: bash

    aptitude install default-jre tokyotyrant

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
    /usr/sbin/ttserver -port 1978 -thnum 4 -kl -pid /var/ttserver/pid -log /var/log/ttserver.log /var/ttserver/casket.tch#bnum=1000000



Echoprint services (on stage server)
::::::::::::::::::::::::::::::::::::

.. code-block:: bash

    nano /etc/supervisor/conf.d/echoprint.conf

.. code-block:: bash

    [program:tokyo]
    directory=/root/
    command=/usr/sbin/ttserver -port 1978 -thnum 4 -pid /var/run/ttserver.pid /var/ttserver/prod_casket.tch#bnum=1000000
    user=root
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=HOME='/root/'
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=5
    stdout_logfile=/var/log/supervisor/tokyo.log

    [program:solr]
    directory=/srv/openbroadcast.org/service/solr
    command=/usr/bin/java -Dsolr.solr.home=/srv/openbroadcast.org/service/solr/solr/ -Djava.awt.headless=true -jar start.jar
    user=root
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=HOME='/root/'
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=5
    stdout_logfile=/var/log/supervisor/solr.log






Audiotools installation
==========

repository: https://github.com/hzlf/python-audio-tools


===============  ===============  ===============
Format           Encoder          Decoder
===============  ===============  ===============
AIFF             Python           Python
MP3              mpg123           twolame
FLAC             Python           Python
Ogg FLAC         Python           flac
Ogg Vorbis       oggdec           oggdec
===============  ===============  ===============



.. code-block:: bash

    aptitude install mpg123 twolame lame flac vorbis-tools


Web Application
***************


packages

.. code-block:: bash

   aptitude install python-dev libmysqlclient-dev mysql libsndfile libsndfile-dev libmemcached-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libsox-fmt-all sox


.. code-block:: bash

    easy_install pip
    pip install pip==1.4.1
    pip install virtualenv

    mkdir -p /var/log/django/

.. code-block:: bash

    mkdir ~/.pip/cache
    nano ~/.pip/pip.conf

.. code-block:: bash

    [global]
    download_cache = ~/.pip/cache



Prepare storage directories

.. code-block:: bash

    mkdir -p /nas/storage/prod.openbroadcast.org/media
    mkdir /nas/storage/prod.openbroadcast.org/static
    mkdir /nas/storage/prod.openbroadcast.org/doc



Now try to run the deployment-script on your local machine.

.. note::

    VPN-connection required!

.. code-block:: bash

    cd <code root>
    fab prod_openbroadcast_ch deploy

.. note::

    If anything fails during deployment just try to run the script again...








