import os
import sys
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

DELETE_PATHS = ['import', 'export', 'alibrary',]

class Command(BaseCommand):

    can_import_settings = True

    def handle(self, *args, **options):

        print '***********************************************'
        print '           COMPLETE DATA RESET                 '
        print '***********************************************'
        print



        confirm = raw_input('are you really sure? enter "y" to continue: ')

        if not confirm == 'y':
            sys.exit(1)


        print
        print '* deleting files:'
        print

        if MEDIA_ROOT:
            for dir in DELETE_PATHS:
                path = os.path.join(MEDIA_ROOT, dir)
                print 'deleting: %s' % path
                confirm = raw_input('enter "y" to continue: ')
                if confirm == 'y' and os.path.exists(path):
                    shutil.rmtree(path)





        print
        print '* wiping database:'
        print

        from alibrary.models import *
        from arating.models import Vote
        from atracker.models import Event
        from bcmon.models import Playout
        from exporter.models import Export
        from importer.models import Import, ImportFile
        from actstream.models import Action, Follow

        Action.objects.all().delete()
        Follow.objects.all().delete()

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


        # exporter
        Export.objects.all().delete()

        # filer
        File.objects.all().delete()
        Folder.objects.all().delete()
        Image.objects.all().delete()

        # importer
        Import.objects.all().delete()
        ImportFile.objects.all().delete()

        from django.contrib.comments import Comment
        Comment.objects.all().delete()





        print
        print '* reseting counters:'
        print
        from obp_legacy.models import Medias, Artists, Releases, Labels
        Medias.objects.using('legacy').update(migrated = None)
        Artists.objects.using('legacy').update(migrated = None)
        Releases.objects.using('legacy').update(migrated = None)
        Labels.objects.using('legacy').update(migrated = None)

        from obp_legacy.models_legacy import ElggCmMaster
        ElggCmMaster.objects.using('legacy_legacy').update(migrated = None)



        print
        print '* reseting users:'
        print
        from django.contrib.auth.models import User
        from profiles.models import Profile, Community
        #User.objects.exclude(username__in=['root', 'AnonymousUser']).delete()
        #Community.objects.all().delete()
