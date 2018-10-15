# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# import logging
# import random
# #from catalog.models import Media
# from django.conf import settings
# from rest_framework import serializers
# from easy_thumbnails.templatetags.thumbnail import thumbnail_url
#
# #from ..models import PlayerItem
#
# from alibrary.models import Release
#
# SITE_URL = getattr(settings, 'SITE_URL')
#
# log = logging.getLogger(__name__)
#
#
#
#
# class ImageSerializer(serializers.ImageField):
#     def to_representation(self, instance):
#         if not instance:
#             return
#         return '{}{}'.format(SITE_URL, thumbnail_url(instance, 'thumbnail_240'))
#
#
#
# class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
#     url = serializers.HyperlinkedIdentityField(
#         read_only=True,
#         view_name='api:release-detail',
#         lookup_field='uuid'
#     )
#
#     image = ImageSerializer(
#         source='main_image',
#     )
#
#     # name = serializers.CharField(
#     #     source='content_object.name',
#     # )
#     # image = ImageSerializer(
#     #     source='content_object.key_image',
#     #     read_only=True,
#     # )
#     #
#     # items = PlayItemSerializer(
#     #     source='get_items',
#     #     many=True
#     # )
#
#     class Meta:
#         model = Release
#         depth = 1
#         fields = [
#             'url',
#             'name',
#             'uuid',
#             'image',
#         ]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # class ImageSerializer(serializers.ImageField):
# #
# #     def to_representation(self, instance):
# #         if not instance:
# #             return
# #         return '{}{}'.format(SITE_URL, instance.file.crop['580x580'].url)
# #
# #
# # class MediaSerializer(serializers.HyperlinkedModelSerializer):
# #     url = serializers.HyperlinkedIdentityField(
# #         view_name='api:catalog-media-detail',
# #         lookup_field='uuid'
# #     )
# #
# #     duration = serializers.SerializerMethodField()
# #
# #     def get_duration(self, obj, **kwargs):
# #         return obj.master.duration
# #
# #     waveform = serializers.SerializerMethodField()
# #
# #     def get_waveform(self, obj, **kwargs):
# #         # TODO: implement waveform API endpoint
# #         # return []
# #         if hasattr(obj, 'waveform') and obj.waveform.data:
# #             return obj.waveform.data
# #         # add dummy data in case of missing waveform
# #         return [10, 6, 10] + [random.randint(0, 8) for i in range(0, 196)] + [10]
# #
# #     artist_display = serializers.CharField(
# #         source='get_artist_display',
# #         read_only=True
# #     )
# #
# #     release_display = serializers.SerializerMethodField()
# #
# #     def get_release_display(self, obj, **kwargs):
# #         if not obj.release:
# #             return
# #         return obj.release.name
# #
# #     label_display = serializers.SerializerMethodField()
# #
# #     def get_label_display(self, obj, **kwargs):
# #         if not obj.release or not obj.release.label:
# #             return
# #         return obj.release.label.name
# #
# #     stream_url = serializers.SerializerMethodField()
# #
# #     def get_stream_url(self, obj, **kwargs):
# #
# #         # TODO: propperly serialize assets
# #         stream_url = obj.master.file.url.replace('media/media_server/', '')
# #         return '{}{}'.format(MEDIA_SERVER_URL.rstrip('/'), stream_url)
# #
# #     ###################################################################
# #     # internally related detail urls
# #     ###################################################################
# #     detail_url = serializers.SerializerMethodField()
# #
# #     def get_detail_url(self, obj, **kwargs):
# #         if not obj.release:
# #             return None
# #         _rel = obj.release.get_absolute_url()
# #         if not _rel:
# #             return None
# #         return '{}{}'.format(SITE_URL, _rel)
# #
# #     release_detail_url = serializers.SerializerMethodField()
# #
# #     def get_release_detail_url(self, obj, **kwargs):
# #         if not obj.release:
# #             return None
# #
# #         _rel = obj.release.get_absolute_url()
# #         if not _rel:
# #             return None
# #         return '{}{}'.format(SITE_URL, _rel)
# #
# #     artist_detail_url = serializers.SerializerMethodField()
# #
# #     def get_artist_detail_url(self, obj, **kwargs):
# #         if not obj.artists.exists():
# #             return None
# #
# #         _rel = obj.artists.first().get_absolute_url()
# #         if not _rel:
# #             return None
# #         return '{}{}'.format(SITE_URL, _rel)
# #
# #     class Meta:
# #         model = Media
# #         depth = 1
# #         fields = [
# #             'uuid',
# #             'url',
# #             'name',
# #             'tracknumber',
# #             'duration',
# #             'stream_url',
# #             'waveform',
# #             # 'assets',
# #             # 'image',
# #             'detail_url',
# #             'release_detail_url',
# #             'artist_detail_url',
# #             'artist_display',
# #             'release_display',
# #             'label_display',
# #         ]
# #
# #
# # class PlayItemSerializer(serializers.Serializer):
# #     position = serializers.IntegerField()
# #     image = ImageSerializer(
# #         read_only=True,
# #     )
# #     media = MediaSerializer(
# #         many=False,
# #         read_only=False,
# #     )
# #
# #     class Meta:
# #         depth = 1
# #         fields = [
# #             'uuid',
# #             'image',
# #             'position'
# #             'media'
# #         ]
#
#
