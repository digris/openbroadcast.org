#-*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand, NoArgsCommand
from django.conf import settings
from django.db.models import F, Q

#from alibrary.models import Artist, Release, Media, Label, Relation, License

from filer.models.filemodels import File
from filer.models.audiomodels import Audio
from filer.models.imagemodels import Image

from obp_legacy.models import *

from datetime import datetime

from lib.util import filer_extra

from obp_legacy.util.migrator import get_release_by_legacy_object
from obp_legacy.util.migrator import get_label_by_legacy_object
from obp_legacy.util.migrator import get_artist_by_legacy_object
from obp_legacy.util.migrator import get_media_by_legacy_object
from obp_legacy.util.migrator import get_playlist_by_legacy_object
from obp_legacy.util.migrator import get_user_by_legacy_legacy_object
from obp_legacy.util.migrator import get_community_by_legacy_legacy_object
from obp_legacy.util.migrator import get_license_by_legacy_object


DEFAULT_LIMIT = 100
FORCE_UPDATE = True


def id_to_location(id):
    l = "%012d" % id
    return '%d/%d/%d' % (int(l[0:4]), int(l[4:8]), int(l[8:12]))
    

"""
Needed db changes on legacy_legacy:

ALTER TABLE `elgg_cm_master` ADD `migrated` DATETIME  NULL  AFTER `locked_userident`;

"""

