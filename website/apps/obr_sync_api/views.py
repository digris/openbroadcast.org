# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.http import FileResponse
from rest_framework import mixins, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError

from . import serializers
from alibrary.models import Media, Artist, Release, Playlist
from profiles.models import Profile
from abcast.models import Emission


class SyncPermissions(permissions.BasePermission):
    message = "Insufficient permissions"

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False
        return request.user.has_perm("account.view_obr_sync_api")


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Media.objects.all().order_by("-updated")
    permission_classes = (SyncPermissions,)
    serializer_class = serializers.MediaSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        qs = self.queryset.select_related(
            "artist",
            "release",
        )
        return qs

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            uuid=self.kwargs["uuid"],
        )


class MediaMasterDwonloadView(APIView):
    permission_required = "alibrary.download_master"
    permission_classes = (SyncPermissions,)
    raise_exception = True

    def get(self, request, uuid):
        media = get_object_or_404(Media, uuid=uuid)
        filename = "{uuid}.{encoding}".format(
            uuid=media.uuid, encoding=media.master_encoding
        )
        response = FileResponse(open(media.master.path, "rb"))
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)

        return response


class ArtistViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Artist.objects.all().order_by("-updated")
    permission_classes = (SyncPermissions,)
    serializer_class = serializers.ArtistSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        qs = self.queryset.prefetch_related("relations",).select_related(
            "country",
        )
        return qs

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            uuid=self.kwargs["uuid"],
        )


class ReleaseViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Release.objects.all().order_by("-updated")
    permission_classes = (SyncPermissions,)
    serializer_class = serializers.ReleaseSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        qs = self.queryset.prefetch_related("relations",).select_related(
            "release_country",
            "label",
        )
        return qs

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            uuid=self.kwargs["uuid"],
        )


class PlaylistViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Playlist.objects.all().order_by("-updated")
    permission_classes = (SyncPermissions,)
    serializer_class = serializers.PlaylistSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        qs = self.queryset
        return qs

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            uuid=self.kwargs["uuid"],
        )


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all().order_by("-updated")
    permission_classes = (SyncPermissions,)
    serializer_class = serializers.ProfileSerializer
    lookup_field = "uuid"

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            uuid=self.kwargs["uuid"],
        )


class EmissionFilter(filters.FilterSet):
    # query:
    # /api/v2/obr-sync/emissions/?time_start_0=2019-06-03+06:00&time_start_1=2019-06-04+06:00
    time_start = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Emission
        fields = ["time_start"]


class EmissionViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Emission.objects.all().order_by("-updated")
    permission_classes = (SyncPermissions,)
    serializer_class = serializers.EmissionSerializer
    filter_class = EmissionFilter
    # lookup_field = "uuid"

    def get_queryset(self):
        qs = self.queryset
        return qs

    # def get_object(self):
    #     return get_object_or_404(
    #         self.get_queryset(),
    #         uuid=self.kwargs["uuid"],
    #     )
