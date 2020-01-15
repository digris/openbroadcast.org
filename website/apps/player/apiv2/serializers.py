# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import random

# from catalog.models import Media
from django.conf import settings
from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

# from ..models import PlayerItem

from alibrary.models import Media
from alibrary.apiv2.serializers import MediaSerializer, ArtistSerializer

SITE_URL = getattr(settings, "SITE_URL")

log = logging.getLogger(__name__)

# for consistency - player expects list/items
class MediaObjSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:media-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct")

    detail_url = serializers.URLField(source="release.get_absolute_url")

    items = serializers.SerializerMethodField()

    def get_items(self, obj, **kwargs):
        items = []
        serializer = MediaSerializer(obj, context={"request": self.context["request"]})
        items.append({"content": serializer.data})
        return items

    class Meta:
        model = Media
        depth = 1
        fields = ["name", "url", "ct", "uuid", "detail_url", "items"]


class ArtistObjSerializer(ArtistSerializer):

    items = serializers.SerializerMethodField()

    def get_items(self, obj, **kwargs):
        items = []
        for media in obj.get_media()[0:20]:

            serializer = MediaSerializer(
                media, context={"request": self.context["request"]}
            )
            items.append({"content": serializer.data})

        return items

    class Meta(ArtistSerializer.Meta):
        fields = ["url", "ct", "detail_url", "uuid", "name", "image", "items"]


class ProfileObjSerializer(ArtistSerializer):

    items = serializers.SerializerMethodField()

    def get_items(self, obj, **kwargs):
        items = []

        # TODO: highly experimental... play user's recent "likes"
        qs = obj.user.votes.filter(vote__gt=0, content_type_id=104).order_by("-created").prefetch_related(
            "content_object"
        )

        # for media in qs.all()[0:30]:
        for media in [r.content_object for r in qs.all()[0:30]]:

            serializer = MediaSerializer(
                media, context={"request": self.context["request"]}
            )
            items.append({"content": serializer.data})

        return items

    class Meta(ArtistSerializer.Meta):
        fields = ["url", "ct", "detail_url", "uuid", "name", "image", "items"]
