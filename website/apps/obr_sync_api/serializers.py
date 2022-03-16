# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from alibrary.models import (
    Artist,
    Media,
    Release,
    Relation,
    Playlist,
    PlaylistItemPlaylist,
)
from profiles.models import Profile
from abcast.models import Emission
from tagging.models import Tag
from arating.models import Vote

User = get_user_model()

SITE_URL = getattr(settings, "SITE_URL")


class ApproximateDateSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not instance:
            return None
        return "{year:04d}-{month:02d}-{day:02d}".format(
            year=instance.year,
            month=instance.month or 1,
            day=instance.day or 1,
        )


class ImageSerializer(serializers.ImageField):
    def to_representation(self, instance):
        if not instance:
            return None
        try:
            return SITE_URL + instance.url
        except ValueError:
            # inconsistent case when file is missing
            return None


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "uuid",
            "type",
            "name",
        ]


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = [
            "uuid",
            "service",
            "url",
        ]


class MediaSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:media-detail",
        lookup_field="uuid",
    )
    ct = serializers.CharField(source="get_ct")

    # artist = serializers.HyperlinkedRelatedField(
    #     many=False,
    #     read_only=True,
    #     view_name="api:obr-sync:artist-detail",
    #     lookup_field="uuid",
    # )
    release = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()
    type = serializers.CharField(source="mediatype")
    duration = serializers.FloatField(source="master_duration")
    tags = TagSerializer(many=True)
    relations = RelationSerializer(many=True)

    def get_release(self, obj, **kwargs):
        if obj.release:
            return {
                "name": obj.release.name,
                "uuid": str(obj.release.uuid),
                "position": obj.tracknumber,
            }
        return None

    def get_artists(self, obj, **kwargs):
        # NOTE: kind of ugly.. unifies track artist (1-1) and extra artists
        if obj.artist:
            yield {
                "name": obj.artist.name,
                "ct": obj.artist.get_ct(),
                "uuid": str(obj.artist.uuid),
                "join_phrase": None,
                "position": 0,
            }
        for position, media_artist in enumerate(
            obj.media_mediaartist.exclude(artist__isnull=True).select_related(
                "artist",
            )[1:],
            1,
        ):
            yield {
                "name": media_artist.artist.name,
                "ct": media_artist.artist.get_ct(),
                "uuid": str(media_artist.artist.uuid),
                "join_phrase": media_artist.join_phrase,
                "position": position,
            }

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            "uuid",
            "isrc",
            "updated",
            #
            "type",
            "name",
            "duration",
            "release",
            "artists",
            "tags",
            "relations",
        ]


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:artist-detail",
        lookup_field="uuid",
    )

    ct = serializers.CharField(source="get_ct")

    country_code = serializers.CharField(source="country.iso2_code")
    description = serializers.CharField(source="biography")
    image = ImageSerializer(source="main_image")
    tags = TagSerializer(many=True)
    relations = RelationSerializer(many=True)

    date_start = ApproximateDateSerializer()
    date_end = ApproximateDateSerializer()

    class Meta:
        model = Artist
        fields = [
            "url",
            "ct",
            "uuid",
            "updated",
            #
            "type",
            "name",
            "country_code",
            "date_start",
            "date_end",
            "description",
            "image",
            "tags",
            "relations",
        ]


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:release-detail",
        lookup_field="uuid",
    )

    ct = serializers.CharField(source="get_ct")

    type = serializers.CharField(source="releasetype")
    description = serializers.CharField()
    image = ImageSerializer(source="main_image")
    tags = TagSerializer(many=True)
    relations = RelationSerializer(many=True)

    releasedate = ApproximateDateSerializer()

    class Meta:
        model = Release
        fields = [
            "url",
            "ct",
            "uuid",
            "updated",
            #
            "type",
            "name",
            "releasedate",
            "description",
            "image",
            "tags",
            "relations",
        ]


class PlaylistMediaSerializer(serializers.ModelSerializer):

    ct = serializers.CharField(source="get_ct")
    duration = serializers.FloatField(source="master_duration")

    class Meta:
        model = Media
        fields = [
            "ct",
            "uuid",
            "name",
            "duration",
        ]


