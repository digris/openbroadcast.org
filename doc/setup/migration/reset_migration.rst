Reset plattform to restart migration from `zero`
################################################


Remove all files on storage server
**********************************

.. note::

    Make sure to be in the right directory!!!!!!!!!!!!!!!!
    for stage this is:

    `/nas/storage/stage.openbroadcast.org/`


.. code-block:: bash

    rm -R static/*
    rm -R smedia/*
    rm -R doc/*
    rm -R media/*



Reset legacy databases
**********************


Tables on ":abbr:`legacy-legacy (a.k.a. ELGG)`"

.. code-block:: sql

    UPDATE `elgg_cm_master` SET `migrated` = NULL WHERE;


Tables on ":abbr:`legacy (a.k.a. Music Library)`"

.. code-block:: sql

    UPDATE `medias` SET `migrated` = NULL;
    UPDATE `artists` SET `migrated` = NULL;
    UPDATE `labels` SET `migrated` = NULL;
    UPDATE `releases` SET `migrated` = NULL;


./manage.py cleanup


remove unneeded entries
=======================



in python shell:
================

Release.objects.all().delete()
Media.objects.all().delete()
Artist.objects.all().delete()
Label.objects.all().delete()
Playlist.objects.all().delete()
Agency.objects.all().delete()

AgencyScope.objects.all().delete()
APILookup.objects.all().delete()
Distributor.objects.all().delete()
NameVariation.objects.all().delete()
PlaylistItem.objects.all().delete()
Series.objects.all().delete()

# arating
Vote.objects.all().delete()

# atracker
Event.objects.all().delete()

# bcmon
Playout.objects.all().delete()

# bcmon
Comment.objects.all().delete()

# exporter
Export.objects.all().delete()

# filer
File.objects.all().delete()
Folder.objects.all().delete()
Image.objects.all().delete()

# importer
Import.objects.all().delete()
ImportFile.objects.all().delete()

# tags
Tag.objects.all().delete()




# user & profiles
Invitation.objects.all().delete()
User.objects.exclude(username__in=['root', 'AnonymousUser']).delete()
Community.objects.all().delete()











thumbnails
==========

# maybe manual action required

TRUNCATE TABLE `easy_thumbnails_thumbnail`;
TRUNCATE TABLE `easy_thumbnails_source`;




reload fixtures
===============

./manage.py loaddata apps/abcast/fixtures/abcast.json




