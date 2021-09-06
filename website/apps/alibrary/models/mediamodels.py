# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
import uuid
import arating
import tagging
from base.audio.fileinfo import FileInfoProcessor
from cacheops import invalidate_obj
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django_extensions.db.fields import AutoSlugField
from base.fields.languages import LanguageField
from base.signals.unsignal import disable_for_loaddata
from base.mixins import TimestampedModelMixin, UUIDModelMixin
from base.fs.utils import sha1_by_file
from tagging.registry import register as tagging_register

from alibrary import settings as alibrary_settings
from alibrary.models.basemodels import MigrationMixin, License, Relation, Profession
from alibrary.models.playlistmodels import PlaylistItem, Playlist
from alibrary.util.slug import unique_slugify
from alibrary.util.storage import get_dir_for_object

from alibrary.tasks import ingest_fprint_for_media, delete_fprint_for_media

USE_CELERYD = getattr(settings, "ALIBRARY_USE_CELERYD", False)
AUTOCREATE_FPRINT = getattr(settings, "ALIBRARY_AUTOCREATE_FPRINT", True)

LAME_BINARY = getattr(settings, "LAME_BINARY")
SOX_BINARY = getattr(settings, "SOX_BINARY")
FAAD_BINARY = getattr(settings, "FAAD_BINARY")

LOOKUP_PROVIDERS = (("musicbrainz", _("Musicbrainz")),)

VERSION_CHOICES = (
    ("original", _("Original")),
    ("track", _("Track")),
    ("remix", _("Remix")),
    ("cover", _("Cover")),
    ("live", _("Live Version")),
    ("studio", _("Studio Version")),
    ("radio", _("Radio Version")),
    ("demo", _("Demo Version")),
    ("other", _("Other")),
)

MEDIATYPE_CHOICES = (
    (
        _("Single content recording"),
        (
            ("song", _("Song")),
            ("acappella", _("A cappella")),
            ("soundeffects", _("Sound effects")),
            ("soundtrack", _("Soundtrack")),
            ("spokenword", _("Spokenword")),
            ("interview", _("Interview")),
            ("jingle", _("Jingle")),
        ),
    ),
    (
        _("Multiple content recording"),
        (
            ("djmix", _("DJ-Mix")),
            ("concert", _("Concert")),
            ("liveact", _("Live Act (PA)")),
            ("radioshow", _("Radio show")),
        ),
    ),
    ("other", _("Other")),
    (None, _("Unknown")),
)


VALID_BITRATES = [56, 64, 96, 128, 160, 196, 256, 320]

LOSSLESS_CODECS = ["wav", "aif", "aiff", "flac"]

log = logging.getLogger(__name__)


