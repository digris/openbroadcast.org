# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from rest_framework import serializers
from alibrary.models import Artist, Relation
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


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:obr-sync:artist-detail",
        lookup_field="uuid",
    )

    ct = serializers.CharField(source="get_ct")

    # detail_url = serializers.URLField(source="get_absolute_url")

    description = serializers.CharField(source="biography")
    image = ImageSerializer(source="main_image")
    tags = TagSerializer(many=True)
    relations = RelationSerializer(many=True)

    date_start = ApproximateDateSerializer()
    date_end = ApproximateDateSerializer()

    # image = serializers.SerializerMethodField()
    #
    # def get_image(self, obj):
    #     try:
    #         return SITE_URL + obj.main_image.url
    #     except ValueError:
    #         return None

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
