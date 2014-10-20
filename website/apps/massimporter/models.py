#-*- coding: utf-8 -*-
import os
import sys
import time
import locale
import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, UUIDField

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4

log = logging.getLogger(__name__)

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

    uuid = UUIDField()
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    class Meta:
        abstract = True

class Massimport(BaseModel):

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    directory = models.CharField(max_length=512)

    # importer relations
    # TODO: define

    class Meta:
        app_label = 'massimporter'
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ('-created', )


    def __unicode__(self):
        return self.directory


    def scan_directory(self, reset=False):

        if not os.path.isdir(self.directory):
            raise IOError('directory "%s" does not exist' % self.directory)

        log.debug('scanning directory: %s - reset: %s' % (self.directory, reset))
        for root, dirs, files in os.walk(self.directory):

            for file in files:

                path = os.path.join(root, file)
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

                        metadata, status = extract_metadata(path=os.path.join(self.directory, rel_path))


                        importfile, created = MassimportFile.objects.get_or_create(path=rel_path, massimport=self)
                        log.info('assigned file: %s - created: %s' % (importfile.path, created))

                    else:

                        log.debug('extension "%s" not allowed. (not %s)' % (ext, ', '.join(ALLOWED_EXTENSIONS)))


                else:
                    log.warning('file does not exists: %s' % path)




class MassimportFile(BaseModel):

    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    massimport = models.ForeignKey(Massimport, related_name='files')
    path = models.CharField(max_length=512)

    # importer relations
    # TODO: define


    class Meta:
        app_label = 'massimporter'
        verbose_name = _('File')
        verbose_name_plural = _('Files')
        ordering = ('-created', )


    def __unicode__(self):
        return self.path



"""
TODO: maybe place in own module...
"""
def extract_metadata(path):
    print '*** extract_metadata ***'
    print 'path: %s' % path


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

    print '////////// META ////////////////////'
    print meta

    return 1, 1
