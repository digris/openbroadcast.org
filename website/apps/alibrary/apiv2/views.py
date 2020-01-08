# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db.models import Q

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_flex_fields import FlexFieldsModelViewSet

from .serializers import (
    ArtistSerializer,
    ReleaseSerializer,
    MediaSerializer,
    PlaylistSerializer,
)
from ..models import Artist, Release, Media, Playlist

log = logging.getLogger(__name__)


# TODO: find a better place...
def add_items_to_playlist(items, playlist):

    for item in items:

        obj_ct = item["content"].get("ct")
        obj_uuid = item["content"].get("uuid")

        log.debug("item requested to collect: {} {}".format(obj_ct, obj_uuid))
        obj = apps.get_model(*obj_ct.split(".")).objects.get(uuid=obj_uuid)

        cue_and_fade = {
            "fade_in": item.get("fade_in", 0),
            "fade_out": item.get("fade_out", 0),
            "cue_in": item.get("cue_in", 0),
            "cue_out": item.get("cue_out", 0),
        }

        playlist.add_item(item=obj, cue_and_fade=cue_and_fade, commit=False)


class PlaylistViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Playlist.objects.all().order_by("-created")
    serializer_class = PlaylistSerializer
    lookup_field = "uuid"

    def list(self, request, *args, **kwargs):
        queryset = Playlist.objects.all().order_by("-created")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list_collect(self, request, *args, **kwargs):
        """
        list current user 'collectable' playlists
        (private & public playlist)
        """

        q = request.GET.get("q", "").strip()

        queryset = Playlist.objects.filter(
            user=request.user, type__in=["basket", "playlist"]
        ).order_by("-updated")

        if q != "":
            queryset = queryset.filter(
                Q(name__istartswith=q) | Q(series__name__istartswith=q)
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        # serializer = PlaylistSerializer(
        #     queryset,
        #     many=True,
        #     context={'request': request}
        # )
        # return Response({
        #     'results': serializer.data
        # })

    def add_items(self, request, uuid=None, *args, **kwargs):

        playlist = self.get_object()
        items_to_collect = self.request.data.get("items_to_collect", [])

        add_items_to_playlist(items_to_collect, playlist)

        playlist.save()

        serializer = PlaylistSerializer(playlist, context={"request": request})
        return Response(serializer.data)

    def create(self, request, uuid=None, *args, **kwargs):

        name = self.request.data.get("name")
        type = self.request.data.get("type")
        items_to_collect = self.request.data.get("items_to_collect", [])

        playlist = Playlist(name=name, user=request.user, type=type)

        playlist.save()

        add_items_to_playlist(items_to_collect, playlist)

        playlist.save()

        serializer = PlaylistSerializer(playlist, context={"request": request})

        return Response(serializer.data)


playlist_list = PlaylistViewSet.as_view({"get": "list", "post": "create"})
playlist_list_collect = PlaylistViewSet.as_view({"get": "list_collect"})
playlist_detail = PlaylistViewSet.as_view({"get": "retrieve", "put": "add_items"})


class ArtistViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Artist.objects.all().order_by("-created")
    serializer_class = ArtistSerializer
    lookup_field = "uuid"


artist_list = ArtistViewSet.as_view({"get": "list"})
artist_detail = ArtistViewSet.as_view({"get": "retrieve"})


class ReleaseViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Release.objects.all().order_by("-created")
    serializer_class = ReleaseSerializer
    lookup_field = "uuid"


release_list = ReleaseViewSet.as_view({"get": "list"})
release_detail = ReleaseViewSet.as_view({"get": "retrieve"})


class MediaViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Media.objects.all().order_by("-created")
    serializer_class = MediaSerializer
    lookup_field = "uuid"


media_list = MediaViewSet.as_view({"get": "list"})
media_detail = MediaViewSet.as_view({"get": "retrieve"})
