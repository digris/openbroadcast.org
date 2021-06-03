# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from . import serializers
from alibrary.models import Artist


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
