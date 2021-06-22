# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from rest_framework import serializers
from alibrary.models import Artist, Media, Release, Relation
from tagging.models import Tag

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
            "updated",
            #
            "type",
            "name",
            "tracknumber",
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
            "date_start",
            "date_end",
            "description",
            "image",
            "tags",
            "relations",
        ]


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:artist-detail",
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
