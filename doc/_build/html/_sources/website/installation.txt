packages [debian base install,  base-packages, additionally]:

.. code-block:: bash

    aptitude install supervisor sudo libmysqlclient-dev libjpeg-dev python-dev libxml2 libxml2-dev libxslt-dev
    aptitude install libsndfile libsndfile-dev libboost-dev libtag1-dev ffmpeg libmagic1

    easy_install PIP
    pip install virtualenv
    pip install setuptools --no-use-wheel --upgrade




# downgrade pip
pip install pip==1.4.1

# manual installation (don't ask why...)
pip install numpy
pip install django-phonenumber-field==0.2a3


pip install -r requirements/requirements.txt



