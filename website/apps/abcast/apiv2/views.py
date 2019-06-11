# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_flex_fields import FlexFieldsModelViewSet
from .serializers import EmissionSerializer, EmissionHistorySerializer
from ..models import Emission

log = logging.getLogger(__name__)


class EmissionFilter(filters.FilterSet):
    # query:
    # /api/v2/abcast/emission/?time_start_0=2019-06-03+06:00&time_start_1=2019-06-04+06:00
    time_start = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Emission
        fields = ['time_start']


class EmissionViewSet(FlexFieldsModelViewSet):

    queryset = Emission.objects.all().order_by('-time_start')
    lookup_field = 'uuid'
    serializer_class = EmissionSerializer
    filter_class = EmissionFilter

    def get_queryset(self):
        qs = super(EmissionViewSet, self).get_queryset()
        qs = qs.prefetch_related('content_object')
        return qs


emission_list = EmissionViewSet.as_view({
    'get': 'list',
})

emission_detail = EmissionViewSet.as_view({
    'get': 'retrieve',
})


class EmissionHistory(APIView):

    def get_object(self):
        obj_ct = self.kwargs.get('obj_ct')
        obj_uuid = self.kwargs.get('obj_uuid')

        return get_object_or_404(apps.get_model(*obj_ct.split(".")), uuid=obj_uuid)

    def get(self, request, obj_ct, obj_uuid):

        obj = self.get_object()
        serializer = EmissionHistorySerializer(instance=obj.emissions.order_by('-time_start'), many=True)

        return Response(serializer.data)

emission_history = EmissionHistory.as_view()
