# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.core import urlresolvers
from hvad.admin import TranslatableAdmin
from genericadmin.admin import GenericAdminModelAdmin, GenericTabularInline
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer

from django.contrib import admin
from alibrary.models import (
    Label,
    Artist,
    Media,
    Release,
    Playlist,
    ReleaseExtraartists,
    ReleaseAlbumartists,
    Relation,
    ReleaseMedia,
    MediaExtraartists,
    NameVariation,
    License,
    ArtistProfessions,
    Profession,
    Distributor,
    PlaylistItem,
    PlaylistItemPlaylist,
    Daypart,
    Season,
    Weather,
    Series,
)

THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


# from guardian.admin import GuardedModelAdmin
# class BaseAdmin(GuardedModelAdmin):
class BaseAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    save_on_top = True


class LabelInline(admin.TabularInline):
    model = Label
    extra = 1


class MediaInline(admin.TabularInline):
    model = Media

    fields = [
        "name",
        "tracknumber",
        "opus_number",
        "version",
        "artist",
        "isrc",
        "license",
        "original_filename",
        "master_encoding",
        "master_bitrate",
        "master_samplerate",
        "master_duration",
    ]

    readonly_fields = [
        "original_filename",
        "master_encoding",
        "master_bitrate",
        "master_samplerate",
        "master_duration",
    ]

    raw_id_fields = ["artist"]

    extra = 0


class ReleaseExtraartistsInline(admin.TabularInline):
    model = ReleaseExtraartists
    extra = 1
    raw_id_fields = ["artist"]


class ReleaseAlbumartistsInline(admin.TabularInline):
    model = ReleaseAlbumartists
    extra = 2
    fieldsets = [(None, {"fields": ["position", "join_phrase", "artist"]})]
    raw_id_fields = ["artist"]


class RelationsInline(GenericTabularInline):
    model = Relation
    extra = 2
    fieldsets = [(None, {"fields": ["url", "name", "service"]})]
    readonly_fields = ["service"]


class ReleaseMediaMediaInline(admin.TabularInline):
    model = Media
    extra = 1


class ReleaseMediaInline(admin.TabularInline):
    model = ReleaseMedia
    extra = 1
    inlines = [ReleaseMediaMediaInline]


class ReleaseAdmin(BaseAdmin):
    list_display = (
        "image_display",
        # 'name',
        "info_display",
        "meta_display",
        "catalognumber",
    )

    list_display_links = ["catalognumber"]

    search_fields = ["name", "catalognumber", "label__name"]

    list_filter = ("releasetype",)
    date_hierarchy = "created"

    inlines = [
        ReleaseAlbumartistsInline,
        MediaInline,
        RelationsInline,
        ReleaseExtraartistsInline,
    ]
    readonly_fields = ["slug", "license", "d_tags"]

    raw_id_fields = ["label", "owner", "creator", "last_editor", "publisher"]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "main_image",
                    ("label", "catalognumber"),
                    ("releasedate", "release_country", "license"),
                    ("releasetype",),
                    "d_tags",
                    "description",
                ]
            },
        ),
        ("Users", {"fields": ["owner", "creator", "last_editor", "publisher"]}),
    ]

    def info_display(self, obj):

        tpl = """<p>
        <strong><a href="{object_url}">{object_name}</strong></a><br>
        by: {artist_name}<br>
        on: <a href="{label_url}">{label_name}</a>
        </p>""".format(
            object_url=urlresolvers.reverse(
                "admin:alibrary_release_change", args=(obj.pk,)
            )
            if obj.label
            else "#",
            object_name=obj.name[0:40],
            artist_name=obj.get_artist_display(),
            label_url=urlresolvers.reverse(
                "admin:alibrary_label_change", args=(obj.label.pk,)
            )
            if obj.label
            else "#",
            label_name=obj.label,
        )
        return tpl

    info_display.short_description = _("Release")
    info_display.allow_tags = True

    def meta_display(self, obj):

        tpl = """<p>
        <strong>{releasedate}</strong><br>
        {type}<br>
        {num_tracks} Tracks<br>
        </p>""".format(
            releasedate=obj.releasedate_approx,
            type=obj.get_releasetype_display(),
            num_tracks=obj.get_media().count(),
        )
        return tpl

    meta_display.short_description = _("Metadata")
    meta_display.allow_tags = True

    def image_display(self, obj):
        if obj.main_image:
            try:
                return '<img src="%s" />' % (
                    get_thumbnailer(obj.main_image).get_thumbnail(THUMBNAIL_OPT).url
                )
            except Exception as e:
                pass
        return "-"

    image_display.short_description = _("Cover")
    image_display.allow_tags = True


