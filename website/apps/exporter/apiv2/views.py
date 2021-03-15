# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from rest_framework import mixins
from rest_framework import viewsets

# from rest_framework.decorators import action # `action` not implemented in used DRF version (3.6.4)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from .serializers import ExportSerializer
from ..models import Export, ExportItem

log = logging.getLogger(__name__)


class ExportViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Export.objects.all().order_by("-created")
    serializer_class = ExportSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        export = serializer.save(user=self.request.user)

        _objects = self.request.data.get("objects", [])

        def get_obj_by_key(key):
            ct, uuid = key.split(":")
            model = apps.get_model(*ct.split("."))
            obj = model.objects.get(uuid=uuid)
            return obj

        objects = [get_obj_by_key(k) for k in _objects]

        for obj in objects:
            e = ExportItem(
                content_object=obj,
                export_session=export,
            )
            e.save()

        export.status = 2
        export.save()

        # print('data', self.request.data)
        # print('_objects', _objects)
        # print('objects', objects)
        # print('export', export)
