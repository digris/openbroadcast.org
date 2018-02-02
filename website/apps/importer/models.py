# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import time
import unicodedata
import string
import ntpath
import magic
from alibrary.models import Media, Artist, Release
from celery.task import task
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django_extensions.db.fields.json import JSONField
from base.signals.unsignal import disable_for_loaddata
from django_extensions.db.fields import UUIDField, CreationDateTimeField, ModificationDateTimeField

from .signals import importitem_created

log = logging.getLogger(__name__)

USE_CELERYD = getattr(settings, 'IMORTER_USE_CELERYD', False)
AUTOIMPORT_MB = getattr(settings, 'IMORTER_AUTOIMPORT_MB', True)
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')


GENERIC_STATUS_CHOICES = (
    (0, _('Init')),
    (1, _('Done')),
    (2, _('Ready')),
    (3, _('Progress')),
    (99, _('Error')),
    (11, _('Other')),
)


def unsafe_join(base, *paths):
    """
    Join one or more path components to the base path component intelligently.
    Return a normalized, absolute version of the final path.
    Does *not* raise ValueError if the final path isn't located inside of the base path
    component.
    """
    base = force_text(base)
    paths = [force_text(p) for p in paths]
    final_path = os.path.abspath(os.path.join(base, *paths))

    return final_path

class UnuspiciousStorage(FileSystemStorage):
    """
    Allows accessing files stored outside of `MEDIA_ROOT`
    """
    def path(self, name):
        return unsafe_join(self.location, name)


