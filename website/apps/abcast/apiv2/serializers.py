# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from api_extra.serializers import ImageSerializer, AbsoluteURLField
from alibrary.models import Playlist
from alibrary.apiv2.serializers import PlaylistSerializer
from profiles.apiv2.serializers import ProfileSerializer

from ..models import Emission

SITE_URL = getattr(settings, "SITE_URL")


class EmissionContentObjectSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        filter_fields = self.context["request"].GET.get("fields", "").split(",")
        co_filter_fields = [f[3:] for f in filter_fields if f.startswith("co.")]

        if isinstance(obj, Playlist):
            serializer = PlaylistSerializer(
                obj, context=self.context, fields=co_filter_fields
            )
        else:
            raise Exception("Unexpected type of content object")

        return serializer.data


class EmissionSerializer(FlexFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:emission-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct")
    co_ct = serializers.CharField(source="content_object.get_ct")
    co_uuid = serializers.UUIDField(source="content_object.uuid")
    co = serializers.SerializerMethodField(source="content_object")

    series = serializers.CharField(source="content_object.series_display")
    image = ImageSerializer(source="content_object.main_image")

    detail_url = AbsoluteURLField(source="get_absolute_url")

    user = serializers.SerializerMethodField(source="user")

    is_playing = serializers.BooleanField()
    is_history = serializers.BooleanField()

    def get_co(self, obj):
        if not obj.content_object:
            return
        return EmissionContentObjectSerializer(
            obj.content_object, context=self.context
        ).data

    def get_user(self, obj):
        if not (obj.user and getattr(obj.user, "profile")):
            return
        return ProfileSerializer(obj.user.profile, context=self.context).data

    class Meta:
        model = Emission
        depth = 2
        fields = [
            "url",
            "updated",
            "ct",
            "uuid",
            "user",
            "co_ct",
            "co_uuid",
            "co",
            "detail_url",
            "is_playing",
            "is_history",
            "name",
            "time_start",
            "time_end",
            "duration",
            "series",
            "image",
            "color",
            "has_lock",
        ]


class EmissionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emission
        fields = ["uuid", "time_start", "time_end", "duration"]


class PlayoutScheduleEmissionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()
    duration = serializers.IntegerField()


class PlayoutScheduleMasterSerializer(serializers.Serializer):
    encoding = serializers.CharField(source="master_encoding")
    sha1 = serializers.CharField(source="master_sha1")
    url = AbsoluteURLField(source="master_url")
    filesize = serializers.IntegerField(source="master_filesize")
    # path = serializers.CharField(source="master")


class PlayoutScheduleItemSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()
    fade_in = serializers.IntegerField()
    fade_out = serializers.IntegerField()
    fade_cross = serializers.IntegerField()
    cue_in = serializers.IntegerField()
    cue_out = serializers.IntegerField()
    duration = serializers.IntegerField(source="playout_duration")

    obi_ct = serializers.CharField(source="content_object.get_ct")
    obi_uuid = serializers.UUIDField(source="content_object.uuid")
    obj_name = serializers.CharField(source="content_object.name")
    # obj_master = serializers.CharField(source="content_object.master")
    # obj_master_sha1 = serializers.CharField(source="content_object.master_sha1")
    # obj_master_url = serializers.CharField(source="content_object.master_url")

    emission = PlayoutScheduleEmissionSerializer()
    master = PlayoutScheduleMasterSerializer(source="content_object")


class PlayoutScheduleSerializer(serializers.Serializer):
    """
    flat list of items including absolute timestamps
    """

    def __init__(self, **kwargs):
        super(PlayoutScheduleSerializer, self).__init__(**kwargs)

    count = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()

    def get_count(self, objects):
        return len(objects)

    def get_results(self, objects):
        for content_item in objects:
            yield PlayoutScheduleItemSerializer(content_item).data

        # return [e.uuid for e in emissions]