class PlaylistItemsSerializer(serializers.ModelSerializer):
    # item = PlaylistItemSerializer(read_only=True)

    content = serializers.SerializerMethodField()

    def get_content(self, obj, **kwargs):
        if isinstance(obj.item.content_object, Media):
            serializer = PlaylistMediaSerializer(
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
            "content",
            "position",
            "cue_in",
            "cue_out",
            "fade_in",
            "fade_out",
            "fade_cross",
        ]


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:playlist-detail",
        lookup_field="uuid",
    )

    ct = serializers.CharField(source="get_ct")

    image = ImageSerializer(source="main_image")

    items = PlaylistItemsSerializer(source="playlist_items", many=True)
    tags = TagSerializer(many=True)
    series = serializers.SerializerMethodField()
    editor = serializers.SerializerMethodField()

    def get_series(self, obj, **kwargs):
        if obj.series:
            return {
                "name": obj.series.name,
                "ct": obj.series.get_ct(),
                "uuid": str(obj.series.uuid),
                "episode": obj.series_number,
            }
        return None

    def get_editor(self, obj, **kwargs):
        if not (obj.user and getattr(obj.user, "profile")):
            return None
        profile = obj.user.profile
        return {
            "name": profile.name,
            "ct": profile.get_ct(),
            "uuid": str(profile.uuid),
        }

    class Meta:
        model = Playlist
        fields = [
            "url",
            "ct",
            "uuid",
            "updated",
            #
            "name",
            "type",
            "image",
            "items",
            "series",
            "editor",
            "tags",
        ]


class AccountSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:user-detail",
        lookup_field="id",
    )

    gender = serializers.SerializerMethodField()
    birth_date = serializers.DateField(source='profile.birth_date')
    phone_mobile = serializers.CharField(source='profile.mobile')
    phone_landline = serializers.CharField(source='profile.phone')
    address = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "date_joined",
            "last_login",
            "gender",
            "first_name",
            "last_name",
            "username",
            "email",
            "birth_date",
            "phone_mobile",
            "phone_landline",
            "address",
        ]

    def get_gender(self, obj):
        if not obj.profile:
            return None
        try:
            return obj.profile.get_gender_display().lower()
        except AttributeError:
            return None

    def get_address(self, obj):
        if not obj.profile:
            return {}
        return {
            'line_1': obj.profile.address1 or None,
            'line_2': obj.profile.address2 or None,
            'city': obj.profile.city or None,
            'postal_code': obj.profile.zip or None,
            'country': obj.profile.country.iso2_code if obj.profile.country else None,
        }


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:profile-detail",
        lookup_field="uuid",
    )

    ct = serializers.CharField(source="get_ct")

    description = serializers.CharField()
    image = ImageSerializer(source="main_image")
    tags = TagSerializer(many=True)
    links = RelationSerializer(many=True, source="link_set")

    class Meta:
        model = Profile
        fields = [
            "url",
            "ct",
            "uuid",
            "updated",
            #
            "name",
            "description",
            "image",
            "tags",
            "links",
        ]


class EmissionSerializer(serializers.ModelSerializer):

    ct = serializers.CharField(source="get_ct")
    co = serializers.SerializerMethodField(source="content_object")

    def get_co(self, obj):
        co = obj.content_object
        if not co:
            return None
        return {
            "ct": co.get_ct(),
            "uuid": str(co.uuid),
            "name": co.name,
        }

    class Meta:
        model = Emission
        fields = [
            "ct",
            "uuid",
            "updated",
            "time_start",
            "time_end",
            "duration",
            "co",
        ]


class VoteSerializer(serializers.ModelSerializer):

    ct = serializers.CharField(source="get_ct")
    co = serializers.SerializerMethodField(source="content_object")
    user = serializers.CharField(source="user.email")
    value = serializers.IntegerField(source="vote")

    def get_co(self, obj):
        co = obj.content_object
        if not co or not hasattr(co, "get_ct"):
            return None
        return {
            "ct": co.get_ct(),
            "uuid": str(co.uuid),
        }

    class Meta:
        model = Vote
        fields = [
            "ct",
            "uuid",
            "user",
            "value",
            "co",
        ]
