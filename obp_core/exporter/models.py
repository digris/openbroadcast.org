import os
import time
import hashlib
import datetime
import shutil
import logging
import unicodedata

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.files import File as DjangoFile
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.urlresolvers import reverse
from django.conf import settings
from celery import shared_task
from .util.process import Process

from base.mixins import TimestampedModelMixin, UUIDModelMixin


log = logging.getLogger(__name__)

BASE_DIR = getattr(settings, "BASE_DIR", None)
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)
USE_CELERYD = getattr(settings, "EXPORTER_USE_CELERYD", False)

GENERIC_STATUS_CHOICES = (
    (0, "Init"),
    (1, "Done"),
    (2, "Ready"),  # a.k.a. 'queued'
    (3, "Progress"),
    (4, "Downloaded"),
    (99, "Error"),
    (11, "Other"),
)


def create_download_path(instance, filename):
    filename, extension = os.path.splitext(filename)
    cleaned_filename = unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore")
    folder = "export/processed/{}-{}/".format(
        time.strftime("%Y%m%d%H%M%S", time.gmtime()),
        instance.uuid,
    )
    return os.path.join(folder, f"{cleaned_filename.lower()}{extension.lower()}")


def create_archive_dir(instance):

    path = "export/cache/{}-{}/".format(
        time.strftime("%Y%m%d%H%M%S", time.gmtime()),
        instance.uuid,
    )

    path_full = os.path.join(MEDIA_ROOT, path)

    # debug - set to persistent directory for easier testing:
    # path_full = os.path.join(BASE_DIR, 'media' , 'export/debug/')

    try:
        os.makedirs(os.path.join(path_full, "cache/"))
    except OSError:
        pass  # file exists

    return path_full


class Export(UUIDModelMixin, TimestampedModelMixin, models.Model):
    FORMAT_CHOICES = (("mp3", "MP3"), ("flac", "Flac"))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="exports",
        on_delete=models.SET_NULL,
    )
    status = models.PositiveIntegerField(default=0, choices=GENERIC_STATUS_CHOICES)

    status_msg = models.CharField(max_length=512, blank=True, null=True)

    filesize = models.IntegerField(default=0, blank=True, null=True)

    filename = models.CharField(max_length=256, blank=True, null=True)
    file = models.FileField(upload_to=create_download_path, blank=True, null=True)
    fileformat = models.CharField(max_length=4, default="mp3", choices=FORMAT_CHOICES)

    token = models.CharField(max_length=256, blank=True, null=True)

    downloaded = models.DateTimeField(blank=True, null=True)

    TYPE_CHOICES = (
        ("web", "Web Interface"),
        ("api", "API"),
        ("fs", "Filesystem"),
    )
    type = models.CharField(max_length=10, default="web", choices=TYPE_CHOICES)
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optionally, just add some notes to this export if desired.",
    )

    class Meta:
        app_label = "exporter"
        verbose_name = "Export"
        verbose_name_plural = "Exports"
        ordering = ("created",)

    def __str__(self):
        return f"{self.user} - {self.created}"

    def get_ct(self):
        return f"{self._meta.app_label}.{self.__class__.__name__}".lower()

    def get_absolute_url(self):
        return None

    def get_delete_url(self):
        return "#"

    @models.permalink
    def get_download_url(self):
        return (
            "exporter:export-download",
            (),
            {"uuid": self.uuid, "token": self.token},
        )

    def get_api_url(self):
        url = reverse(
            "api_dispatch_list", kwargs={"resource_name": "export", "api_name": "v1"}
        )
        return f"{url}{self.pk}/"

    def set_downloaded(self):
        self.downloaded = datetime.datetime.now()
        self.status = 4
        self.save()

        return None

    def process(self):
        log = logging.getLogger("exporter.models.process")
        log.info("Start process Export: %s", self.pk)

        if USE_CELERYD:
            self.process_task.delay(self)
        else:
            self.process_task(self)

    @shared_task
    def process_task(obj):

        target = "download"

        process = Process()
        status, result, messages = process.run(instance=obj, format=obj.fileformat)

        if target == "download":
            if result:
                obj.filesize = os.path.getsize(result)
                with open(result, "rb") as result_file:
                    obj.file = DjangoFile(result_file, "archive")

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
            # self.token = hashlib.sha1("TX%s" % self.uuid).hexdigest()
            self.token = hashlib.sha1(f"TX{self.uuid}".encode()).hexdigest()

        super().save(*args, **kwargs)


def post_save_export(sender, **kwargs):
    obj = kwargs["instance"]

    # if status is 'ready' > run exporter
    if obj.status == 2:
        obj.process()

    # emmit update message via pushy
    if kwargs["created"] and obj.user and obj.user.profile:
        from pushy.util import pushy_custom

        pushy_custom(str(obj.user.profile.uuid))

    obj.export_items.update(status=1)


post_save.connect(post_save_export, sender=Export)


def post_delete_export(sender, **kwargs):
    obj = kwargs["instance"]

    if obj.file:
        log.debug("Post delete action, remove file: %s", obj.file.path)

        directory = os.path.split(obj.file.path)[0]
        try:
            shutil.rmtree(directory, True)
        except BaseException:
            obj.file.delete(False)


post_delete.connect(post_delete_export, sender=Export)


def generate_export_filename(qs):
    filename = "initializing export"
    if qs.count() == 1:
        item = qs.all()[0]
        if item.content_type.name.lower() == "release":
            filename = item.content_object.name.encode("ascii", "ignore")
        if item.content_type.name.lower() == "track":
            filename = item.content_object.name.encode("ascii", "ignore")
        if item.content_type.name.lower() == "playlist":
            filename = item.content_object.name.encode("ascii", "ignore")

    if qs.count() > 1:
        filename = "Multiple items"

    return filename


class ExportItem(UUIDModelMixin, TimestampedModelMixin, models.Model):
    class Meta:
        app_label = "exporter"
        verbose_name = "Export Item"
        verbose_name_plural = "Export Items"
        ordering = ("-created",)

    export_session = models.ForeignKey(
        Export, verbose_name="Export", null=True, related_name="export_items"
    )
    status = models.PositiveIntegerField(default=0, choices=GENERIC_STATUS_CHOICES)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        try:
            return f"{self.content_object} - {self.get_status_display()}"
        except BaseException:
            return f"{self.pk} - {self.status}"

    # @models.permalink
    def get_delete_url(self):
        # return ('exporter-upload-delete', [str(self.pk)])
        return ""

    def process(self):
        log = logging.getLogger("exporter.models.process")
        log.info("Start processing ExportItem: %s", self.pk)
        log.info("Path: %s", self.file.path)

        if USE_CELERYD:
            self.process_task.delay(self)
        else:
            self.process_task(self)

    @shared_task
    def process_task(obj):
        pass


@shared_task
def cleanup_exports():
    qs = Export.objects.filter(
        created__lte=datetime.datetime.now() - datetime.timedelta(days=7)
    )
    qs.delete()
