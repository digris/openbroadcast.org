Overview
===================


vz node post-install
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    aptitude install build-essential python-setuptools supervisor git screen htop iftop bsd-mailx cron-apt locales ca-certificates


(configure email / postfix)

.. code-block:: bash

    nano /etc/aliases     # (map root to to sysadmin)
    nano /etc/postfix/transport   # (* smtp:[mx2.digris.ch])

    postalias /etc/aliases
    postmap /etc/postfix/transport

    /etc/init.d/postfix reload




vz nodes post-clone
~~~~~~~~~~~~~~~~~~~

on vz-host:

.. code-block:: bash

    nano /etc/vz/conf/<id>.conf # adapt ip and hostname


/etc/hosts/
~~~~~~~~~~~

.. code-block:: bash

    # obp dev
    95.211.179.43   stage.openbroadcast.org
    172.20.10.27    vz.obp
    172.20.10.201   node01.obp
    172.20.10.202   node02.obp
    172.20.10.203   node03.obp
    172.20.10.204   node04.obp
    172.20.10.205   node05.obp
    172.20.10.206   node06.obp
    172.20.10.207   node07.obp
    172.20.10.208   node08.obp
    172.20.10.209   node09.obp
    172.20.10.210   node10.obp


vz host
~~~~~~~

 - internal: 172.20.10.27
 - external: 95.211.179.27
 - kvm: 95.211.179.28 / 172.20.10.28

https://172.20.10.27:8006/



vz nodes
~~~~~~~~

node01 - WebHead
::::::


 - internal: 172.20.10.201
 - external: 95.211.179.43


.. code-block:: bash

    aptitude install nginx


node02 - Database
::::::


 - internal: 172.20.10.202

 - mariadb

.. code-block:: bash

    apt-get install python-software-properties
    apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db
    add-apt-repository 'deb http://mirror.netcologne.de/mariadb/repo/10.0/debian wheezy main'

    apt-get update
    apt-get install mariadb-server


node03 - Messaging
::::::

messaging & cache server

 - internal: 172.20.10.203
 - external: 95.211.179.44

See :doc:`messaging`



node04 - APP-Server Development
::::::

development app-server

 - internal: 172.20.10.204
 - external: 95.211.179.45

See :doc:`appserver`


node05 - APP-Server Production
::::::

app-server

 - internal: 172.20.10.205
 - external: 95.211.179.46

See :doc:`appserver`


node06 - Streaming & Stream-generation
::::::

streaming-server

 - internal: 172.20.10.206
 - external: 95.211.179.47

See :doc:`streaming` &
See :doc:`playout`

node07 - Mirror(s)
::::::

musicbrainz mirror

 - internal: 172.20.10.207


