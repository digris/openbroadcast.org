#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import shutil
import logging

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.files import File as DjangoFile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from celery.task import task

from util.process import Process
from lib.util.filename import safe_name
from pushy.util import pushy_custom


log = logging.getLogger(__name__)

USE_CELERYD = True

GENERIC_STATUS_CHOICES = (
    (0, _('Init')),
    (1, _('Done')),
    (2, _('Ready')), # a.k.a. 'queued'
    (3, _('Progress')),
    (4, _('Downloaded')),
    (99, _('Error')),
    (11, _('Other')),
)



# extra fields
from django_extensions.db.fields import *

from settings import PROJECT_DIR


def create_download_path(instance, filename):
    import unicodedata
    import string

    filename, extension = os.path.splitext(filename)
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    folder = "export/processed/%s-%s/" % (time.strftime("%Y%m%d%H%M%S", time.gmtime()), instance.uuid)
    return os.path.join(folder, "%s%s" % (cleaned_filename.lower(), extension.lower()))


def create_export_path():
    import unicodedata
    import string

    filename, extension = os.path.splitext(filename)
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
    folder = "export/%s/" % time.strftime("%Y%m%d%H%M%S", time.gmtime())
    return os.path.join(folder, "%s%s" % (cleaned_filename.lower(), extension.lower()))


def create_archive_dir(instance):

    path = "export/cache/%s-%s/" % (time.strftime("%Y%m%d%H%M%S", time.gmtime()), instance.uuid)
    #path = "export/cache/%s/" % ('DEBUG')

    path_full = os.path.join(PROJECT_DIR, 'media', path)

    # debug - set to persistent directory for easier testing:
    # path_full = os.path.join(PROJECT_DIR, 'media' , 'export/debug/')

    try:
        os.makedirs(os.path.join(path_full, 'cache/'))
    except OSError, e:
        pass # file exists

    print 'archive dir: %s' % path_full

    return path_full


class BaseModel(models.Model):
    created = CreationDateTimeField()
    updated = ModificationDateTimeField()

    uuid = UUIDField()

    class Meta:
        abstract = True


class Export(BaseModel):
    FORMAT_CHOICES = (
        ('mp3', _('MP3')),
        ('flac', _('Flac')),
    )

    class Meta:
        app_label = 'exporter'
        verbose_name = _('Export')
        verbose_name_plural = _('Exports')
        ordering = ('created', )

    user = models.ForeignKey(User, blank=True, null=True, related_name="exports", on_delete=models.SET_NULL)
    status = models.PositiveIntegerField(default=0, choices=GENERIC_STATUS_CHOICES)

    status_msg = models.CharField(max_length=512, blank=True, null=True)

    filesize = models.IntegerField(default=0, blank=True, null=True)

    filename = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(upload_to=create_download_path, blank=True, null=True)
    fileformat = models.CharField(max_length=4, default='mp3', choices=FORMAT_CHOICES)

    token = models.CharField(max_length=256, blank=True, null=True)

    downloaded = models.DateTimeField(blank=True, null=True)

    TYPE_CHOICES = (
        ('web', _('Web Interface')),
        ('api', _('API')),
        ('fs', _('Filesystem')),
    )
    type = models.CharField(max_length="10", default='web', choices=TYPE_CHOICES)
    notes = models.TextField(blank=True, null=True,
                             help_text=_('Optionally, just add some notes to this export if desired.'))


    def __unicode__(self):
        return "%s - %s" % (self.user, self.created)

    @models.permalink
    def get_absolute_url(self):
        return ('exporter-export-update', [str(self.pk)])

    @models.permalink
    def get_delete_url(self):
        return ('exporter-export-delete', [str(self.pk)])


    @models.permalink
    def get_download_url(self):

        return ('exporter-export-download', (), {'uuid': self.uuid, 'token': self.token})
        #return ('exporter-export-download', [self.uuid])

    def get_api_url(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'export', 'api_name': 'v1'})
        return '%s%s/' % (url, self.pk)



    #@models.permalink
    def get_delete_url(self):
        #return ('exporter-upload-delete', [str(self.pk)])
        return ''

    def set_downloaded(self):
        self.downloaded = datetime.datetime.now()
        self.status = 4
        self.save()

        return None


    def process(self):
        log = logging.getLogger('exporter.models.process')
        log.info('Start process Export: %s' % (self.pk))

        if USE_CELERYD:
            self.process_task.delay(self)
        else:
            self.process_task(self)

    @task
    def process_task(obj):

        target = 'download'

        from atracker.util import create_event

        process = Process()
        status, result, messages = process.run(instance=obj, format=obj.fileformat)

        if target == 'download':

            if result:

                obj.filesize = os.path.getsize(result)
                obj.file = DjangoFile(open(result), u'archive')

                # update status
                obj.status = 1
                obj.save()
                process.clear_cache()
            else:
                obj.status = 99
                obj.status_msg = messages
                obj.save()
                process.clear_cache()



    def save(self, *args, **kwargs):

        self.filename = generate_export_filename(self.export_items)

        if not self.token:
            self.token = sha_constructor('TX%s' % self.uuid).hexdigest()

        super(Export, self).save(*args, **kwargs)


