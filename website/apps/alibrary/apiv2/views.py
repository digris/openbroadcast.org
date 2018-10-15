# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ArtistSerializer, ReleaseSerializer, MediaSerializer, PlaylistSerializer
from ..models import Artist, Release, Media, Playlist

log = logging.getLogger(__name__)

class PlaylistViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Playlist.objects.all().order_by('-created')
    serializer_class = PlaylistSerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        queryset = Playlist.objects.all().order_by('-created')
        serializer = PlaylistSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response({
            'results': serializer.data
        })


    def add_items(self, request, uuid=None, *args, **kwargs):
        """
        initialize scanning & redirect to detail view
        """
        playlist = self.get_object()
        print('***********************')
        print(self.request.data)

        items_to_collect = self.request.data.get('items_to_collect', [])

        for item in items_to_collect:

            obj_ct = item['content'].get('ct')
            obj_uuid = item['content'].get('uuid')

            log.debug('item requested to collect: {} {}'.format(obj_ct, obj_uuid))

            try:
                obj = apps.get_model(*obj_ct.split('.')).objects.get(uuid=obj_uuid)

                cue_and_fade = {
                    'fade_in': item.get('fade_in', 0),
                    'fade_out': item.get('fade_out', 0),
                    'cue_in': item.get('cue_in', 0),
                    'cue_out': item.get('cue_out', 0),
                }

                playlist.add_item(item=obj, cue_and_fade=cue_and_fade, commit=False)

            except ObjectDoesNotExist:
                raise Http404

        playlist.save()

        # import time
        # time.sleep(2.0)

        serializer = PlaylistSerializer(
            playlist,
            context={'request': request}
        )
        return Response(serializer.data)


    def create(self, request, uuid=None, *args, **kwargs):
        """
        initialize scanning & redirect to detail view
        """
        playlist = Playlist(
            name=self.request.data.get('name'),
            user=request.user,
            type='basket'
        )

        playlist.save()

        serializer = PlaylistSerializer(
            playlist,
            context={'request': request}
        )

        return Response(serializer.data)



playlist_list = PlaylistViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
playlist_detail = PlaylistViewSet.as_view({
    'get': 'retrieve',
    'put': 'add_items',
})




class ArtistViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Artist.objects.all().order_by('-created')
    serializer_class = ArtistSerializer
    lookup_field = 'uuid'



artist_list = ArtistViewSet.as_view({
    'get': 'list',
})
artist_detail = ArtistViewSet.as_view({
    'get': 'retrieve',
})


class ReleaseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Release.objects.all().order_by('-created')
    serializer_class = ReleaseSerializer
    lookup_field = 'uuid'



release_list = ReleaseViewSet.as_view({
    'get': 'list',
})
release_detail = ReleaseViewSet.as_view({
    'get': 'retrieve',
})



class MediaViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Media.objects.all().order_by('-created')
    serializer_class = MediaSerializer
    lookup_field = 'uuid'



media_list = MediaViewSet.as_view({
    'get': 'list',
})
media_detail = MediaViewSet.as_view({
    'get': 'retrieve',
})
