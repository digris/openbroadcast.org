#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import logging

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_delete
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields.json import JSONField
import magic
from celery.task import task
from lib.signals.unsignal import disable_for_loaddata

from alibrary.models import Media

log = logging.getLogger(__name__)

USE_CELERYD = True

AUTOIMPORT_MB = True
        
GENERIC_STATUS_CHOICES = (
    (0, _('Init')),
    (1, _('Done')),
    (2, _('Ready')),
    (3, _('Progress')),
    (99, _('Error')),
    (11, _('Other')),
)

# extra fields
from django_extensions.db.fields import *

def clean_upload_path(instance, filename):
    import unicodedata
    import string
    filename, extension = os.path.splitext(filename)
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')    
    folder = "import/%s/" % time.strftime("%Y%m%d%H%M%S", time.gmtime())
    return os.path.join(folder, "%s%s" % (cleaned_filename.lower(), extension.lower()))


class BaseModel(models.Model):

    uuid = UUIDField()
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()
    
    class Meta:
        abstract = True
        
        
class Import(BaseModel):

    class Meta:
        app_label = 'importer'
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ('-created', )
    
    
    user = models.ForeignKey(User, blank=True, null=True, related_name="import_user", on_delete=models.SET_NULL)

    uuid_key = models.CharField(max_length=60, null=True, blank=True)

    STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Done')),
        (2, _('Ready')),
        (3, _('Progress')),
        (99, _('Error')),
        (11, _('Other')),
    )
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
        
    TYPE_CHOICES = (
        ('web', _('Web Interface')),
        ('api', _('API')),
        ('fs', _('Filesystem')),
    )
    type = models.CharField(max_length="10", default='web', choices=TYPE_CHOICES)
    
    notes = models.TextField(blank=True, null=True, help_text=_('Optionally, just add some notes to this import if desired.'))
    
    

    def __unicode__(self):
        return "%s | %s" % (self.created, self.user)

    @models.permalink
    def get_absolute_url(self):
        return ('importer-import-update', [str(self.pk)])

    @models.permalink
    def get_delete_url(self):
        return ('importer-import-delete', [str(self.pk)])
    

    @task
    def get_stats(self):
        stats = {}
        stats['init'] = self.files.filter(status=0)
        stats['done'] = self.files.filter(status=1)
        stats['ready'] = self.files.filter(status=2)
        stats['working'] = self.files.filter(status=3)
        stats['warning'] = self.files.filter(status=4)
        stats['duplicate'] = self.files.filter(status=5)
        stats['queued'] = self.files.filter(status=6)
        stats['importing'] = self.files.filter(status=6)
        stats['error'] = self.files.filter(status=99)
        
        return stats



    def get_inserts(self):

        inserts = {
            'media_mb': [],
            'artist_mb': [],
            'release_mb': [],
        }


        for file in self.files.filter(status=2):
            it = file.import_tag
            if 'mb_track_id' in it:
                if not it['mb_track_id'] in inserts['media_mb']:
                    inserts['media_mb'].append(it['mb_track_id'])

            if 'mb_artist_id' in it:
                if not it['mb_artist_id'] in inserts['artist_mb']:
                    inserts['artist_mb'].append(it['mb_artist_id'])

            if 'mb_release_id' in it:
                if not it['mb_release_id'] in inserts['release_mb']:
                    inserts['release_mb'].append(it['mb_release_id'])




        return inserts

        

    def get_api_url(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'import', 'api_name': 'v1'})
        return '%s%s/' % (url, self.pk)
    
    def apply_import_tag(self, importfile, **kwargs):

        #print 'apply_import_tag:'
        #print importfile.import_tag

        if 'mb_release_id' in importfile.import_tag:
        
            mb_release_id = importfile.import_tag['mb_release_id']
            
            qs = self.files.exclude(pk=importfile.pk)
            importfiles = qs.filter(status=2)
            for file in importfiles:
                for mb in file.results_musicbrainz:
                    # got a match - try to apply
                    if 'mb_id' in mb and mb['mb_id'] == mb_release_id:
                        print 'GOT A MATCH!!!'
                        # main id
                        file.import_tag['mb_release_id'] = mb_release_id
                        # textual
                        file.import_tag['release'] = mb['name']
                        file.import_tag['artist'] = mb['artist']['name']
                        file.import_tag['name'] = mb['media']['name']
                        # mb ids
                        file.import_tag['mb_artist_id'] = mb['artist']['mb_id']
                        file.import_tag['mb_track_id'] = mb['media']['mb_id']
                        
                        kwargs['skip_apply_import_tag'] = True
                        file.save(**kwargs)

                        return

                


    def add_to_playlist(self, item):
        pass
    
    def add_to_collection(self, item):
        pass


    # importitem handling
    def add_importitem(self, item):

        ctype = ContentType.objects.get_for_model(item)

        try:
            item, created = ImportItem.objects.get_or_create(object_id=item.pk, content_type=ctype, import_session=self)
        except Exception, e:
            item = ImportItem.objects.filter(object_id=item.pk, content_type=ctype, import_session=self)[0]
            created = False


        if created:
            self.add_to_playlist(item)
            self.add_to_collection(item)
    
        return item
    
    def get_importitem_ids(self, ctype):
        ii_ids = ImportItem.objects.filter(content_type=ctype, import_session=self).values_list('object_id', flat=True)
        return ii_ids


    def save(self, *args, **kwargs):
        
        """
        stats = self.get_stats()
        
        if stats['done'].count() == self.files.count():
            self.status = 1
        
        if stats['done'].count() + stats['duplicate'].count() == self.files.count():
            self.status = 1
        
        if stats['error'].count() > 0:
            self.status = 99
        """   
        
        super(Import, self).save(*args, **kwargs)
 
    