def post_save_export(sender, **kwargs):
    obj = kwargs['instance']

    # if status is 'ready' > run exporter
    if obj.status == 2:
        obj.process()

    # emmit update message via pushy
    if kwargs['created']:
        if obj.user and obj.user.profile:
            pushy_custom(obj.user.profile.uuid)

    obj.export_items.update(status=1)


post_save.connect(post_save_export, sender=Export)


def post_delete_export(sender, **kwargs):
    obj = kwargs['instance']

    if obj.file:
        log.debug('Post delete action, remove file: %s' % obj.file.path)

        directory = os.path.split(obj.file.path)[0]
        try:
            shutil.rmtree(directory, True)
        except:
            obj.file.delete(False)




post_delete.connect(post_delete_export, sender=Export)


def generate_export_filename(qs):
    filename = _('initializing export')
    if qs.count() == 1:
        item = qs.all()[0]
        if item.content_type.name.lower() == 'release':
            filename = item.content_object.name.encode('ascii', 'ignore')
        if item.content_type.name.lower() == 'track':
            filename = item.content_object.name.encode('ascii', 'ignore')

    if qs.count() > 1:
        filename = _('Multiple items')

    return filename


class ExportItem(BaseModel):
    class Meta:
        app_label = 'exporter'
        verbose_name = _('Export Item')
        verbose_name_plural = _('Export Items')
        ordering = ('-created', )

    #filename = models.CharField(max_length=256, blank=True, null=True)
    #file = models.FileField(upload_to=create_download_path, blank=True, null=True)

    export_session = models.ForeignKey(Export, verbose_name=_('Export'), null=True, related_name='export_items')
    status = models.PositiveIntegerField(default=0, choices=GENERIC_STATUS_CHOICES)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    def __unicode__(self):
        try:
            return '%s - %s' % (self.content_object, self.get_status_display())
        except:
            return '%s - %s' % (self.pk, self.status)

    #@models.permalink
    def get_delete_url(self):
        #return ('exporter-upload-delete', [str(self.pk)])
        return ''


    def process(self):
        log = logging.getLogger('exporter.models.process')
        log.info('Start processing ExportItem: %s' % (self.pk))
        log.info('Path: %s' % (self.file.path))

        if USE_CELERYD:
            self.process_task.delay(self)
        else:
            self.process_task(self)

    @task
    def process_task(obj):
        pass


    def save(self, *args, **kwargs):

        #if not self.filename:
        #    self.filename = self.file.name

        super(ExportItem, self).save(*args, **kwargs)


def post_save_exportitem(sender, **kwargs):
    obj = kwargs['instance']

    """
    if obj.status == 0:
        obj.process()
    """

#post_save.connect(post_save_exportitem, sender=ExportItem)      

def post_delete_exportitem(sender, **kwargs):
    #import shutil
    obj = kwargs['instance']
    try:
        os.remove(obj.file.path)
    except:
        pass

#post_delete.connect(post_delete_exportitem, sender=ExportItem)



"""
maintenance tasks
(called via celerybeat, or management command)
"""

@task
def cleanup_exports():
    es = Export.objects.filter(created__lte=datetime.datetime.now() - datetime.timedelta(days=2))
    es.delete()

        