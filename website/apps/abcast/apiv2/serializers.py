# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from api_extra.serializers import ImageSerializer, AbsoluteUURLField

from alibrary.models import Playlist
from alibrary.apiv2.serializers import PlaylistSerializer
from profiles.apiv2.serializers import ProfileSerializer
from ..models import Emission

SITE_URL = getattr(settings, 'SITE_URL')


class EmissionContentObjectSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """

        print('****************')
        print(obj)
        filter_fields = self.context['request'].GET.get('fields', '').split(',')
        print(filter_fields)

        co_filter_fields = [f.lstrip('co.') for f in filter_fields if f.startswith('co.')]

        print(co_filter_fields)
        print('---')

        if isinstance(obj, Playlist):

            fields = [
                'url',
                'uuid',
                'mixdown_file',
            ]
            if 'co.items' in filter_fields:
                fields.append('items')

            serializer = PlaylistSerializer(obj, context=self.context, fields=co_filter_fields)
        else:
            raise Exception('Unexpected type of content object')

        return serializer.data



class EmissionSerializer(FlexFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:emission-detail',
        lookup_field='uuid'
    )

    ct = serializers.CharField(source='get_ct')
    co_ct = serializers.CharField(
        source='content_object.get_ct'
    )
    co_uuid = serializers.UUIDField(
        source='content_object.uuid'
    )
    co = serializers.SerializerMethodField(
        source='content_object'
    )

    series = serializers.CharField(
        source='content_object.series_display',
    )
    image = ImageSerializer(
        source='content_object.main_image',
    )

    detail_url = AbsoluteUURLField(source='get_absolute_url')

    user = serializers.SerializerMethodField(
        source='user'
    )

    is_playing = serializers.BooleanField()
    is_history = serializers.BooleanField()

    def get_co(self, obj):
        return EmissionContentObjectSerializer(obj.content_object, context=self.context).data

    def get_user(self, obj):
        if not (obj.user and getattr(obj.user, 'profile')):
            return
        return ProfileSerializer(obj.user.profile, context=self.context).data


    class Meta:
        model = Emission
        depth = 2
        fields = [
            'url',
            'ct',
            'uuid',
            'user',
            'co_ct',
            'co_uuid',
            'co',
            'detail_url',
            'is_playing',
            'is_history',
            'name',
            'time_start',
            'time_end',
            'duration',
            'series',
            'image',
        ]

    # expandable_fields = {
    #     'co': (EmissionContentObjectSerializer, {'source': 'content_object'})
    # }