class ImportFile(BaseModel):

    STATUS_CHOICES = (
        (0, _('Init')),
        (1, _('Done')),
        (2, _('Ready')),
        (3, _('Working')),
        (4, _('Warning')),
        (5, _('Duplicate')),
        (6, _('Queued')),
        (7, _('Importing')),
        (99, _('Error')),
        (11, _('Other')),
    )
    
    filename = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(max_length=256, upload_to=clean_upload_path)
    import_session = models.ForeignKey(Import, verbose_name=_('Import'), null=True, related_name='files')
    mimetype = models.CharField(max_length=100, blank=True, null=True)
    messages = JSONField(blank=True, null=True, default=None)
    
    """
    Result sets. Not stored in foreign model - as they are rather fix.
    """
    settings = JSONField(blank=True, null=True)
    results_tag = JSONField(blank=True, null=True)
    results_tag_status = models.PositiveIntegerField(verbose_name=_('Result Tags (ID3 & co)'), default=0, choices=GENERIC_STATUS_CHOICES)
    results_acoustid = JSONField(blank=True, null=True)
    results_acoustid_status = models.PositiveIntegerField(verbose_name=_('Result Musicbrainz'), default=0, choices=GENERIC_STATUS_CHOICES)
    results_musicbrainz = JSONField(blank=True, null=True)
    results_discogs_status = models.PositiveIntegerField(verbose_name=_('Result Musicbrainz'), default=0, choices=GENERIC_STATUS_CHOICES)
    results_discogs = JSONField(blank=True, null=True)
    #results_discogs_status = models.PositiveIntegerField(verbose_name=_('Result Discogs'), default=0, choices=GENERIC_STATUS_CHOICES)
    import_tag = JSONField(blank=True, null=True)
    
    # actual media!
    media = models.ForeignKey(Media, blank=True, null=True, related_name="importfile_media", on_delete=models.SET_NULL)
    imported_api_url = models.CharField(max_length=512, null=True, blank=True)
    error = models.CharField(max_length=512, null=True, blank=True)
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)


    class Meta:
        app_label = 'importer'
        verbose_name = _('Import File')
        verbose_name_plural = _('Import Files')
        ordering = ('created', )
    
    
    def __unicode__(self):
        return self.filename
        

    def get_api_url(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'importfile', 'api_name': 'v1'})
        return '%s%s/' % (url, self.pk)

    #@models.permalink
    def get_delete_url(self):
        #return ('importer-upload-delete', [str(self.pk)])
        return ''

    def process(self):
        log = logging.getLogger('importer.models.process')
        log.info('Start processing ImportFile: %s' % (self.pk))
        log.info('Path: %s' % (self.file.path))
        
        if USE_CELERYD:
            self.process_task.delay(self)
        else:
            self.process_task(self)
        
    @task
    def process_task(obj):
        
        # to prevent circular import errors
        from util.process import Process

        pre_sleep = 2
        log.debug('sleping for %s seconds' % pre_sleep)
        time.sleep(pre_sleep)
        log.debug('wakeup after %s seconds' % pre_sleep)


        if not obj.mimetype:
            try:
                mime = magic.Magic(mime=True)
                obj.mimetype = mime.from_file(obj.file.path.encode('ascii', 'ignore'))
            except Exception, e:
                log.warning('Unable to determine mimetype: %s' % e)


        processor = Process()
        
        # duplicate check by sha1
        media_id = processor.id_by_sha1(obj.file)
        log.debug('Got something by sha1?: %s' % media_id)
        # duplicate check by echoprint
        if not media_id:
            media_id = processor.id_by_echoprint(obj.file)
            log.debug('Got something by echoprint?: %s' % media_id)

        try:
            metadata = processor.extract_metadata(obj.file)
            if metadata:
                log.info('sucessfully extracted metadata')

            # check if we have obp-data available
            obp_media_uuid = metadata['obp_media_uuid'] if 'obp_media_uuid' in metadata else None

            if obp_media_uuid:
                print
                print '******************************************************************'
                print 'got obp match'
                print 'obp_media_uuid: %s' % obp_media_uuid
                print '******************************************************************'
                print

                obj.status = 5
                obj.media = Media.objects.get(uuid=obp_media_uuid)
                obj.save()
                return

            # check if we have musicbrainz-data available
            media_mb_id = metadata['media_mb_id'] if 'media_mb_id' in metadata else None
            artist_mb_id = metadata['artist_mb_id'] if 'artist_mb_id' in metadata else None
            release_mb_id = metadata['release_mb_id'] if 'release_mb_id' in metadata else None

            media_name = metadata['media_name'] if 'media_name' in metadata else None
            artist_name = metadata['artist_name'] if 'artist_name' in metadata else None
            release_name = metadata['release_name'] if 'release_name' in metadata else None
            media_tracknumber = metadata['media_tracknumber'] if 'media_tracknumber' in metadata else None

            if media_mb_id and artist_mb_id and release_mb_id:
                print
                print '******************************************************************'
                print 'got musicbrainz match'
                print 'media_name: %s' % media_name
                print 'artist_name: %s' % artist_name
                print 'release_name: %s' % release_name
                print 'media_mb_id: %s' % media_mb_id
                print 'artist_mb_id: %s' % artist_mb_id
                print 'release_mb_id: %s' % release_mb_id
                print 'media_tracknumber: %s' % media_tracknumber
                print '******************************************************************'
                print

                if not media_id:
                    print 'directly applying mb-data and send to import-queue'

                    # build import tag
                    import_tag = {
                        'name': media_name,
                        'artist': artist_name,
                        'release': release_name,
                        'media_tracknumber': media_tracknumber,
                        'mb_track_id': media_mb_id,
                        'mb_artist_id': artist_mb_id,
                        'mb_release_id': release_mb_id,
                    }

                    obj.import_tag = import_tag
                    obj.status = 6
                    obj.save()
                    return



        except Exception, e:
            print e
            obj.error = '%s' % e
            obj.status = 99
            obj.save()
            return
        
        # try to get media by id returned from fingerprinter
        media = None
        if media_id:
            try:
                media = Media.objects.get(pk=media_id)
                if media:
                    obj.status = 5
                    obj.media = media
                    if obj.import_session:
                        obj.import_session.add_importitem(obj)
                    obj.save()

                    return
            except:
                pass
        
        
        if media:
            obj.results_tag = metadata
            obj.media = media

        else:
            pass
            
    
        #time.sleep(1)
        """
        """
        obj.results_tag = metadata
        obj.status = 3
        obj.results_tag_status = True
        obj.save()
        log.info('sucessfully aquired metadata')


        obj.results_acoustid = processor.get_aid(obj.file)
        obj.results_acoustid_status = True
        obj.save()

        obj.results_musicbrainz = processor.get_musicbrainz(obj)
        obj.results_discogs_status = True # TODO: ???
        obj.save()
        
        # requeue if no results yet
        if len(obj.results_musicbrainz) < 1:
            s = {'skip_tracknumber': True}
            obj.settings = s
            obj.save()
            obj.results_musicbrainz = processor.get_musicbrainz(obj)
            obj.save()
            
        
        obj.status = 2
        
        if media:
            obj.status = 5
            # add to session
            if obj.import_session:
                obj.import_session.add_importitem(obj)
        
        obj.results_tag_status = True
        obj.save()
    

    
    
    def do_import(self):
        log = logging.getLogger('importer.models.do_import')
        log.info('Start importing ImportFile: %s' % (self.pk))
        log.info('Path: %s' % (self.file.path))
        
        if USE_CELERYD:
            self.import_task.delay(self)
        else:
            self.import_task(self)
        
    @task
    def import_task(obj):

        log = logging.getLogger('importer.models.import_task')
        log.info('Starting import task for:  %s' % (obj.pk))

        pre_sleep = 1
        log.debug('sleping for %s seconds' % pre_sleep)
        time.sleep(pre_sleep)
        log.debug('wakeup after %s seconds' % pre_sleep)


        # to prevent circular import errors
        from util.importer import Importer
        importer = Importer()
        
        media, status = importer.run(obj)

        if media:
            obj.media = media

            obj.status = 1
            
        else:
            obj.status = 99
        
        log.info('Ending import task for:  %s' % (obj.pk))
        obj.save()
    
    def save(self, skip_apply_import_tag=False, *args, **kwargs):
        
        msg = {'key': 'save', 'content': 'object saved'}
        #self.messages.update(msg);

        # self._pushy_ignore = True

        if not self.filename:
            self.filename = self.file.name
            
        # check/update import_tag
        if self.status == 2: # ready
            from util.importer import Importer
            importer = Importer()
            
            self.import_tag = importer.complete_import_tag(self)
            

        if self.status == 2: # ready
            # try to apply import_tag to other files of this import session
            if not skip_apply_import_tag and self.import_session:
                # TODO: this breaks the interface, as nearly infinite loop arises
                #print 'skipping import_session.apply_import_tag'
                print 'import_session.apply_import_tag'
                self.import_session.apply_import_tag(self)
                
        # check import_tag for completeness
        if self.status == 2 or self.status == 4: # ready
            media = self.import_tag.get('name', None)
            artist = self.import_tag.get('artist', None)
            release = self.import_tag.get('release', None)
            
            if media and artist and release:
                self.status = 2
            else:
                self.status = 4

        super(ImportFile, self).save(*args, **kwargs)

