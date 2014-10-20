Playout [a.k.a. pypo]
####################

Installation
************

.. note::

   Piratepad  `Piratepad wdd912  <http://piratepad.net/wdd912>`_.



Basic Setup
***************************

The playout-system is based on debian-wheezy: http://www.debian.org/releases/wheezy/

Setup the playout-box with debian (we will not explain this step any further here... :) ) - during setup create a 'pypo' user.


Installing pypo
***********************************

Required Packages
~~~~~~

.. code-block:: bash

    aptitude install python-setuptools supervisor sudo

    easy_install PIP
    pip install virtualenv

And finally THE APP!
~~~~~~

.. code-block:: bash

    su pypo
    cd ~/src/
    # git clone git@lab.hazelfire.com:hazelfire/obp/pypo.git # in case you have repo-access
    git clone https://github.com/hzlf/pypo.git
    cd pypo/pypo/

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt


Again, as root

.. code-block:: bash

    mkdir -p /var/log/pypo/ls/
    chown -R pypo:pypo /var/log/pypo

    # run the scripts [testing]

    cd /home/pypo/src/pypo/pypo/liquidsoap_scripts
    sudo -u pypo /usr/local/bin/liquidsoap --verbose -f ls_script.liq

    cd /home/pypo/src/pypo/pypo
    sudo -u pypo env/bin/python pypo.py


    # add to supervisor (symlink, or copy if you feel safer...)
    ln -s /home/pypo/src/pypo/conf/* /etc/supervisor/conf.d/
    supervisorctl reread
    supervisorctl update




Installing Liquidsoap [from source]
***********************************

Required Packages
~~~~~~

.. code-block:: bash

    apt-get -y --force-yes install git-core ocaml-findlib libao-ocaml-dev \
    libportaudio-ocaml-dev libmad-ocaml-dev libtaglib-ocaml-dev libalsa-ocaml-dev \
    libvorbis-ocaml-dev libladspa-ocaml-dev libxmlplaylist-ocaml-dev libflac-dev \
    libxml-dom-perl libxml-dom-xpath-perl patch autoconf libmp3lame-dev \
    libcamomile-ocaml-dev libcamlimages-ocaml-dev libtool libpulse-dev camlidl \
    libfaad-dev libpcre-ocaml-dev


Source Code & installation
~~~~~~~~~~~

.. code-block:: bash

    su pypo # important!!

    cd ~/src
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
    make # & go to buy a sixpack and make yourself comfortable

    exit # become root
    make install





Soundcard Configuration
***********************************



Digigram UAX220v2
~~~~~~~~~~~

.. code-block:: bash

    aptitude install alsa-base alsa-tools alsa-utils


.. code-block:: bash

    nano /etc/asound.conf



.. code-block:: bash

    # on-board card
    pcm.onboard {
        type hw
        card NVidia
    }
    ctl.onboard {
        type hw
        card NVidia
    }

    # UAX220 [usb]
    pcm.digigram {
        type hw
        card UAX220v2
    }

    ctl.digigram {
        type hw
        card UAX220v2
    }

    # dmix-plugin
    pcm.dmixer {
        type dmix
        ipc_key 1024
        ipc_perm 0666
        slave.pcm "digigram"
        slave {
            ### buffer_size - adapt in case of problems
            period_time 4
            period_size 1024
            buffer_size 8192
            ### default is 48000, try 44100 in case of problems.
            rate 44100
            ###
            format S16_LE
            ### Available Formats: S8 U8 S16_LE S16_BE U16_LE U16_BE S24_LE S24_BE U24_LE U24_BE
            ###               S32_LE S32_BE U32_LE U32_BE FLOAT_LE FLOAT_BE FLOAT64_LE FLOAT64_BE
            ###               IEC958_SUBFRAME_LE IEC958_SUBFRAME_BE MU_LAW A_LAW IMA_ADPCM MPEG GSM
            periods 128
            channels 2
        }
        bindings {
            0 0
            1 1
        }
    }

    # dsnooper-plugin - allows recording-access for multiple processes
    pcm.dsnooper {
        type dsnoop
        ipc_key 2048
        ipc_perm 0666
        slave.pcm "digigram"
        slave
        {
            period_time 4
            period_size 1024
            buffer_size 8192

            rate 44100
            format S16_LE
            periods 128
            channels 2
        }
        bindings {
            0 0
            1 1
        }
    }

    # duplexasym-plugin - defines full-duplex.
    pcm.duplexasym {
        type asym
        playback.pcm "dmixer"
        capture.pcm "dsnooper"
    }

    # Plug and Play auf alle Channels
    pcm.duplex {
        type plug
        slave.pcm "duplexasym"
    }

    ctl.duplex {
        type hw
        card UAX220v2
    }

    pcm.!default {
        type plug
        slave.pcm "duplexasym"
    }