admin.site.register(Release, ReleaseAdmin)


class ArtistMembersInline(admin.TabularInline):
    model = Artist.members.through
    fk_name = "parent"
    raw_id_fields = ["child"]
    extra = 1


class ArtistParentsInline(admin.TabularInline):
    model = Artist.members.through
    fk_name = "child"
    raw_id_fields = ["parent"]
    extra = 1


class ArtistProfessionsInline(admin.TabularInline):
    model = ArtistProfessions
    extra = 1


class MediaExtraartistsInline(admin.TabularInline):
    model = MediaExtraartists
    extra = 1
    raw_id_fields = ["artist"]


class NameVariationInline(admin.TabularInline):
    model = NameVariation
    extra = 3


class ArtistAdmin(BaseAdmin):

    list_display = ["name", "type", "disambiguation", "listed"]
    search_fields = ["name", "media__name"]
    list_filter = ["listed"]

    # RelationsInline,
    inlines = [
        NameVariationInline,
        RelationsInline,
        ArtistProfessionsInline,
        ArtistMembersInline,
        ArtistParentsInline,
    ]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "main_image",
                    "real_name",
                    "country",
                    ("listed", "disable_link"),
                    "biography",
                    "excerpt",
                ]
            },
        ),
        ("Users", {"fields": ["owner", "creator", "last_editor", "publisher"]}),
        ("Various", {"fields": ["booking_contact", "email"]}),
    ]

    raw_id_fields = ["owner", "creator", "last_editor", "publisher"]


admin.site.register(Artist, ArtistAdmin)
admin.site.register(NameVariation)


class LicenseAdmin(TranslatableAdmin):
    inline_instances = ("name_translated", "restricted", "parent")

    search_fields = ("name",)


admin.site.register(License, LicenseAdmin)


class RelationAdmin(BaseAdmin):
    list_display = ("url", "service", "name")
    list_filter = ("service",)
    search_fields = ("url",)
    fieldsets = [(None, {"fields": ["url", "service"]})]
    # readonly_fields = ['service']


admin.site.register(Relation, RelationAdmin)


class ProfessionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profession, ProfessionAdmin)

""""""


class MediaReleaseInline(admin.TabularInline):
    model = Release.media.through
    extra = 1
    raw_id_fields = ["release"]


class MediaAdmin(BaseAdmin):
    list_display = [
        "name",
        "created",
        "release_link",
        "artist",
        "mediatype",
        "tracknumber",
        "medianumber",
        "master_duration",
        "master_status",
        "fprint_ingested",
    ]

    search_fields = ["artist__name", "release__name", "name"]

    list_filter = ("mediatype", "preflight_check__status", "license__name")

    inlines = [MediaReleaseInline, RelationsInline, MediaExtraartistsInline]

    readonly_fields = ["slug", "uuid", "release_link", "master_sha1", "d_tags"]

    date_hierarchy = "created"

    def master_status(self, obj):
        if not obj.master or not obj.master.path:
            return False
        return os.path.isfile(obj.master.path)

    master_status.boolean = True

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "isrc",
                    "filename",
                    "uuid",
                    ("tracknumber", "medianumber", "opus_number"),
                    "mediatype",
                    "version",
                    ("release", "release_link"),
                    "artist",
                    "license",
                    "d_tags",
                ]
            },
        ),
        ("Users", {"fields": ["owner", "creator", "last_editor", "publisher"]}),
        ("Text", {"fields": ["description", "lyrics"]}),
        (
            "Master Audio File",
            {
                "fields": [
                    "master",
                    "master_sha1",
                    ("master_encoding", "master_bitrate", "master_samplerate"),
                    ("master_duration", "master_filesize"),
                ]
            },
        ),
        ("Analyse & co", {"classes": ("uncollapse",), "fields": ("fprint_ingested",)}),
    ]

    raw_id_fields = [
        "owner",
        "creator",
        "last_editor",
        "publisher",
        "release",
        "artist",
    ]