@disable_for_loaddata
def post_save_importfile(sender, **kwargs):

    obj = kwargs['instance']

    # init: newly uploaded/created file. let's process (gather data) it
    if obj.status == 0:
        obj.process()

    if obj.status == 6:
        obj.do_import()
      
post_save.connect(post_save_importfile, sender=ImportFile)      
  
def post_delete_importfile(sender, **kwargs):
    obj = kwargs['instance']
    try:
        os.remove(obj.file.path)
    except:
        pass
      
post_delete.connect(post_delete_importfile, sender=ImportFile)












"""
ImportItem
store relations to objects created/assigned during that specific import
"""

class ImportItem(BaseModel):
        
    # limit to alibrary objects
    ct_limit = models.Q(app_label = 'alibrary', model = 'media') | \
    models.Q(app_label = 'alibrary', model = 'release') | \
    models.Q(app_label = 'alibrary', model = 'artist') | \
    models.Q(app_label = 'alibrary', model = 'label')
    
    import_session = models.ForeignKey(Import, verbose_name=_('Import'), null=True, related_name='importitem_set')
    
    content_type = models.ForeignKey(ContentType, limit_choices_to = ct_limit)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'importer'
        verbose_name = _('Import Item')
        verbose_name_plural = _('Import Items')
        #ordering = ('-created', )
        
    def __unicode__(self):
        try:
            return '%s | %s' % (ContentType.objects.get_for_model(self.content_object), self.content_object.name)
        except:
            return '%s' % (self.pk)
            
    
    def save(self, *args, **kwargs):
        super(ImportItem, self).save(*args, **kwargs) 













        
        