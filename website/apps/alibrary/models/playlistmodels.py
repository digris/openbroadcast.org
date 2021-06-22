# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid

import arating
import tagging
from alibrary import settings as alibrary_settings
from alibrary.models import MigrationMixin, Daypart
from alibrary.util.storage import get_dir_for_object, OverwriteStorage
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.fields.json import JSONField
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from base.fields import extra
from tagging.registry import register as tagging_register

from base.mixins import TimestampedModelMixin

from ..util.mixdown_client import MixdownAPIClient


try:
    from urllib.request import urlopen  # for python 3.0 and later
except ImportError:
    from urllib2 import urlopen  # fall back to python 2's urllib2

log = logging.getLogger(__name__)

DURATION_MAX_DIFF = 2500  # in ms


# TODO: remove. still referenced in migrations, so left here for the moment
def filename_by_uuid(instance, filename):
    filename, extension = os.path.splitext(filename)
    path = "playlists/"
    filename = str(instance.uuid).replace("-", "/") + extension
    return os.path.join(path, filename)


def upload_image_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(
        get_dir_for_object(instance), "playlists{}".format(extension.lower())
    )


def upload_mixdown_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(
        get_dir_for_object(instance), "mixdown{}".format(extension.lower())
    )


@python_2_unicode_compatible
class Season(models.Model):
    name = models.CharField(max_length=200)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    class Meta:
        app_label = "alibrary"
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
        ordering = ("-name",)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class Weather(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        app_label = "alibrary"
        verbose_name = _("Weather")
        verbose_name_plural = _("Weather")
        ordering = ("-name",)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class Series(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from="name", editable=True, blank=True, overwrite=True
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    description = extra.MarkdownTextField(blank=True, null=True)

    class Meta:
        app_label = "alibrary"
        verbose_name = _("Series")
        verbose_name_plural = _("Series")
        ordering = ("-name",)

    def __str__(self):
        return "{}".format(self.name)

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()


@python_2_unicode_compatible
class Playlist(MigrationMixin, TimestampedModelMixin, models.Model):

    TYPE_BASKET = "basket"
    TYPE_PLAYLIST = "playlist"
    TYPE_BROADCAST = "broadcast"
    TYPE_OTHER = "other"

    TYPE_CHOICES = (
        (TYPE_BASKET, _("Private Playlist")),
        (TYPE_PLAYLIST, _("Public Playlist")),
        (TYPE_BROADCAST, _("Broadcast")),
        (TYPE_OTHER, _("Other")),
    )

    name = models.CharField(
        max_length=200,
    )
    slug = AutoSlugField(
        populate_from="name",
        editable=True,
        blank=True,
        overwrite=True,
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    status = models.PositiveIntegerField(
        default=0,
        choices=alibrary_settings.PLAYLIST_STATUS_CHOICES,
    )
    type = models.CharField(
        max_length=12,
        default="basket",
        null=True,
        choices=TYPE_CHOICES,
    )
    broadcast_status = models.PositiveIntegerField(
        default=0,
        choices=alibrary_settings.PLAYLIST_BROADCAST_STATUS_CHOICES,
    )
    broadcast_status_messages = JSONField(
        blank=True,
        null=True,
        default=None,
    )

    playout_mode_random = models.BooleanField(
        verbose_name=_("Shuffle Playlist"),
        default=False,
        help_text=_(
            "If enabled the order of the tracks will be randomized for playout"
        ),
    )

    rotation = models.BooleanField(
        default=True,
    )
    rotation_date_start = models.DateField(
        verbose_name=_("Rotate from"),
        blank=True,
        null=True,
    )
    rotation_date_end = models.DateField(
        verbose_name=_("Rotate until"),
        blank=True,
        null=True,
    )

    main_image = models.ImageField(
        verbose_name=_("Image"),
        upload_to=upload_image_to,
        storage=OverwriteStorage(),
        null=True,
        blank=True,
    )

    # relations
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        default=None,
        related_name="playlists",
    )
    items = models.ManyToManyField(
        "PlaylistItem",
        through="PlaylistItemPlaylist",
        blank=True,
    )

    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(
        max_length=1024,
        verbose_name="Tags",
        blank=True,
        null=True,
    )

    # updated/calculated on save
    duration = models.IntegerField(
        null=True,
        default=0,
    )

    target_duration = models.PositiveIntegerField(
        default=0,
        null=True,
        choices=alibrary_settings.PLAYLIST_TARGET_DURATION_CHOICES,
    )

    dayparts = models.ManyToManyField(
        Daypart,
        blank=True,
        related_name="daypart_plalists",
    )
    seasons = models.ManyToManyField(
        "Season",
        blank=True,
        related_name="season_plalists",
    )
    weather = models.ManyToManyField(
        "Weather",
        blank=True,
        related_name="weather_plalists",
    )

    # series
    series = models.ForeignKey(
        Series,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    series_number = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    # is currently selected as default?
    is_current = models.BooleanField(
        _("Currently selected?"),
        default=False,
    )

    description = extra.MarkdownTextField(
        blank=True,
        null=True,
    )

    mixdown_file = models.FileField(
        null=True,
        blank=True,
        upload_to=upload_mixdown_to,
    )

    emissions = GenericRelation("abcast.Emission")

    # meta
    class Meta:
        app_label = "alibrary"
        verbose_name = _("Playlist")
        verbose_name_plural = _("Playlists")
        ordering = ("-updated",)

        permissions = (
            ("view_playlist", "View Playlist"),
            ("edit_playlist", "Edit Playlist"),
            ("schedule_playlist", "Schedule Playlist"),
            ("admin_playlist", "Edit Playlist (extended)"),
        )

    def __str__(self):
        return self.name

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()

    def get_absolute_url(self):
        return reverse("alibrary-playlist-detail", kwargs={"uuid": self.uuid})

    def get_edit_url(self):
        return reverse("alibrary-playlist-edit", kwargs={"uuid": self.uuid})

    def get_delete_url(self):
        return reverse("alibrary-playlist-delete", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:alibrary_playlist_change", args=(self.pk,))

    def get_duration(self):
        duration = 0
        try:
            for item in self.items.all():
                duration += item.content_object.get_duration()
                pip = PlaylistItemPlaylist.objects.get(playlist=self, item=item)
                duration -= pip.cue_in
                duration -= pip.cue_out
                duration -= pip.fade_cross
        except:
            pass

        return duration

    # TODO: remove usages and use generic reverse 'emissions' instead
    def get_emissions(self):
        from abcast.models import Emission

        ctype = ContentType.objects.get_for_model(self)
        emissions = Emission.objects.filter(
            content_type__pk=ctype.id, object_id=self.id
        ).order_by("-time_start")
        return emissions

    def get_api_url(self):
        return (
            reverse(
                "api_dispatch_detail",
                kwargs={
                    "api_name": "v1",
                    "resource_name": "library/playlist",
                    "pk": self.pk,
                },
            )
            + ""
        )

    def get_api_simple_url(self):
        return (
            reverse(
                "api_dispatch_detail",
                kwargs={
                    "api_name": "v1",
                    "resource_name": "library/simpleplaylist",
                    "pk": self.pk,
                },
            )
            + ""
        )

    def can_be_deleted(self):

        can_delete = False
        reason = _("This playlist cannot be deleted.")

        if self.type == "basket":
            can_delete = True
            reason = None

        if self.type == "playlist":
            can_delete = False
            reason = _(
                'Playlist "%s" is public. It cannot be deleted anymore.' % self.name
            )

        if self.type == "broadcast":
            can_delete = False
            reason = _(
                'Playlist "%s" published for broadcast. It cannot be deleted anymore.'
                % self.name
            )

        return can_delete, reason

    def get_transform_status(self, target_type):
        """
        check if transformation is possible /
        what needs to be done
        Not so nicely here - but...
        """

        status = False

        """
        criterias = [
            {
                'key': 'tags',
                'name': _('Tags'),
                'status': True,
                'warning': _('Please add some tags'),
            },
            {
                'key': 'description',
                'name': _('Description'),
                'status': False,
                'warning': _('Please add a description'),
            }
        ]
        """

        criterias = []

        # "basket" only used while dev...
        if target_type == "basket":
            status = True

        if target_type == "playlist":
            status = True
            # tags
            tag_count = self.tags.count()
            if tag_count < 1:
                status = False
            criteria = {
                "key": "tags",
                "name": _("Tags"),
                "status": tag_count > 0,
                "warning": _("Please add some tags"),
            }
            criterias.append(criteria)
            # scheduled
            if self.type == "broadcast":
                schedule_count = self.get_emissions().count()
                if schedule_count > 0:
                    status = False
                criteria = {
                    "key": "scheduled",
                    "name": _("Playlist already scheduled")
                    if schedule_count > 0
                    else _("Playlist not scheduled"),
                    "status": schedule_count < 1,
                    "warning": _(
                        'This playlist has already ben scheduled %s times. Remove all scheduler entries to "un-broadcast" this playlist.'
                        % schedule_count
                    ),
                }
                if schedule_count > 0:
                    criterias.append(criteria)

        if target_type == "broadcast":
            status = True
            # tags
            tag_count = self.tags.count()
            if tag_count < 1:
                status = False
            criteria = {
                "key": "tags",
                "name": _("Tags"),
                "status": tag_count > 0,
                "warning": _("Please add some tags"),
            }
            criterias.append(criteria)

            # dayparts
            dp_count = self.dayparts.count()
            if not dp_count:
                status = False
            criteria = {
                "key": "dayparts",
                "name": _("Dayparts"),
                "status": dp_count > 0,
                "warning": _("Please specify the dayparts"),
            }
            criterias.append(criteria)

            # duration
            if not self.broadcast_status == 1:
                status = False
            criteria = {
                "key": "duration",
                "name": _("Duration"),
                "status": True if self.broadcast_status == 1 else False,
                "warning": _("Durations do not match"),
                # 'warning': ', '.join(self.broadcast_status_messages),
            }
            criterias.append(criteria)

        transformation = {"criterias": criterias, "status": status}

        return transformation

    ###################################################################
    # legacy version - used in tastypie API (v1)
    ###################################################################
    def add_items_by_ids(self, ids, ct, timing=None):

        from alibrary.models.mediamodels import Media

        log.debug("add media to playlist: {}".format(", ".join(ids)))

        for id in ids:
            id = int(id)

            co = None

            if ct == "media":
                co = Media.objects.get(pk=id)

            if co:

                i = PlaylistItem(content_object=co)
                i.save()
                """
                ctype = ContentType.objects.get_for_model(co)
                item, created = PlaylistItem.objects.get_or_create(object_id=co.pk, content_type=ctype)
                """

                pi, created = PlaylistItemPlaylist.objects.get_or_create(
                    item=i, playlist=self, position=self.items.count()
                )

                if timing:
                    try:
                        pi.fade_in = timing["fade_in"]
                        pi.fade_out = timing["fade_out"]
                        pi.cue_in = timing["cue_in"]
                        pi.cue_out = timing["cue_out"]
                        pi.save()
                    except:
                        pass

        self.save()

    ###################################################################
    # new version - used in DRF API (v245)
    ###################################################################
    def add_item(self, item, cue_and_fade=None, commit=True):

        log.debug("add item to playlist: {}".format(item))

        playlist_item = PlaylistItem(content_object=item)
        playlist_item.save()

        playlist_item_playlist = PlaylistItemPlaylist(
            item=playlist_item, playlist=self, position=self.items.count()
        )

        if cue_and_fade:
            playlist_item_playlist.fade_in = cue_and_fade["fade_in"]
            playlist_item_playlist.fade_out = cue_and_fade["fade_out"]
            playlist_item_playlist.cue_in = cue_and_fade["cue_in"]
            playlist_item_playlist.cue_out = cue_and_fade["cue_out"]

        playlist_item_playlist.save()

        if commit:
            self.save()

    def reorder_items_by_uuids(self, uuids):

        i = 0

        for uuid in uuids:
            pi = PlaylistItemPlaylist.objects.get(uuid=uuid)
            pi.position = i
            pi.save()

            i += 1

        self.save()

    def convert_to(self, playlist_type):

        log.debug(
            'requested to convert "%s" from %s to %s'
            % (self.name, self.type, playlist_type)
        )

        if playlist_type == "broadcast":
            self.broadcast_status, self.broadcast_status_messages = self.self_check()

        transformation = self.get_transform_status(playlist_type)
        status = transformation["status"]

        if playlist_type == "broadcast" and status:
            _status, messages = self.self_check()
            if _status == 1:
                status = True

        if status:
            self.type = playlist_type
            self.created = timezone.now()
            self.save()

        return self, status

    def get_items(self):

        pis = PlaylistItemPlaylist.objects.filter(playlist=self).order_by("position")

        items = []
        for pi in pis:
            item = pi.item
            item.cue_in = pi.cue_in
            item.cue_out = pi.cue_out
            item.fade_in = pi.fade_in
            item.fade_out = pi.fade_out
            item.fade_cross = pi.fade_cross
            # get the actual playout duration
            try:
                # print '// getting duration for:'
                # print '%s - %s' % (item.content_object.pk, item.content_object.name)
                # print 'obj duration: %s' % item.content_object.duration_s
                item.playout_duration = (
                    item.content_object.duration_ms
                    - item.cue_in
                    - item.cue_out
                    - item.fade_cross
                )
            except Exception as e:
                log.warning("unable to get duration: {}".format(e))
                item.playout_duration = 0

            items.append(item)
        return items

    def self_check(self):
        """
        check if everything is fine to be 'scheduled'
        """

        log.info("Self check requested for: %s" % self.name)

        status = 1  # set to 'OK'
        messages = []

        # return status, messages

        try:
            # check ready-status of related media
            for item in self.items.all():
                # log.debug('Self check content object: %s' % item.content_object)
                # log.debug('Self check master: %s' % item.content_object.master)
                # log.debug('Self check path: %s' % item.content_object.master.path)

                # check if file available
                try:
                    with open(item.content_object.master.path):
                        pass
                except IOError as e:
                    log.warning(
                        _("File does not exists: %s | %s")
                        % (e, item.content_object.master.path)
                    )
                    status = 99
                    messages.append(
                        _("File does not exists: %s | %s")
                        % (e, item.content_object.master.path)
                    )

                """
                pip = PlaylistItemPlaylist.objects.get(playlist=self, item=item)
                duration -= pip.cue_in
                duration -= pip.cue_out
                duration -= pip.fade_cross
                """

            # check duration & matching target_duration
            """
            compare durations. target: in seconds | calculated duration in milliseconds
            """
            diff = self.get_duration() - self.target_duration * 1000
            if abs(diff) > DURATION_MAX_DIFF:
                messages.append(
                    _(
                        "durations do not match. difference is: %s seconds"
                        % int(diff / 1000)
                    )
                )
                log.warning(
                    "durations do not match. difference is: %s seconds"
                    % int(diff / 1000)
                )
                status = 2

        except Exception as e:
            messages.append(_("Validation error: %s " % e))
            log.warning("validation error: %s " % e)
            status = 99

        if status == 1:
            log.info('Playlist "%s" checked - all fine!' % (self.name))

        return status, messages

    ###################################################################
    # playlist mixdown
    ###################################################################
    def get_mixdown(self):
        """
        get mixdown from api
        """
        return MixdownAPIClient().get_for_playlist(self)

    def request_mixdown(self):
        """
        request (re-)creation of mixdown
        """
        return MixdownAPIClient().request_for_playlist(self)

    def download_mixdown(self):
        """
        download generated mixdown from api & store locally (in `mixdown_file` field)
        """
        if not self.mixdown:
            log.info("mixdown not available on api")
            return

        if not self.mixdown["status"] == 3:
            log.info("mixdown not ready on api")
            return

        url = self.mixdown["mixdown_file"]

        log.debug("download mixdown from api: {} > {}".format(url, self.name))

        f_temp = NamedTemporaryFile(delete=True)
        f_temp.write(urlopen(url).read())
        f_temp.flush()

        # wipe existing file
        try:
            self.mixdown_file.delete(False)
        except IOError:
            pass

        self.mixdown_file.save(url.split("/")[-1], File(f_temp))

        return MixdownAPIClient().request_for_playlist(self)

    @property
    def sorted_items(self):
        return self.items.order_by("playlist_items__position")

    @cached_property
    def num_media(self):
        return self.items.count()

    @cached_property
    def mixdown(self):
        return self.get_mixdown()

    # provide type-based properties
    @property
    def is_broadcast(self):
        return self.type == Playlist.TYPE_BROADCAST

    @property
    def is_playlist(self):
        return self.type == Playlist.TYPE_PLAYLIST

    @cached_property
    def is_archived(self):
        if not self.type == Playlist.TYPE_BROADCAST:
            return
        if self.rotation_date_end and self.rotation_date_end < timezone.now().date():
            return True

    @cached_property
    def is_upcoming(self):
        if not self.type == Playlist.TYPE_BROADCAST:
            return
        if (
            self.rotation_date_start
            and self.rotation_date_start > timezone.now().date()
        ):
            return True

    @cached_property
    def series_display(self):
        if not self.series:
            return
        if self.series_number:
            return "{} #{}".format(self.series.name, self.series_number)
        return self.series.name

    @cached_property
    def last_emission(self):
        ###############################################################
        # we cannot filter a prefetched qs - so to avoid
        # additional queries we have to loop the qs and 'filter'
        # 'manually'
        ###############################################################
        for emission in self.emissions.order_by("-time_start"):
            if emission.time_start < timezone.now():
                return emission

    @cached_property
    def next_emission(self):
        ###############################################################
        # we cannot filter a prefetched qs - so to avoid
        # additional queries we have to loop the qs and 'filter'
        # 'manually'
        ###############################################################
        for emission in self.emissions.order_by("time_start"):
            if emission.time_start > timezone.now():
                return emission

    def save(self, *args, **kwargs):

        # status update
        if self.status == 0:
            self.status = 2

        try:
            self.duration = self.get_duration()
        except Exception as e:
            self.duration = 0

        # auto-add incremented series number
        if self.series and not self.series_number:
            _qs = (
                type(self)
                .objects.filter(series=self.series)
                .exclude(pk=self.pk)
                .order_by("-series_number")
            )
            _p = _qs.first()
            if _p and _p.series_number:
                self.series_number = _p.series_number + 1
            else:
                self.series_number = 1

        # TODO: maybe move
        self.broadcast_status, self.broadcast_status_messages = self.self_check()
        if self.broadcast_status == 1:
            self.status = 1  # 'ready'
        else:
            self.status = 99  # 'error'

        # handle series numbering

        super(Playlist, self).save(*args, **kwargs)


try:
    tagging_register(Playlist)
except Exception as e:
    pass

arating.enable_voting_on(Playlist)


@receiver(post_save, sender=Playlist)
def playlist_post_save(sender, instance, **kwargs):

    if not instance.type == "broadcast":
        return

    if instance.mixdown_file:
        return

    if instance.mixdown:
        return

    log.debug("no mixdown yet for {} - request to generate".format(instance.name))
    instance.request_mixdown()


class PlaylistItemPlaylist(TimestampedModelMixin, models.Model):

    playlist = models.ForeignKey(
        "Playlist", on_delete=models.CASCADE, related_name="playlist_items"
    )
    item = models.ForeignKey(
        "PlaylistItem", on_delete=models.CASCADE, related_name="playlist_items"
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    position = models.PositiveIntegerField(default=0)

    cue_in = models.PositiveIntegerField(default=0)
    cue_out = models.PositiveIntegerField(default=0)
    fade_in = models.PositiveIntegerField(default=0)
    fade_out = models.PositiveIntegerField(default=0)
    fade_cross = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "alibrary"
        ordering = ("position",)

    def save(self, *args, **kwargs):

        # catch invalid cases
        if int(self.fade_cross) > int(self.fade_out):
            self.fade_cross = int(self.fade_out) - 1

        if int(self.fade_cross) < 0:
            self.fade_cross = 0

        if int(self.cue_in) < 0:
            self.cue_in = 0

        if int(self.cue_out) < 0:
            self.cue_out = 0

        if int(self.fade_in) < 0:
            self.fade_in = 0

        if int(self.fade_out) < 0:
            self.fade_out = 0

        super(PlaylistItemPlaylist, self).save(*args, **kwargs)


@python_2_unicode_compatible
class PlaylistItem(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        app_label = "alibrary"
        verbose_name = _("Playlist Item")
        verbose_name_plural = _("Playlist Items")
        # ordering = ('-created', )

    ct_limit = models.Q(app_label="alibrary", model="media") | models.Q(
        app_label="alibrary", model="release"
    )

    content_type = models.ForeignKey(ContentType, limit_choices_to=ct_limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "%s" % (self.pk)

    def save(self, *args, **kwargs):
        super(PlaylistItem, self).save(*args, **kwargs)
