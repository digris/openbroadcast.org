# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import PreflightCheckSerializer
from ..models import PreflightCheck





class PreflightCheckViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = PreflightCheck.objects.all()
    serializer_class = PreflightCheckSerializer
    # lookup_field = 'media__uuid'

    def get_object(self):
        obj = get_object_or_404(PreflightCheck, media__uuid=self.kwargs.get('uuid'))
        return obj

    def perform_update(self, serializer):
        serializer.save()


preflight_check_detail = PreflightCheckViewSet.as_view({
    'get': 'retrieve',
    'patch': 'update',
})
