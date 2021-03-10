# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.utils.cache import patch_response_headers

from rest_framework import mixins
from rest_framework import viewsets

# from rest_framework.decorators import action
# TODO: `action` not implemented in used DRF version (3.6.4) - refactor to 'actions' once
# it is possible to upgrade DRF.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from .serializers import (
    ArtistSerializer,
    LabelSerializer,
    ReleaseSerializer,
    MediaSerializer,
    PlaylistSerializer,
)
from ..models import Artist, Label, Release, Media, Playlist

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
        # items_to_collect = self.request.data.get("items_to_collect", [])
        items_to_collect = self.request.data.get("itemsToCollect", [])

        print("add_items_to_playlist", items_to_collect, playlist)

        add_items_to_playlist(items_to_collect, playlist)

        playlist.save()

        serializer = PlaylistSerializer(playlist, context={"request": request})
        return Response(serializer.data)

    def create(self, request, uuid=None, *args, **kwargs):

        name = self.request.data.get("name")
        type = self.request.data.get("type")
        # items_to_collect = self.request.data.get("items_to_collect", [])
        items_to_collect = self.request.data.get("itemsToCollect", [])

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


# artist_list = ArtistViewSet.as_view({"get": "list"})
# artist_detail = ArtistViewSet.as_view({"get": "retrieve"})


class LabelViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Label.objects.all().order_by("-created")
    serializer_class = LabelSerializer
    lookup_field = "uuid"


# label_list = LabelViewSet.as_view({"get": "list"})
# label_detail = LabelViewSet.as_view({"get": "retrieve"})


class ReleaseViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    lookup_field = "uuid"
    queryset = Release.objects.all().order_by("-created")
    serializer_class = ReleaseSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = [
        "uuid"
    ]  # TODO: filter_fields is depreciated, newer version uses filterset_fields


# release_list = ReleaseViewSet.as_view({"get": "list"})
# release_detail = ReleaseViewSet.as_view({"get": "retrieve"})


class MediaViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Media.objects.all().order_by("-created")
    serializer_class = MediaSerializer
    lookup_field = "uuid"


# media_list = MediaViewSet.as_view({"get": "list"})
# media_detail = MediaViewSet.as_view({"get": "retrieve"})


class MediaDownloadView(APIView):
    permission_required = "alibrary.download_master"
    raise_exception = True

    version = None

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated():
    #         raise PermissionDenied("no anonymous users allowed")
    #     return super(MediaDownloadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):

        if not self.version == "master":
            raise NotImplementedError("only master version supported at the moment")

        if not request.user.is_authenticated():
            raise PermissionDenied("no anonymous users allowed")

        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied(
                "missing permission: {} for user: {}".format(
                    self.permission_required, request.user
                )
            )

        obj = get_object_or_404(Media, uuid=kwargs.get("uuid"))
        filename = "{uuid}.{encoding}".format(
            uuid=obj.uuid, encoding=obj.master_encoding
        )

        response = FileResponse(open(obj.master.path, "rb"))
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)

        return response


media_download_master = MediaDownloadView.as_view(version="master")


# utility views
class ObjectMergeView(APIView):
    permission_required = "alibrary.merge_media"

    def get(self, request, **kwargs):
        return Response()

    def post(self, request, **kwargs):

        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied(
                "missing permission: {} for user: {}".format(
                    self.permission_required, request.user
                )
            )

        from ..util.merge import merge

        def get_obj_by_key(key):
            ct, uuid = key.split(":")
            model = apps.get_model(*ct.split("."))
            obj = model.objects.get(uuid=uuid)
            return obj

        master = get_obj_by_key(request.data.get("master"))
        slaves = [get_obj_by_key(k) for k in request.data.get("slaves")]

        master = merge(master, slaves)

        return Response()


class ObjectReassignView(APIView):
    permission_required = "alibrary.reassign_media"

    def get(self, request, **kwargs):
        return Response()

    def post(self, request, **kwargs):

        if not request.user.has_perm(self.permission_required):
            raise PermissionDenied(
                "missing permission: {} for user: {}".format(
                    self.permission_required, request.user
                )
            )

        from ..util.reassign import reassign_media

        def get_obj_by_key(key):
            ct, uuid = key.split(":")
            model = apps.get_model(*ct.split("."))
            obj = model.objects.get(uuid=uuid)
            return obj

        print(request.data)

        target = request.data.get("target")
        if not target.get("create"):
            release = get_obj_by_key(target.get("key"))
        else:
            release = Release.objects.create(name=target.get("name"))

        media_qs = [get_obj_by_key(k) for k in request.data.get("objects")]

        obj = reassign_media(release, media_qs)

        return Response({"location": obj.get_absolute_url()})


class MediaAppearances(APIView):
    def get(self, request, uuid):

        cache_key = "media-appearances-{}".format(uuid)
        data = cache.get(cache_key)
        if not data:
            obj = get_object_or_404(Media, uuid=uuid)

            qs = obj.get_appearances()

            public_count = qs.filter(type=Playlist.TYPE_PLAYLIST).count()
            broadcast_count = qs.filter(type=Playlist.TYPE_BROADCAST).count()

            # unpublished broaadcasts: count "private" playlists that have a target duration set.
            # so we assume they will become broadcastable sooner or later...
            broadcast_unpublished_count = qs.filter(
                type=Playlist.TYPE_BASKET,
                target_duration__gt=0,
            ).count()

            # if channel_uuid:
            #     qs = qs.filter(channel__uuid=channel_uuid)

            data = {
                "public": public_count,
                "broadcast": broadcast_count,
                "broadcast_unpublished": broadcast_unpublished_count,
            }

            cache.set(cache_key, data, 60 * 60)

        response = Response(data)
        patch_response_headers(response, cache_timeout=60 * 60)

        return response