class LegacyImporter(object):

    def __init__(self, * args, **kwargs):
        self.object_type = kwargs.get('object_type')
        self.id = kwargs.get('id')
        self.legacy_id = kwargs.get('legacy_id')
        self.limit = kwargs.get('limit')
        self.verbosity = int(kwargs.get('verbosity', 1))
        
    def run(self):

        if not self.check():
            import sys
            print '-------------------------------------------------'
            print 'Self-check failed.'
            print
            sys.exit(2)


        if self.id or self.legacy_id:

            if(self.object_type == 'media'):

                if self.legacy_id:
                    legacy_obj = Medias.objects.using('legacy').get(id=int(self.legacy_id))
                    obj, status = get_media_by_legacy_object(legacy_obj, force=True)
                    legacy_obj.migrated = datetime.now()
                    legacy_obj.save()

            if(self.object_type == 'release'):

                if self.legacy_id:
                    legacy_obj = Releases.objects.using('legacy').get(id=int(self.legacy_id))
                    obj, status = get_release_by_legacy_object(legacy_obj, force=True)
                    legacy_obj.migrated = datetime.now()
                    legacy_obj.save()

            if(self.object_type == 'artist'):

                if self.legacy_id:
                    legacy_obj = Artists.objects.using('legacy').get(id=int(self.legacy_id))
                    obj, status = get_artist_by_legacy_object(legacy_obj, force=True)
                    legacy_obj.migrated = datetime.now()
                    legacy_obj.save()

            if(self.object_type == 'label'):

                if self.legacy_id:
                    legacy_obj = Labels.objects.using('legacy').get(id=int(self.legacy_id))
                    obj, status = get_label_by_legacy_object(legacy_obj, force=True)
                    legacy_obj.migrated = datetime.now()
                    legacy_obj.save()

            if(self.object_type == 'user'):

                if self.legacy_id:

                    from obp_legacy.models_legacy import ElggUsers
                    legacy_obj = ElggUsers.objects.using('legacy_legacy').get(ident=int(self.legacy_id))
                    obj, status = get_user_by_legacy_legacy_object(legacy_obj, force=True)
                    legacy_obj.migrated = datetime.now()
                    legacy_obj.save()

            if(self.object_type == 'playlist'):

                if self.legacy_id:

                    from obp_legacy.models_legacy import ElggCmMaster

                    legacy_obj = ElggCmMaster.objects.using('legacy_legacy').get(ident=int(self.legacy_id))
                    obj, status = get_playlist_by_legacy_object(legacy_obj, force=True)
                    legacy_obj.migrated = datetime.now()
                    legacy_obj.save()

            return

        if(self.object_type == 'release'):

            objects = Releases.objects.using('legacy').filter(Q(migrated__lte=F('updated')) | Q(migrated=None)).exclude(name=u'').all()[0:self.limit]

            for legacy_obj in objects:
                obj, status = get_release_by_legacy_object(legacy_obj, force=FORCE_UPDATE)
                legacy_obj.migrated = datetime.now()
                legacy_obj.save()
        
        
        if(self.object_type == 'media'):

            #objects = Medias.objects.using('legacy').filter(migrated=None).exclude(name=u'').order_by('-created').all()[0:self.limit]
            objects = Medias.objects.using('legacy').filter(Q(migrated__lte=F('updated')) | Q(migrated=None)).exclude(name=u'').order_by('-created').all()[0:self.limit]

            print 'NUM OBJECTS: %s' % objects.count()
        
            for legacy_obj in objects:
                obj, status = get_media_by_legacy_object(legacy_obj, force=FORCE_UPDATE)
                legacy_obj.migrated = datetime.now()
                legacy_obj.save()
                
                        
        if(self.object_type == 'label'):

            #objects = Labels.objects.using('legacy').filter(migrated=None).exclude(name=u'').all()[0:self.limit]
            objects = Labels.objects.using('legacy').filter(Q(migrated__lte=F('updated')) | Q(migrated=None)).exclude(name=u'').all()[0:self.limit]
        
            for legacy_obj in objects:
                obj, status = get_label_by_legacy_object(legacy_obj, force=FORCE_UPDATE)
                legacy_obj.migrated = datetime.now()
                legacy_obj.save()
                
                        
        if(self.object_type == 'artist'):

            #objects = Artists.objects.using('legacy').filter(migrated=None).exclude(name=u'').all()[0:self.limit]
            objects = Artists.objects.using('legacy').filter(Q(migrated__lte=F('updated')) | Q(migrated=None)).exclude(name=u'').all()[0:self.limit]
        
            for legacy_obj in objects:
                obj, status = get_artist_by_legacy_object(legacy_obj, force=FORCE_UPDATE)
                legacy_obj.migrated = datetime.now()
                legacy_obj.save()
                
                        
        if(self.object_type == 'user'):

            #objects = Users.objects.using('legacy').filter(migrated=None).exclude(name=u'').all()[0:5]
            #objects = Users.objects.using('legacy').exclude(username=u'').all()[0:1000]
            from obp_legacy.models_legacy import ElggUsers
            objects = ElggUsers.objects.using('legacy_legacy').filter(user_type='person')[0:self.limit]
            #objects = ElggUsers.objects.using('legacy_legacy').filter(user_type='person', ident=9)[0:2000] # jonas
        
            for legacy_obj in objects:
                obj, status = get_user_by_legacy_legacy_object(legacy_obj)                
                #legacy_obj.migrated = datetime.now()
                legacy_obj.save()
                
                        
        if(self.object_type == 'group'):

            #objects = Users.objects.using('legacy').filter(migrated=None).exclude(name=u'').all()[0:5]
            #objects = Users.objects.using('legacy').exclude(username=u'').all()[0:1000]
            from obp_legacy.models_legacy import ElggUsers
            objects = ElggUsers.objects.using('legacy_legacy').filter(user_type='community')[0:self.limit]
        
            for legacy_obj in objects:
                obj, status = get_community_by_legacy_legacy_object(legacy_obj)                
                #legacy_obj.migrated = datetime.now()
                legacy_obj.save()
                
                        
        if(self.object_type == 'playlist'):

            from obp_legacy.models_legacy import ElggCmMaster
            objects = ElggCmMaster.objects.using('legacy_legacy').filter(type='Container', migrated=None)[0:self.limit]

            for legacy_obj in objects:
                obj, status = get_playlist_by_legacy_object(legacy_obj)                
                legacy_obj.migrated = datetime.now()
                legacy_obj.save()


        if(self.object_type == 'license'):

            from obp_legacy.models import Licenses
            objects = Licenses.objects.using('legacy').all()

            for legacy_obj in objects:
                print legacy_obj
                obj, status = get_license_by_legacy_object(legacy_obj)



    def check(self):

        status = True

        """
        check if directories exist & permissions match
        """
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        legacy_storage = getattr(settings, 'LEGACY_STORAGE_ROOT', None)

        print 'media root:     %s' % media_root
        print 'legacy storage: %s' % legacy_storage


        """
        check if legacy-databases are ready
        """



        return status

                
        




class Command(NoArgsCommand):
    """
    Import directory structure into alibrary:

        manage.py import_folder --path=/tmp/assets/images
    """

    option_list = BaseCommand.option_list + (
        make_option('--type',
            action='store',
            dest='object_type',
            default=False,
            help='Import files located in the path into django-filer'),
        make_option('--id',
            action='store',
            dest='id',
            default=False,
            help='Specify an ID to run migration on'),
        make_option('--legacy_id',
            action='store',
            dest='legacy_id',
            default=False,
            help='Specify a Legacy-ID to run migration on'),
        make_option('--limit',
            action='store',
            dest='limit',
            default=100,
            help='How many rows to process... defaults to 100'),
        )

    def handle_noargs(self, **options):
        legacy_importer = LegacyImporter(**options)
        legacy_importer.run()
