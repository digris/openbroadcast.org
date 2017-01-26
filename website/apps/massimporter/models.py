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


class BaseModel(models.Model):

    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    class Meta:
        abstract = True

class Massimport(BaseModel):


    STATUS_INIT = 0
    STATUS_DONE = 1
    STATUS_QUEUED = 2
    STATUS_ERROR = 99
    STATUS_CHOICES = (
        (STATUS_INIT, _(u'Init')),
        (STATUS_DONE, _(u'Done')),
        (STATUS_QUEUED, _(u'Queued')),
        (STATUS_ERROR, _(u'Error')),
    )

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.PositiveIntegerField(default=STATUS_INIT, choices=STATUS_CHOICES)
    directory = models.CharField(max_length=1024)
    uuid = models.UUIDField(default=uuid.uuid4)

    collection_name = models.CharField(
        max_length=250,
        blank=True, null=True
    )

    class Meta:
        app_label = 'massimporter'
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')
        ordering = ('-created', )


    def __unicode__(self):
        return '{} - {}'.format(self.pk, self.directory)

    @property
    def cache_directory(self):
        return os.path.join('massimporter', 'cache', '{}'.format(self.uuid))


    @property
    def abs_cache_directory(self):
        return os.path.join(MEDIA_ROOT, self.cache_directory)

    @property
    def import_session(self):

        import_session, c = ImportSession.objects.get_or_create(
            user=self.user,
            type=ImportSession.TYPE_API,
            uuid_key=self.uuid,
            collection_name=self.collection_name
        )

        return import_session


    def update(self):

        for item in self.files.all():
            item.update()

        if self.files.count() > 0 and self.files.filter(status=ImportFile.STATUS_INIT).count() == 0:
            self.status = Massimport.STATUS_DONE
            self.save()

    def scan(self):

        stats = {
            'added': 0,
            'ignored': 0,
            'missing': 0,
        }

        if not os.path.isdir(self.directory):
            raise IOError('directory "%s" does not exist' % self.directory)

        print('scanning {}'.format(self.directory))

        for root, dirs, files in os.walk(self.directory):

            for file in files:

                try:

                    path = os.path.join(root.decode('utf-8'), file.decode('utf-8'))

                    rel_path = path.replace(self.directory, '')

                    if os.path.isfile(path):



                        filename, ext = os.path.splitext(path)
                        if ext in ALLOWED_EXTENSIONS:
                            MassimportFile.objects.get_or_create(
                                path=rel_path, massimport=self
                            )

                            stats['added'] += 1



                        else:
                            print(' - {}'.format(rel_path))
                            stats['ignored'] += 1

                    else:
                        print(' ! {}'.format(rel_path))
                        stats['missing'] += 1

                except Exception as e:
                    print('{}'.format(e))
                    stats['missing'] += 1


        print('----------------------------------------------------------')
        print('ID: {}'.format(self.pk))
        print('----------------------------------------------------------')
        print('Files added:      {}'.format(stats['added']))
        print('Files ignored:    {}'.format(stats['ignored']))
        print('Files unreadable: {}'.format(stats['missing']))


        self.status = Massimport.STATUS_QUEUED
        self.save()


@receiver(post_save, sender=Massimport, dispatch_uid="massimport_post_save")
def massimport_post_save(sender, instance, created, **kwargs):


    ImportSession.objects.filter(pk=instance.import_session.pk).update(
        notes='Massimport ID: {} - Files: {}'.format(
            instance.id,
            instance.files.count()
        )
    )

    try:
        os.makedirs(instance.abs_cache_directory)
    except OSError as e:
        pass


class MassimportFile(BaseModel):

    # TODO: a bit hackish - linked states to ImportFile model$

    STATUS_CHOICES = ImportFile.STATUS_CHOICES

    status = models.PositiveIntegerField(default=ImportFile.STATUS_INIT, choices=STATUS_CHOICES)
    massimport = models.ForeignKey(Massimport, related_name='files')
    import_file = models.ForeignKey(ImportFile, null=True)
    path = models.CharField(max_length=1024)
    uuid = models.UUIDField(default=uuid.uuid4)

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


    def update(self):

        if self.import_file:

            # if self.status != self.import_file.status:
            #     print 'update status from {} to {} for {}'.format(
            #         self.get_status_display(),
            #         self.import_file.get_status_display(),
            #         self.path
            #     )

            self.status = self.import_file.status


        else:
            self.status = ImportFile.STATUS_INIT

        self.save()



    def enqueue(self):

        if not self.import_file:
            import_file = ImportFile(
                    #file=self.cache_path,
                    file=self.abs_path,
                    import_session=self.massimport.import_session
                )

            import_file.save()

            self.import_file = import_file
            self.save()



