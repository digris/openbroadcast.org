# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from versatileimagefield.serializers import VersatileImageFieldSerializer

from media_asset.models import Format, Waveform
from profiles.apiv2.serializers import ProfileSerializer

from ..models import (
    Artist,
    Release,
    Media,
    Playlist,
    PlaylistItem,
    PlaylistItemPlaylist,
)

SITE_URL = getattr(settings, "SITE_URL")


class ImageSerializer(serializers.ImageField):
    def to_representation(self, instance):

        if not instance:
            return

        return "{}{}".format(SITE_URL, thumbnail_url(instance, "thumbnail_240"))


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:artist-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct")

    detail_url = serializers.URLField(source="get_absolute_url")

    image = ImageSerializer(source="main_image")

    class Meta:
        model = Artist
        depth = 1
        fields = ["url", "ct", "detail_url", "uuid", "name", "image"]


class MediaSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:media-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct")

    detail_url = serializers.URLField(source="get_absolute_url")

    duration = serializers.FloatField(source="master_duration")

    artist = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="api:artist-detail", lookup_field="uuid"
    )

    release = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="api:release-detail", lookup_field="uuid"
    )

    artist_display = serializers.CharField(source="get_artist_display")

    image = ImageSerializer(source="release.main_image")

    release_display = serializers.SerializerMethodField()

    def get_release_display(self, obj, **kwargs):
        return obj.release.name if obj.release else None

    assets = serializers.SerializerMethodField()

    def get_assets(self, obj, **kwargs):
        # TODO: propperly serialize assets

        stream_url = reverse_lazy(
            "mediaasset-format",
            kwargs={"media_uuid": obj.uuid, "quality": "default", "encoding": "mp3"},
        )

        waveform_url = reverse_lazy(
            "mediaasset-waveform", kwargs={"media_uuid": obj.uuid, "type": "w"}
        )

        assets = {
            "stream": "{}{}".format(SITE_URL, stream_url),
            "waveform": "{}{}".format(SITE_URL, waveform_url),
        }

        # TODO: check if this is a good idea...
        # request asset generation for media
        # print('request asset generation for {}'.format(obj))
        # Format.objects.get_or_create_for_media(media=obj)
        # Waveform.objects.get_or_create_for_media(media=obj, type=Waveform.WAVEFORM)

        return assets

    class Meta:
        model = Media
        depth = 1
        fields = [
            "url",
            "ct",
            "detail_url",
            "uuid",
            "image",
            "name",
            "duration",
            "assets",
            "isrc",
            "artist_display",
            "release_display",
            "artist",
            "release",
        ]


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:release-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct")

    image = ImageSerializer(source="main_image")

    detail_url = serializers.URLField(source="get_absolute_url")
    releasedate = serializers.CharField(source="releasedate_approx")

    items = serializers.SerializerMethodField()

    def get_items(self, obj, **kwargs):
        items = []
        for media in obj.get_media():

            serializer = MediaSerializer(
                media, context={"request": self.context["request"]}
            )
            items.append({"content": serializer.data})

        return items

    class Meta:
        model = Release
        depth = 1
        fields = [
            "url",
            "ct",
            "uuid",
            "detail_url",
            "name",
            "image",
            "releasedate",
            "items",
        ]


class PlaylistItemField(serializers.RelatedField):
    """
    A custom field to use for the `item` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Media):
            # return 'Media: {}'.format(value.pk)
            serializer = MediaSerializer(
                value, context={"request": self.context["request"]}
            )
        elif isinstance(value, Media):
            return "Jingle: {}".format(value.pk)
        else:
            raise Exception("Unexpected type of tagged object")

        return serializer.data


class PlaylistItemSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#generic-relationships

    content = PlaylistItemField(read_only=True, source="content_object")

    class Meta:
        model = PlaylistItem
        depth = 1
        fields = ["content"]


class PlaylistItemPlaylistSerializer(serializers.ModelSerializer):
    # item = PlaylistItemSerializer(read_only=True)

    content = serializers.SerializerMethodField()

    def get_content(self, obj, **kwargs):

        # TODO: implement for `Jingle`
        if isinstance(obj.item.content_object, Media):
            serializer = MediaSerializer(
                instance=Media.objects.get(pk=obj.item.content_object.pk),
                many=False,
                context={"request": self.context["request"]},
            )
        elif isinstance(obj.item.content_object, Media):
            serializer = MediaSerializer(
                instance=Media.objects.get(pk=obj.item.content_object.pk),
                many=False,
                context={"request": self.context["request"]},
            )
        else:
            raise Exception("Unexpected type of tagged object")

        return serializer.data

    class Meta:
        model = PlaylistItemPlaylist
        depth = 1
        fields = [
            # 'item',
            "content",
            "position",
            "cue_in",
            "cue_out",
            "fade_in",
            "fade_out",
            "fade_cross",
        ]


class PlaylistSerializer(FlexFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:playlist-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct")

    image = ImageSerializer(source="main_image")

    detail_url = serializers.URLField(source="get_absolute_url")

    items = PlaylistItemPlaylistSerializer(source="playlist_items", many=True)

    tags = serializers.StringRelatedField(many=True)

    user = serializers.SerializerMethodField(source="user")

    item_appearances = serializers.SerializerMethodField()

    def get_user(self, obj):
        if not (obj.user and getattr(obj.user, "profile")):
            return
        return ProfileSerializer(obj.user.profile, context=self.context).data

    def get_item_appearances(self, obj, **kwargs):
        items = [
            "{}:{}".format(co.content_object.get_ct(), co.content_object.uuid)
            for co in obj.get_items()
        ]
        return items

    class Meta:
        model = Playlist
        depth = 1
        fields = [
            "url",
            "ct",
            "uuid",
            "detail_url",
            "name",
            "series_display",
            "image",
            "tags",
            "user",
            "mixdown_file",
            "items",
            "item_appearances",
            "num_media",
            "duration",
        ]
