# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ArtistSerializer, MediaSerializer, PlaylistSerializer
from ..models import Artist, Media, Playlist



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


playlist_list = PlaylistViewSet.as_view({
    'get': 'list',
})
playlist_detail = PlaylistViewSet.as_view({
    'get': 'retrieve',
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
