# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from ..models import (
    Media, Playlist, PlaylistItem
)

class MediaSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:media-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = Media
        depth = 1
        fields = [
            'url',
        ]




# class PlaylistItemSerializer(serializers.HyperlinkedModelSerializer):
#
#     url = serializers.HyperlinkedIdentityField(
#         view_name='api:playlist-item-detail',
#         lookup_field='uuid'
#     )
#
#     class Meta:
#         model = PlaylistItem
#         depth = 1
#         fields = [
#             'url',
#         ]






class PlaylistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:playlist-detail',
        lookup_field='uuid'
    )

    # items = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='playlist-item-detail'
    # )

    class Meta:
        model = Playlist
        depth = 1
        fields = [
            'url',
            'name',
            'main_image',
            'd_tags',
            'mixdown_file',
            #'items',
        ]
