# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from rest_framework import serializers
from api_extra.serializers import ImageSerializer, AbsoluteUURLField
from ..models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:profile-detail", lookup_field="uuid"
    )
    user_id = serializers.IntegerField(source="user.id")
    ct = serializers.CharField(source="get_ct")
    detail_url = AbsoluteUURLField(source="get_absolute_url")
    display_name = serializers.CharField(source="get_display_name")
    full_name = serializers.CharField(source="get_display_name")
    image = ImageSerializer(source="main_image")
    groups = serializers.StringRelatedField(
        source="user.groups", many=True, read_only=True
    )
    tags = serializers.StringRelatedField(many=True, read_only=True)
    country = serializers.CharField(source="country.iso2_code")

    class Meta:
        model = Profile
        depth = 1
        fields = [
            "url",
            "ct",
            "user_id",
            "detail_url",
            "uuid",
            "name",
            "display_name",
            "full_name",
            "image",
            "groups",
            "tags",
            "city",
            "country",
        ]