def clean_upload_path(instance, filename):

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

    STATUS_INIT = 0
    STATUS_DONE = 1
    STATUS_READY = 2
    STATUS_PROGRESS = 3
    STATUS_ERROR = 99
    STATUS_OTHER = 11
    STATUS_CHOICES = (
        (STATUS_INIT, _('Init')),
        (STATUS_DONE, _('Done')),
        (STATUS_READY, _('Ready')),
        (STATUS_PROGRESS, _('Progress')),
        (STATUS_ERROR, _('Error')),
        (STATUS_OTHER, _('Other')),
    )

    TYPE_WEB = 'web'
    TYPE_API = 'api'
    TYPE_FS = 'fs'
    TYPE_CHOICES = (
        (TYPE_WEB, _('Web Interface')),
        (TYPE_API, _('API')),
        (TYPE_FS, _('Filesystem')),
    )

    user = models.ForeignKey(
        User,
        blank=True, null=True,
        related_name="import_user",
        on_delete=models.SET_NULL
    )
    uuid_key = models.CharField(
        max_length=60,
        null=True, blank=True
    )

    status = models.PositiveIntegerField(
        default=STATUS_INIT, choices=STATUS_CHOICES
    )

    type = models.CharField(
        max_length=10,
        default=TYPE_WEB,
        choices=TYPE_CHOICES
    )
    notes = models.TextField(
        blank=True, null=True
    )

    # TODO: not so nice - field is used to ad imported files to a specific collection
    collection_name = models.CharField(
        max_length=250,
        blank=True, null=True
    )

    class Meta:
        app_label = 'importer'
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ('-created', )

    def __unicode__(self):
        return "%s | %s" % (self.created, self.user)

    @models.permalink
    def get_absolute_url(self):
        return ('importer-import-update', [str(self.pk)])

    @models.permalink
    def get_delete_url(self):
        return ('importer-import-delete', [str(self.pk)])

    #@task
    def get_stats(self):

        stats = {}

        stats['init'] = self.files.filter(
            status=ImportFile.STATUS_INIT
        )
        stats['done'] = self.files.filter(
            status=ImportFile.STATUS_DONE
        )
        stats['ready'] = self.files.filter(
            status=ImportFile.STATUS_READY
        )
        stats['working'] = self.files.filter(
            status=ImportFile.STATUS_PROGRESS
        )
        stats['warning'] = self.files.filter(
            status=ImportFile.STATUS_WARNING
        )
        stats['duplicate'] = self.files.filter(
            status=ImportFile.STATUS_DUPLICATE
        )
        stats['queued'] = self.files.filter(
            status=ImportFile.STATUS_QUEUED
        )
        stats['importing'] = self.files.filter(
            status=ImportFile.STATUS_IMPORTING
        )
        stats['error'] = self.files.filter(
            status=ImportFile.STATUS_ERROR
        )

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
        url = reverse('api_dispatch_list',
                      kwargs={'resource_name': 'import', 'api_name': 'v1'}
                      )
        return '%s%s/' % (url, self.pk)

    def apply_import_tag(self, importfile, **kwargs):

        if 'mb_release_id' in importfile.import_tag:

            mb_release_id = importfile.import_tag['mb_release_id']

            qs = self.files.exclude(pk=importfile.pk)
            importfiles = qs.filter(status=ImportFile.STATUS_READY)
            for file in importfiles:
                for mb in file.results_musicbrainz:

                    if 'mb_id' in mb and mb['mb_id'] == mb_release_id:

                        file.import_tag['mb_release_id'] = mb_release_id
                        file.import_tag['release'] = mb['name']
                        file.import_tag['artist'] = mb['artist']['name']
                        file.import_tag['name'] = mb['media']['name']
                        file.import_tag['mb_artist_id'] = mb['artist']['mb_id']
                        file.import_tag['mb_track_id'] = mb['media']['mb_id']

                        kwargs['skip_apply_import_tag'] = True
                        file.save(**kwargs)

                        return

    def add_to_playlist(self, item):
        pass

    def add_to_collection(self, item):
        pass

    def add_importitem(self, item):

        log.debug('add importitem: {}'.format(item))
        ctype = ContentType.objects.get_for_model(item)

        created = False
        try:
            item, created = ImportItem.objects.get_or_create(
                object_id=item.pk,
                content_type=ctype,
                import_session=self
            )
        except Exception as e:
            log.warning('unable to create importitem: {} - {}'.format(item, e))
            pass

        try:
            item = ImportItem.objects.filter(
                object_id=item.pk,
                content_type=ctype,
                import_session=self)[0]
            created = False
        except Exception as e:
            #log.warning('unable to add importitem: {} - {}'.format(item, e))
            pass

        if created:
            self.add_to_playlist(item)
            self.add_to_collection(item)

        return item

    def get_importitems(self):

        qs = self.importitem_set.order_by('content_type__model')
        cts = ['artist', 'release', 'media', 'label']

        importitems = {}
        for obj in [i for i in qs if i.content_object and i.content_type.model in cts]:
            ct = '{}'.format(obj.content_type.model)
            if not ct in importitems:
                importitems[ct] = {
                    'name': obj.content_object._meta.verbose_name_plural,
                    'url': reverse('alibrary-{}-list'.format(ct)),
                    'items': []
                }

            importitems[ct]['items'].append(
                obj.content_object
            )

        return importitems




    def get_importitem_ids(self, ctype):
        ii_ids = ImportItem.objects.filter(
            content_type=ctype,
            import_session=self
        ).values_list('object_id', flat=True)
        return ii_ids

    def save(self, *args, **kwargs):
        super(Import, self).save(*args, **kwargs)