def upload_master_to(instance, filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join(get_dir_for_object(instance), "master%s" % extension.lower())


@python_2_unicode_compatible
class Media(MigrationMixin, UUIDModelMixin, TimestampedModelMixin, models.Model):

    STATUS_CHOICES = (
        (0, _("Init")),
        (1, _("Ready")),
        (3, _("Working")),
        (4, _("File missing")),
        (5, _("File error")),
        (99, _("Error")),
    )

    TRACKNUMBER_CHOICES = ((x, x) for x in range(1, 301))
    MEDIANUMBER_CHOICES = ((x, x) for x in range(1, 51))

    lock = models.PositiveIntegerField(default=0, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = AutoSlugField(
        populate_from="name", editable=True, blank=True, overwrite=True
    )
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES)
    publish_date = models.DateTimeField(blank=True, null=True)
    tracknumber = models.PositiveIntegerField(
        verbose_name=_("Track Number"),
        blank=True,
        null=True,
        choices=TRACKNUMBER_CHOICES,
    )
    opus_number = models.CharField(max_length=200, blank=True, null=True)
    medianumber = models.PositiveIntegerField(
        verbose_name=_('a.k.a. "Disc number'),
        blank=True,
        null=True,
        choices=MEDIANUMBER_CHOICES,
    )
    mediatype = models.CharField(
        verbose_name=_("Type"),
        max_length=128,
        default="song",
        choices=MEDIATYPE_CHOICES,
    )
    version = models.CharField(
        max_length=12, blank=True, null=True, default="track", choices=VERSION_CHOICES
    )
    description = models.TextField(
        verbose_name="Extra Description / Tracklist", blank=True, null=True
    )
    lyrics = models.TextField(blank=True, null=True)
    lyrics_language = LanguageField(blank=True, null=True)

    duration = models.PositiveIntegerField(
        verbose_name="Duration (in ms)", blank=True, null=True, editable=False
    )

    # relations
    release = models.ForeignKey(
        "alibrary.Release",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="media_release",
    )
    artist = models.ForeignKey(
        "alibrary.Artist", blank=True, null=True, related_name="media_artist"
    )

    # user relations
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="media_owner",
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_media",
    )
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="media_last_editor",
    )
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="media_publisher",
    )

    # identifiers
    isrc = models.CharField(verbose_name="ISRC", max_length=12, null=True, blank=True)

    # relations a.k.a. links
    relations = GenericRelation(Relation)
    playlist_items = GenericRelation(PlaylistItem, object_id_field="object_id")

    # reverse generic relation for atracker events
    events = GenericRelation("atracker.Event")

    # tagging (d_tags = "display tags")
    d_tags = tagging.fields.TagField(
        verbose_name="Tags", max_length=1024, blank=True, null=True
    )

    # provide 'multi-names' for artist crediting, like: Artist X feat. Artist Y & Artist Z
    media_artists = models.ManyToManyField(
        "alibrary.Artist", blank=True, through="MediaArtists", related_name="credited"
    )

    # extra-artists
    extra_artists = models.ManyToManyField(
        "alibrary.Artist", blank=True, through="MediaExtraartists"
    )

    license = models.ForeignKey(
        License,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="media_license",
        limit_choices_to={"selectable": True},
    )

    filename = models.CharField(
        verbose_name=_("Filename"), max_length=256, blank=True, null=True
    )
    original_filename = models.CharField(
        verbose_name=_("Original filename"), max_length=256, blank=True, null=True
    )

    folder = models.CharField(max_length=1024, null=True, blank=True, editable=False)

    #######################################################################
    # master audio-file data
    # TODO: all version- & conversion based data will be refactored.
    # the media model should just hold information about the associated master file
    #######################################################################
    master = models.FileField(
        max_length=1024, upload_to=upload_master_to, blank=True, null=True
    )
    master_sha1 = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    master_encoding = models.CharField(max_length=16, blank=True, null=True)
    master_bitrate = models.PositiveIntegerField(
        verbose_name=_("Bitrate"), blank=True, null=True
    )
    master_filesize = models.PositiveIntegerField(
        verbose_name=_("Filesize"), blank=True, null=True
    )
    master_samplerate = models.PositiveIntegerField(
        verbose_name=_("Samplerate"), blank=True, null=True
    )
    master_duration = models.FloatField(
        verbose_name=_("Duration"), blank=True, null=True
    )

    #######################################################################
    # audio properties
    #######################################################################
    tempo = models.FloatField(null=True, blank=True)

    #######################################################################
    # fprint data
    #######################################################################
    fprint_ingested = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        app_label = "alibrary"
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
        ordering = ("medianumber", "tracknumber", "name")

        permissions = (
            ("play_media", "Play Track"),
            # TODO: fix typo in "downoad"
            ("downoad_media", "Download Track"),
            ("download_master", "Download Master"),
            ("edit_media", "Edit Track"),
            ("merge_media", "Merge Tracks"),
            ("reassign_media", "Re-assign Tracks"),
            ("admin_media", "Edit Track (extended)"),
            ("upload_media", "Upload Track"),
        )

    def __str__(self):
        return self.name

    @property
    def duration_s(self):
        return self.get_duration(units="s")

    @property
    def duration_ms(self):
        return self.get_duration(units="ms")

    @property
    def is_lossless(self):
        if self.master_encoding and self.master_encoding.lower() in LOSSLESS_CODECS:
            return True

    @property
    def bitrate(self):
        if not self.is_lossless:
            return self.master_bitrate

    @property
    def classname(self):
        return self.__class__.__name__

    @property
    def main_image(self):
        """main image referes to release image if available"""
        if self.release:
            return self.release.main_image

    @property
    def is_jingle(self):
        return self.mediatype == "jingle"

    def get_lookup_providers(self):

        providers = []
        for key, name in LOOKUP_PROVIDERS:
            relations = self.relations.filter(service=key)
            relation = None
            if relations.count() == 1:
                relation = relations[0]

            providers.append({"key": key, "name": name, "relation": relation})

        return providers

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()

    def get_absolute_url(self):
        return reverse("alibrary-media-detail", kwargs={"uuid": str(self.uuid)})

    def get_edit_url(self):
        return reverse("alibrary-media-edit", args=(self.pk,))

    def get_admin_url(self):
        return reverse("admin:alibrary_media_change", args=(self.pk,))

    def get_api_url(self):
        return reverse(
            "api_dispatch_detail",
            kwargs={
                "api_name": "v1",
                "resource_name": "library/track",
                "uuid": self.uuid,
            },
        )

    # TODO: refactor to admin module
    def release_link(self):
        if self.release:
            return '<a href="%s">%s</a>' % (
                reverse("admin:alibrary_release_change", args=(self.release.id,)),
                self.release.name,
            )
        return None

    release_link.allow_tags = True
    release_link.short_description = "Edit"

    @property
    def master_url(self):
        return reverse("api:media-download-master", args=(self.uuid,))

    # TODO: depreciated
    def get_playlink(self):
        return "/api/tracks/%s/#0#replace" % self.uuid

    # TODO: depreciated
    def get_download_permissions(self):
        pass

    def generate_sha1(self):
        return sha1_by_file(self.master)

    def get_videoclips(self):
        return self.relations.filter(service__in=["youtube", "vimeo"])

    @property
    def has_soundcloud(self):
        return self.relations.filter(service="soundcloud").exists()

    @property
    def get_soundcloud(self):
        return self.relations.filter(service="soundcloud").first()

    @cached_property
    def emissions(self):
        from abcast.models import Emission

        playlist_qs = self.get_appearances()

        emission_qs = (
            Emission.objects.filter(
                object_id__in=playlist_qs.values_list("id", flat=True),
                content_type=ContentType.objects.get_for_model(Playlist),
            )
            .order_by("-time_start")
            .distinct()
        )

        return emission_qs

    @cached_property
    def last_emission(self):
        return self.emissions.first()

    # TODO: this is ugly - improve!
    def get_artist_display(self):

        artist_str = ""
        artists = self.get_mediaartists()
        if len(artists) > 1:
            try:
                for artist in artists:
                    if artist["join_phrase"]:
                        if artist["join_phrase"] != ",":
                            artist_str += " "
                        artist_str += "%s " % artist["join_phrase"]

                    artist_str += artist["artist"].name
            except:
                artist_str = artists[0].name
        else:
            try:
                artist_str = artists[0].name
            except:

                try:
                    artist_str = self.artist.name
                except:
                    artist_str = _("Unknown Artist")

        return artist_str

    def get_mediaartists(self):

        artists = []
        if self.media_artists.exists():
            for media_artist in self.media_mediaartist.all().select_related("artist"):
                artists.append(
                    {
                        "artist": media_artist.artist,
                        "join_phrase": media_artist.join_phrase,
                    }
                )
            return artists

        return artists

    def get_master_path(self):
        try:
            return self.master.path
        except Exception as e:
            log.warning("unable to get master path for: %s" % self.name)

    def get_directory(self, absolute=False):

        if self.folder and absolute:
            return os.path.join(settings.MEDIA_ROOT, self.folder)

        elif self.folder:
            return self.folder

        else:
            log.warning(
                "unable to get directory path for: %s - %s" % (self.pk, self.name)
            )
            return None

    def get_file(self, source, version):
        # TODO: implement...
        return self.master

    def get_playout_file(self, absolute=False):

        abs_path = self.master.path

        if not absolute:
            if settings.MEDIA_ROOT.endswith("/"):
                path = abs_path.replace(settings.MEDIA_ROOT + "/", "")
            else:
                path = abs_path.replace(settings.MEDIA_ROOT, "")

        else:
            path = abs_path

        return path

    def get_duration(self, units="ms"):

        if not self.master_duration:
            return

        if units == "ms":
            return int(self.master_duration * 1000)

        if units == "s":
            return int(self.master_duration)

    def get_appearances(self):
        qs = (
            Playlist.objects.filter(
                playlist_items__item__object_id=self.pk,
                playlist_items__item__content_type=ContentType.objects.get_for_model(
                    self
                ),
            )
            .exclude(type=Playlist.TYPE_OTHER)
            .order_by("-type", "-created")
            .nocache()  # NOTE: do we need `nocache()` here?
            .distinct()
        )

        return qs

    # # TODO: check usage.
    # @cached_property
    # def appearances(self):
    #     return self.get_appearances()
    #
    @cached_property
    def broadcast_appearances(self):
        return self.get_appearances().filter(type=Playlist.TYPE_BROADCAST)

    @cached_property
    def playlist_appearances(self):
        return self.get_appearances().filter(type=Playlist.TYPE_PLAYLIST)

    @cached_property
    def public_appearances(self):
        if self.mediatype == "jingle":
            return None
        return self.broadcast_appearances | self.playlist_appearances

    def process_master_info(self, save=False):

        # read key information from master file
        if self.master:
            file_processor = FileInfoProcessor(self.master.path)
            if file_processor.audio_stream:
                self.master_encoding = file_processor.encoding
                self.master_filesize = file_processor.filesize
                self.master_bitrate = file_processor.bitrate
                self.master_samplerate = file_processor.samplerate
                self.master_duration = file_processor.duration

            else:
                log.warning('unable to process audio file using "FileInfoProcessor"')

            if save:
                self.save()

    def save(self, *args, **kwargs):

        # Assign a default license
        """
        - not applying default license anymore
        - applying default license again: #898
        """
        if not self.license:
            try:
                license = License.objects.filter(is_default=True)[0]
                self.license = license
                log.debug("applied default license: %s" % license.name)
            except Exception as e:
                log.warning("unable to apply default license: {}".format(e))

        self.master_changed = False
        if self.uuid is not None:
            try:
                orig = Media.objects.filter(uuid=self.uuid)[0]
                if orig.master != self.master:
                    self.master_changed = True
            except:
                pass

        if self.master_changed:
            self.process_master_info()

        # check if master changed. if yes we need to reprocess the cached files
        if self.pk is not None:

            try:
                orig = Media.objects.filter(pk=self.pk)[0]
                if orig.master != self.master:
                    log.info(
                        'Media id: %s - Master changed from "%s" to "%s"'
                        % (self.pk, orig.master, self.master)
                    )

                    # `_master_changed` can be / is used in signal listeners
                    self._master_changed = True

                    # reset processing flags
                    self.fprint_ingested = None

                    # set 'original filename'
                    if not self.original_filename and self.master.name:
                        try:
                            self.original_filename = self.master.name[0:250]
                        except Exception as e:
                            log.warning(
                                "unable to update original_filename on media: {}".format(
                                    self.pk
                                )
                            )

            except Exception as e:
                log.warning("unable to update master: {}".format(e))

        if self.version:
            self.version = self.version.lower()

        if self.mediatype:
            self.mediatype = self.mediatype.lower()

        # sha1 for quick duplicate checks
        if self.master and not self.master_sha1:
            self.master_sha1 = self.generate_sha1()
        else:
            self.master_sha1 = None

        unique_slugify(self, self.name)

        # pretty of ugly, clean empty relations
        for ea in MediaExtraartists.objects.filter(media__pk=self.pk):
            try:
                if not ea.artist:
                    ea.delete()
            except:
                pass

        # TODO: remove! just for testing!
        # self._master_changed = True

        super(Media, self).save(*args, **kwargs)