admin.site.register(Media, MediaAdmin)


class DistributorLabelInline(admin.TabularInline):
    model = Distributor.labels.through
    extra = 1


class LabelAdmin(BaseAdmin):
    # inlines = [LabelInline]
    readonly_fields = ["slug"]

    inlines = [RelationsInline]

    """"""
    fieldsets = [
        (None, {"fields": ["name", "slug", "main_image", "type", "description"]}),
        ("Contact", {"fields": ["address", "country", ("phone", "fax"), "email"]}),
        ("Settings", {"fields": ["listed", "disable_link", "disable_editing"]}),
        ("Relations", {"fields": ["parent"], "classes": [""]}),
        ("Users", {"fields": [("owner", "creator", "last_editor", "publisher")]}),
    ]

    raw_id_fields = ["owner", "creator", "last_editor", "publisher", "parent"]


admin.site.register(Label, LabelAdmin)


class DistributorAdmin(BaseAdmin):

    list_display = ["name", "email", "country", "address", "created"]

    readonly_fields = ["slug", "d_tags"]

    inlines = [DistributorLabelInline, RelationsInline]

    fieldsets = [
        (None, {"fields": ["name", "slug", "type", "description"]}),
        ("Contact", {"fields": ["address", "country", ("phone", "fax"), "email"]}),
        ("Relations", {"fields": ["parent"], "classes": [""]}),
    ]


admin.site.register(Distributor, DistributorAdmin)


class PlaylistItemInline(GenericTabularInline):
    model = PlaylistItem
    extra = 1


class PlaylistItemPlaylistInline(admin.TabularInline):
    model = PlaylistItemPlaylist
    inlines = [PlaylistItemInline]
    raw_id_fields = ["item"]
    extra = 1


def playlists_enable_rotation(modeladmin, request, queryset):
    queryset.update(rotation=True)


playlists_enable_rotation.short_description = _(
    "Include selected playlists in rotation"
)


def playlists_disable_rotation(modeladmin, request, queryset):
    queryset.update(rotation=False)


playlists_disable_rotation.short_description = _(
    "Exclude selected playlists from rotation"
)


class PlaylistAdmin(GenericAdminModelAdmin):
    list_display = (
        "name",
        "user",
        "type",
        "duration",
        "target_duration",
        "is_current",
        "rotation",
        "updated",
    )
    list_filter = ("type", "broadcast_status")

    search_fields = ["name", "user__username"]
    date_hierarchy = "created"

    raw_id_fields = ["user"]

    actions = [playlists_enable_rotation, playlists_disable_rotation]

    # readonly_fields = ['slug', 'is_current',]

    inlines = [PlaylistItemPlaylistInline]


class PlaylistItemAdmin(GenericAdminModelAdmin):
    pass


class DaypartAdmin(BaseAdmin):
    list_display = ("day", "time_start", "time_end", "active", "playlist_count")
    list_filter = ("day", "active")


admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Daypart, DaypartAdmin)
admin.site.register(PlaylistItem, PlaylistItemAdmin)


class SeriesAdmin(admin.ModelAdmin):
    pass


class SeasonAdmin(TranslatableAdmin):
    pass


class WeatherAdmin(TranslatableAdmin):
    pass


admin.site.register(Season, SeasonAdmin)
admin.site.register(Weather, WeatherAdmin)

admin.site.register(Series, SeriesAdmin)