class ImportFile(BaseModel):

    STATUS_INIT = 0
    STATUS_DONE = 1
    STATUS_READY = 2
    STATUS_PROGRESS = 3
    STATUS_WARNING = 4
    STATUS_DUPLICATE = 5
    STATUS_QUEUED = 6
    STATUS_IMPORTING = 7
    STATUS_ERROR = 99
    STATUS_OTHER = 11
    STATUS_CHOICES = (
        (STATUS_INIT, _('Init')),
        (STATUS_DONE, _('Done')),
        (STATUS_READY, _('Ready')),
        (STATUS_PROGRESS, _('Working')),
        (STATUS_WARNING, _('Warning')),
        (STATUS_DUPLICATE, _('Duplicate')),
        (STATUS_QUEUED, _('Queued')),
        (STATUS_IMPORTING, _('Importing')),
        (STATUS_ERROR, _('Error')),
        (STATUS_OTHER, _('Other')),
    )

    status = models.PositiveIntegerField(default=STATUS_INIT, choices=STATUS_CHOICES)
    filename = models.CharField(max_length=1024, blank=True, null=True)
    file = models.FileField(max_length=1024, upload_to=clean_upload_path, storage=UnuspiciousStorage())
    import_session = models.ForeignKey(Import, verbose_name=_('Import'), null=True, related_name='files')
    mimetype = models.CharField(max_length=100, blank=True, null=True)
    messages = JSONField(blank=True, null=True, default=None)

    # Result sets - used for further processing.
    settings = JSONField(blank=True, null=True)
    results_tag = JSONField(blank=True, null=True)
    results_tag_status = models.PositiveIntegerField(verbose_name=_('Result Tags (ID3 & co)'), default=0, choices=GENERIC_STATUS_CHOICES)
    results_acoustid = JSONField(blank=True, null=True)
    results_acoustid_status = models.PositiveIntegerField(verbose_name=_('Result Musicbrainz'), default=0, choices=GENERIC_STATUS_CHOICES)
    results_musicbrainz = JSONField(blank=True, null=True)
    results_discogs_status = models.PositiveIntegerField(verbose_name=_('Result Musicbrainz'), default=0, choices=GENERIC_STATUS_CHOICES)
    results_discogs = JSONField(blank=True, null=True)
    import_tag = JSONField(blank=True, null=True)

    # assigned media object
    media = models.ForeignKey(Media, blank=True, null=True, related_name="importfile_media", on_delete=models.SET_NULL)

    imported_api_url = models.CharField(max_length=512, null=True, blank=True)
    error = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        app_label = 'importer'
        verbose_name = _('Import File')
        verbose_name_plural = _('Import Files')
        ordering = ('created', )


    def __unicode__(self):

        if self.file and self.file.path:
            return ntpath.basename(self.file.path)

        return self.filename

    def get_api_url(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'importfile', 'api_name': 'v1'})
        return '%s%s/' % (url, self.pk)

    def get_delete_url(self):
        return ''

    def identify(self):
        log.info('Start processing ImportFile: %s at %s' % (self.pk, self.file.path))

        if USE_CELERYD:
            self.identify_task.delay(self)
        else:
            self.identify_task(self)

    @task
    def identify_task(obj):

        pre_sleep = 1
        time.sleep(pre_sleep)

        if not obj.mimetype:
            try:
                mime = magic.Magic(mime=True)
                obj.mimetype = mime.from_file(obj.file.path.encode('ascii', 'ignore'))
            except Exception as e:
                log.warning('Unable to determine mimetype: %s' % e)


        from util.identifier import Identifier
        identifier = Identifier()

        # get import settings
        reimport_duplicate = obj.settings.get('reimport_duplicate', False)
        if reimport_duplicate:
            log.debug('duplicate reimport forced for pk: {}'.format(obj.pk))


        media_id = None

        if not reimport_duplicate:

            metadata = identifier.extract_metadata(obj.file)

            if not metadata:
                log.warning('unable to extracted metadata')

            # duplicate check by sha1
            try:
                media_id = identifier.id_by_sha1(obj.file)
                log.debug('duplicate by SHA1: {}'.format(media_id))
            except:
                log.warning('unable to identify by sha1: {}'.format(media_id))

            # duplicate check by name matching
            if not media_id:
                try:
                    media_id = identifier.id_by_metadata(obj.file)
                    log.debug('duplicate by metadata: : {}'.format(media_id))
                except:
                    log.warning('unable to identify by metadata: {}'.format(media_id))

            # duplicate check by fprint
            if not media_id:
                try:
                    media_id = identifier.id_by_fprint(obj.file)
                    log.debug('possible duplicate by fprint: {}'.format(media_id))

                    # if possible duplicate and to be imported file have
                    # both a musicbrainz recording id then ignore
                    # the assigned duplicate.
                    # TODO: yes - this is not so nicely done...
                    try:
                        if metadata and 'media_mb_id' in metadata and metadata['media_mb_id']:

                            if Media.objects.get(pk=media_id).relations.filter(
                                    url__contains='musicbrainz.org/recording/'
                            ).exists():
                                media_id = None
                    except:
                        pass

                except:
                    log.warning('unable to identify by fprint: {}'.format(media_id))



        try:
            metadata = identifier.extract_metadata(obj.file)
            if not metadata:
                log.warning('unable to extracted metadata')

            # check if we have obp-data available in files meta
            obp_media_uuid = metadata['obp_media_uuid'] if 'obp_media_uuid' in metadata else None

            if obp_media_uuid:

                try:
                    obj.status = ImportFile.STATUS_DUPLICATE
                    obj.media = Media.objects.get(uuid=obp_media_uuid)
                    obj.save()
                    return
                except Media.DoesNotExist as e:
                    pass

            # check if we have musicbrainz-data available
            media_mb_id = metadata['media_mb_id'] if 'media_mb_id' in metadata else None
            artist_mb_id = metadata['artist_mb_id'] if 'artist_mb_id' in metadata else None
            release_mb_id = metadata['release_mb_id'] if 'release_mb_id' in metadata else None

            media_name = metadata['media_name'] if 'media_name' in metadata else None
            artist_name = metadata['artist_name'] if 'artist_name' in metadata else None
            release_name = metadata['release_name'] if 'release_name' in metadata else None
            media_tracknumber = metadata['media_tracknumber'] if 'media_tracknumber' in metadata else None

            if AUTOIMPORT_MB and media_mb_id and artist_mb_id and release_mb_id:


                # print
                # print '******************************************************************'
                # print 'got musicbrainz match'
                # print 'media_name: %s' % media_name
                # print 'artist_name: %s' % artist_name
                # print 'release_name: %s' % release_name
                # print 'media_mb_id: %s' % media_mb_id
                # print 'artist_mb_id: %s' % artist_mb_id
                # print 'release_mb_id: %s' % release_mb_id
                # print 'media_tracknumber: %s' % media_tracknumber
                # print '******************************************************************'
                # print

                if not media_id:

                    log.debug('directly applying mb-data and send to import-queue')

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
                    obj.status = ImportFile.STATUS_QUEUED
                    obj.save()
                    return

        except Exception as e:
            log.warning('unable to process metadata: %s' % e)
            obj.error = '%s' % e
            obj.status = ImportFile.STATUS_ERROR
            obj.save()
            return

        # try to get media by id returned from fingerprinter
        media = None
        if media_id:
            try:
                media = Media.objects.get(pk=media_id)
                if media:
                    obj.status = ImportFile.STATUS_DUPLICATE
                    obj.media = media


                    # TODO: improve this part
                    if obj.import_session:
                        obj.import_session.add_importitem(media)
                        if media.release:
                            obj.import_session.add_importitem(media.release)
                        if media.artist:
                            obj.import_session.add_importitem(media.artist)
                    obj.save()

                    return
            except:
                pass


        if media:
            obj.results_tag = metadata
            obj.media = media
        else:
            pass

        obj.results_tag = metadata
        obj.status = ImportFile.STATUS_PROGRESS
        obj.results_tag_status = True
        obj.save()

        obj.results_acoustid = identifier.get_aid(obj.file)
        obj.results_acoustid_status = True
        obj.save()

        obj.results_musicbrainz = identifier.get_musicbrainz(obj)
        obj.results_discogs_status = True # TODO: ???
        obj.save()

        # requeue if no results yet
        if len(obj.results_musicbrainz) < 1:
            s = {
                'skip_tracknumber': True
            }
            obj.settings = s
            obj.save()
            obj.results_musicbrainz = identifier.get_musicbrainz(obj)
            obj.save()

        obj.status = ImportFile.STATUS_READY
        if media:
            obj.status = ImportFile.STATUS_DUPLICATE
            if obj.import_session:
                obj.import_session.add_importitem(obj)

        obj.results_tag_status = True
        obj.save()


    def do_import(self):

        log.debug('Start importing ImportFile: %s at %s' % (self.pk, self.file.path))

        if USE_CELERYD:
            self.import_task.delay(self)
        else:
            self.import_task(self)

    @task
    def import_task(obj):

        log.debug('Starting import task for:  %s' % (obj.pk))
        time.sleep(1)

        # to prevent circular import errors
        from util.importer_tools import Importer
        _importer = Importer(user=obj.import_session.user)

        media, status = _importer.run(obj)

        if media:
            obj.media = media
            obj.status = 1
        else:
            obj.status = 99

        log.info('Ending import task with status: %s for: %s' % (obj.status, obj.pk))

        obj.save()


    def save(self, skip_apply_import_tag=False, *args, **kwargs):

        msg = {'key': 'save', 'content': 'object saved'}

        if not self.filename:
            self.filename = self.file.name

        # check/update import_tag
        if self.status == ImportFile.STATUS_READY:
            from importer.util.importer_tools import Importer
            _importer = Importer(user=self.import_session.user)
            self.import_tag = _importer.complete_import_tag(self)

        if self.status == ImportFile.STATUS_READY:
            # try to apply import_tag to other files of this import session
            if not skip_apply_import_tag and self.import_session:
                # TODO: this breaks the interface, as nearly infinite loop arises
                #print 'skipping import_session.apply_import_tag'
                self.import_session.apply_import_tag(self)

        # check import_tag for completeness
        if self.status in [ImportFile.STATUS_READY, ImportFile.STATUS_WARNING]:
            media = self.import_tag.get('name', None)
            artist = self.import_tag.get('artist', None)
            release = self.import_tag.get('release', None)

            if media and artist and release:
                self.status = ImportFile.STATUS_READY
            else:
                self.status = ImportFile.STATUS_WARNING

        # lookup number of possible duplicates by name
        artist_name = self.import_tag.get('artist', None)
        if artist_name:
            num_artist_matches = Artist.objects.filter(name=artist_name).count()
        else:
            num_artist_matches = None
        self.import_tag['alibrary_artist_matches'] = num_artist_matches

        release_name = self.import_tag.get('release', None)
        if release_name:
            num_release_matches = Release.objects.filter(name=release_name).count()
        else:
            num_release_matches = None
        self.import_tag['alibrary_release_matches'] = num_release_matches

        super(ImportFile, self).save(*args, **kwargs)

