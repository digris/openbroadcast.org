# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from . import serializers
from alibrary.models import Media, Artist, Release, Playlist


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Media.objects.all().order_by("-updated")
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


class ArtistViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Artist.objects.all().order_by("-updated")
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