# media post save
@disable_for_loaddata
def media_post_save(sender, **kwargs):

    obj = kwargs["instance"]

    # ingest fingerprint
    if (AUTOCREATE_FPRINT and obj.master) and not obj.fprint_ingested:
        ingest_fprint_for_media.apply_async((obj.pk,))

    if not obj.folder:

        log.debug("no directory for media %s - create it." % obj.pk)
        directory = get_dir_for_object(obj)
        abs_directory = os.path.join(settings.MEDIA_ROOT, directory)

        try:
            if not os.path.exists(abs_directory):
                os.makedirs(abs_directory, 0o755)

            obj.folder = directory
            log.debug("creating directory: %s" % abs_directory)

        except Exception as e:
            log.warning("unable to create directory: %s - %s" % (abs_directory, e))
            obj.folder = None
            obj.status = 99

    # invalidate cache
    invalidate_obj(obj)


post_save.connect(media_post_save, sender=Media)


def media_pre_delete(sender, **kwargs):

    obj = kwargs["instance"]

    # delete associated master file
    if obj.master and os.path.isfile(obj.master.path):
        os.unlink(obj.master.path)

    # delete fingerprint
    delete_fprint_for_media.apply_async((obj.uuid,))


pre_delete.connect(media_pre_delete, sender=Media)