@disable_for_loaddata
def post_save_importfile(sender, **kwargs):

    obj = kwargs['instance']

    # init: newly uploaded/created file. let's process (gather data) it
    # data then is presented in the import dialog, where the user can choose how to continue
    if obj.status == ImportFile.STATUS_INIT:
        obj.identify()

    # finalize the import, fired when user clicks on "start import"
    if obj.status == ImportFile.STATUS_QUEUED:
        obj.do_import()

post_save.connect(post_save_importfile, sender=ImportFile)

def post_delete_importfile(sender, **kwargs):
    obj = kwargs['instance']
    try:
        # only delete file if it is in regular `MEDIA_ROOT`
        # so "unsafe" files via `UnuspiciousStorage` are not affected
        if obj.file.path.startswith(MEDIA_ROOT):
            os.remove(obj.file.path)
    except:
        pass

post_delete.connect(post_delete_importfile, sender=ImportFile)



class ImportItem(BaseModel):

    """
    stores relations to objects created/assigned during the specific import
    """

    # limit to alibrary objects
    ct_limit = models.Q(app_label = 'alibrary', model = 'media') | \
    models.Q(app_label = 'alibrary', model = 'release') | \
    models.Q(app_label = 'alibrary', model = 'artist') | \
    models.Q(app_label = 'alibrary', model = 'label')

    import_session = models.ForeignKey(Import, verbose_name=_('Import'), null=True, related_name='importitem_set')

    content_type = models.ForeignKey(ContentType, limit_choices_to = ct_limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'importer'
        verbose_name = _('Import Item')
        verbose_name_plural = _('Import Items')

    def __unicode__(self):
        try:
            return '%s | %s' % (ContentType.objects.get_for_model(self.content_object), self.content_object.name)
        except:
            return '%s' % (self.pk)

    def save(self, *args, **kwargs):
        super(ImportItem, self).save(*args, **kwargs)


@receiver(post_save, sender=ImportItem)
def importitem_post_save(sender, instance, created, **kwargs):

    if created and instance.import_session and instance.import_session.user and instance.import_session.collection_name:
        importitem_created.send(
            sender=instance.__class__,
            content_object=instance.content_object,
            user=instance.import_session.user,
            collection_name=instance.import_session.collection_name
        )



@task
def reset_hanging_files(age=600):
    from datetime import datetime, timedelta
    for importfile in ImportFile.objects.filter(
            status__in=[ImportFile.STATUS_PROGRESS, ImportFile.STATUS_QUEUED],
            updated__lte=(datetime.now() - timedelta(seconds=age))
        ):
        log.info('releasing "working" lock for %s' % importfile.pk)
        importfile.status = 4
        importfile.save()
