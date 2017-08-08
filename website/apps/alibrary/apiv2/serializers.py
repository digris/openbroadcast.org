# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy

from rest_framework import serializers
from ..models import (
    Artist, Media, Playlist, PlaylistItem, PlaylistItemPlaylist
)


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:artist-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = Artist
        depth = 1
        fields = [
            'url',
            'name',
        ]



class MediaSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:media-detail',
        lookup_field='uuid'
    )

    artist = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:artist-detail',
        lookup_field='uuid'
    )
    artist_display = serializers.CharField(source='get_artist_display')



    stream_uri = serializers.SerializerMethodField()
    def get_stream_uri(self, obj, **kwargs):
        stream_uri = {
            'uri': reverse_lazy('mediaasset-format', kwargs={
                'media_uuid': obj.uuid,
                'quality': 'default',
                'encoding': 'mp3',
            }),
        }

        return stream_uri



    class Meta:
        model = Media
        depth = 1
        fields = [
            'url',
            'name',
            'master_duration',
            'stream_uri',
            'isrc',
            'artist_display',
            'artist',
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
            #return 'Media: {}'.format(value.pk)
            serializer = MediaSerializer(value, context={'request': self.context['request']})
        elif isinstance(value, Media):
            return 'Jingle: {}'.format(value.pk)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class PlaylistItemSerializer(serializers.ModelSerializer):

    # http://www.django-rest-framework.org/api-guide/relations/#generic-relationships

    content = PlaylistItemField(read_only=True, source='content_object')

    class Meta:
        model = PlaylistItem
        depth = 1
        fields = [
            'content',
        ]


class PlaylistItemPlaylistSerializer(serializers.ModelSerializer):

    #item = PlaylistItemSerializer(read_only=True)

    content = serializers.SerializerMethodField()
    def get_content(self, obj, **kwargs):

        # TODO: implement for `Jingle`
        if isinstance(obj.item.content_object, Media):
            serializer = MediaSerializer(
                instance=Media.objects.get(pk=obj.item.content_object.pk),
                many=False,
                context={'request': self.context['request']}
            )
        elif isinstance(obj.item.content_object, Media):
            serializer = MediaSerializer(
                instance=Media.objects.get(pk=obj.item.content_object.pk),
                many=False,
                context={'request': self.context['request']}
            )
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


    class Meta:
        model = PlaylistItemPlaylist
        depth = 1
        fields = [
            #'item',
            'content',
            'position',
            'cue_in',
            'cue_out',
            'fade_in',
            'fade_out',
            'fade_cross',
        ]


class PlaylistSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:playlist-detail',
        lookup_field='uuid'
    )

    items = PlaylistItemPlaylistSerializer(source='playlistitemplaylist_set', many=True)

    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Playlist
        depth = 1
        fields = [
            'url',
            'name',
            'main_image',
            'tags',
            'mixdown_file',
            'items',
        ]