arating.enable_voting_on(Media)

try:
    tagging_register(Media)
except Exception as e:
    pass


@python_2_unicode_compatible
class MediaExtraartists(models.Model):

    artist = models.ForeignKey(
        "alibrary.Artist",
        related_name="extraartist_artist",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    media = models.ForeignKey(
        "Media",
        related_name="extraartist_media",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    profession = models.ForeignKey(
        Profession,
        verbose_name="Role/Profession",
        related_name="media_extraartist_profession",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "alibrary"
        ordering = ("artist__name", "profession__name")

    def __str__(self):
        if self.artist and self.profession:
            return 'Credited "%s" as "%s"' % (self.artist.name, self.profession.name)
        elif self.artist:
            return 'Credited "%s"' % (self.artist.name)
        else:
            return 'Credited "%s"' % self.pk


@receiver(post_delete, sender=MediaExtraartists)
def media_extraartists_post_delete(sender, instance, **kwargs):
    # clear caches
    from alibrary.models import Artist

    Artist.get_releases.invalidate(instance.artist)
    Artist.get_media.invalidate(instance.artist)


@python_2_unicode_compatible
class MediaArtists(models.Model):

    artist = models.ForeignKey(
        "alibrary.Artist", related_name="artist_mediaartist", on_delete=models.CASCADE
    )
    media = models.ForeignKey(
        "Media", related_name="media_mediaartist", on_delete=models.CASCADE
    )
    join_phrase = models.CharField(
        verbose_name="join phrase",
        max_length=12,
        blank=True,
        null=True,
        default=None,
        choices=alibrary_settings.ARTIST_JOIN_PHRASE_CHOICES,
    )
    position = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        app_label = "alibrary"
        verbose_name = _("Artist (title credited)")
        verbose_name_plural = _("Artists (title credited)")
        ordering = ("position",)

    def __str__(self):

        if self.join_phrase:
            return '%s credited with "%s" on %s' % (
                self.artist,
                self.join_phrase,
                self.media,
            )
        else:
            return "%s on %s" % (self.artist, self.media)


@receiver(post_delete, sender=MediaArtists)
def media_artists_post_delete(sender, instance, **kwargs):

    # clear caches
    from alibrary.models import Artist

    Artist.get_releases.invalidate(instance.artist)
    Artist.get_media.invalidate(instance.artist)
