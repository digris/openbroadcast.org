# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
import os
import sys
import time
import shutil
import uuid
import locale
import logging
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, UUIDField

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4

from importer.models import ImportFile
from importer.models import Import as ImportSession

log = logging.getLogger(__name__)

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

ALLOWED_EXTENSIONS = [
    '.mp3',
    '.m4a',
    '.flac',
]


STATUS_CHOICES = (
    (0, _('Init')),
    (1, _('Done')),
    (2, _('Ready')),
    (3, _('Progress')),
    (99, _('Error')),
    (11, _('Other')),
)


class BaseModel(models.Model):

    #uuid = UUIDField()
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    class Meta:
        abstract = True

class Massimport(BaseModel):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    directory = models.CharField(max_length=1024)
    uuid = models.UUIDField(default=uuid.uuid4)

    # importer relations
    # TODO: define

    class Meta:
        app_label = 'massimporter'
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ('-created', )


    def __unicode__(self):
        return self.directory

    @property
    def cache_directory(self):

        return os.path.join('massimporter', 'cache', '{}'.format(self.uuid))


    @property
    def abs_cache_directory(self):

        return os.path.join(MEDIA_ROOT, self.cache_directory)





    def scan_directory(self, reset=False):
        if not os.path.isdir(self.directory):
            raise IOError('directory "%s" does not exist' % self.directory)

        #log.debug('scanning directory: %s - reset: %s' % (self.directory, reset))
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                path = '{}'.format(os.path.join(root, file))
                rel_path = path.replace(self.directory, '')
                if os.path.isfile(path):
                    filename, ext = os.path.splitext(path)

                    """
                    first check by file extension
                    """
                    if ext in ALLOWED_EXTENSIONS:

                        """
                        extract metadata & check foreign relations
                        """
                        aps_path = os.path.join(self.directory, rel_path)
                        cache_path = os.path.join(self.abs_cache_directory, rel_path)
                        cache_dir = os.path.dirname(cache_path)

                        try:
                            if not os.path.isdir(cache_dir):
                                os.makedirs(cache_dir)
                        except OSError, e:
                            print e
                            pass # file exists
                        #else:

                        shutil.copyfile(aps_path, cache_path)

                        metadata, status = extract_metadata(path=aps_path)

                        importfile, created = MassimportFile.objects.get_or_create(path=rel_path, massimport=self)
                        #log.info('assigned file: %s - created: %s' % (importfile.path, created))

                    else:
                        log.debug('extension "%s" not allowed. (not %s)' % (ext, ', '.join(ALLOWED_EXTENSIONS)))

                else:
                    pass
                    #log.warning('file does not exists: %s' % path)


@receiver(post_save, sender=Massimport, dispatch_uid="massimport_post_save")
def massimport_post_save(sender, instance, created, **kwargs):

    print instance.cache_directory
    print instance.abs_cache_directory

    try:
        os.makedirs(instance.abs_cache_directory)
    except OSError, e:
        pass # file exists





class MassimportFile(BaseModel):

    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    massimport = models.ForeignKey(Massimport, related_name='files')
    import_file = models.ForeignKey(ImportFile, null=True)
    path = models.CharField(max_length=1024)
    uuid = models.UUIDField(default=uuid.uuid4)

    # importer relations
    # TODO: define

    class Meta:
        app_label = 'massimporter'
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        ordering = ('-created', )


    def __unicode__(self):
        return self.path

    @property
    def abs_path(self):
        return os.path.join(self.massimport.directory, self.path)

    @property
    def cache_path(self):
        return os.path.join(self.massimport.abs_cache_directory, self.path)



@receiver(post_save, sender=MassimportFile, dispatch_uid="massimport_file_post_save")
def massimport_file_post_save(sender, instance, created, **kwargs):

    if created:
        print 'link to importfile'

        import_session, c = ImportSession.objects.get_or_create(user=instance.massimport.user,
                                                             type=ImportSession.TYPE_API,
                                                             uuid_key=instance.massimport.uuid)

        import_file = ImportFile(file=instance.cache_path,
                                 import_session=import_session)


        import_file.save()

        instance.import_file = import_file
        instance.save()


"""
TODO: maybe place in own module...
"""
def extract_metadata(path):




    enc = locale.getpreferredencoding()


    meta = None
    ext = os.path.splitext(path)[1]
    log.debug('detected %s as extension' % ext)

    if ext:
        ext = ext.lower()

    if ext == '.mp3':
        try:
            meta = EasyID3(path)
        except Exception, e:
            log.debug('unable to process MP3')

    if ext in ['.mp4', '.m4a']:
        try:
            meta = EasyMP4(path)
        except Exception, e:
            log.debug('unable to process M4A')


    if not meta:
        try:
            meta = MutagenFile(path)
            log.debug('using MutagenFile')
        except Exception, e:
            log.warning('even unable to open file with straight mutagen: %s' % e)


    #print meta

    return 1, 1
