Playout Server
###################


Master Stream-generation
*********************

 - Server: node06

Software in use:

 - :abbr:`pypo (Python Playout)`


Basic Setup
***************************

.. note::

    The playout-system is based on debian-wheezy: http://www.debian.org/releases/wheezy/

    Setup the playout-box with debian (we will not explain this step any further here... :) ) - during setup create a 'pypo' user.


.. code-block:: bash

    adduser pypo



Installing Liquidsoap [from source]
***********************************

.. note::

    Installed and tested version is:

    Liquidsoap 1.1.1+scm (git://github.com/savonet/liquidsoap.git@05fc245e72d87d4b87d00f867fd06b62c95abba0:20140221:151637)

Required Packages
===========

.. code-block:: bash

    apt-get -y --force-yes install git-core ocaml-findlib libao-ocaml-dev \
    libportaudio-ocaml-dev libmad-ocaml-dev libtaglib-ocaml-dev libalsa-ocaml-dev \
    libvorbis-ocaml-dev libladspa-ocaml-dev libxmlplaylist-ocaml-dev libflac-dev \
    libxml-dom-perl libxml-dom-xpath-perl patch autoconf libmp3lame-dev \
    libcamomile-ocaml-dev libcamlimages-ocaml-dev libtool libpulse-dev camlidl \
    libfaad-dev libpcre-ocaml-dev sudo


Source Code & installation
===============


.. note::

    Depending on the git version it looks like you'll have to ecit the Makefile.git

    comment:

    .. code-block:: bash

        #git branch --set-upstream-to=origin/master master
        #git submodule foreach "git branch --set-upstream-to=origin/master master"


.. code-block:: bash

    su pypo # important!!

    cd
    mkdir src
    cd src
    git clone https://github.com/savonet/liquidsoap-full
    cd liquidsoap-full
    make init
    make update


.. code-block:: bash

    cp PACKAGES.minimal PACKAGES

    sed -i "s/#ocaml-portaudio/ocaml-portaudio/g" PACKAGES
    sed -i "s/#ocaml-alsa/ocaml-alsa/g" PACKAGES
    sed -i "s/#ocaml-pulseaudio/ocaml-pulseaudio/g" PACKAGES
    sed -i "s/#ocaml-faad/ocaml-faad/g" PACKAGES

    ./bootstrap
    ./configure --with-user=pypo --with-group=pypo


    exit # become root

    cd /home/pypo/src/liquidsoap-full/
    make
    make install


Installing pypo
***********************************

Required Packages
================

.. code-block:: bash

    aptitude install python-setuptools supervisor sudo

    easy_install PIP
    pip install virtualenv

And finally THE APP!
===================

.. code-block:: bash

    su pypo
    cd
    mkdir src
    cd src
    # git clone git@lab.hazelfire.com:hazelfire/obp/pypo.git # in case you have repo-access
    git clone https://github.com/hzlf/pypo.git
    cd pypo/pypo/

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt


Again, as root

.. code-block:: bash

    mkdir /etc/airtime
    nano /etc/airtime/liquidsoap.cfg # in case you want to pre-populate the configs



.. code-block:: bash

    mkdir -p /var/log/pypo/ls/
    chown -R pypo:pypo /var/log/pypo

    # run the scripts [testing]

    cd /home/pypo/src/pypo/pypo/liquidsoap_scripts
    sudo -u pypo /usr/local/bin/liquidsoap --verbose -f ls_script.liq

    cd /home/pypo/src/pypo/pypo
    sudo -u pypo env/bin/python pypo.py


    # add to supervisor (symlink, or copy if you feel safer...)
    ln -s /home/pypo/src/pypo/conf/pypo.supervised.conf /etc/supervisor/conf.d/
    supervisorctl reread
    supervisorctl update