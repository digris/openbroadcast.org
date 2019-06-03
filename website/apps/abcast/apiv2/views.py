# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db.models import Q

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_flex_fields import FlexFieldsModelViewSet

from .serializers import EmissionSerializer
from ..models import Emission

log = logging.getLogger(__name__)


class EmissionFilter(filters.FilterSet):
    # query:
    # /api/v2/abcast/emission/?time_start_0=2019-06-03+06:00&time_start_1=2019-06-04+06:00
    time_start = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Emission
        fields = ['time_start']
        # fields = {
        #     'name': ['startswith'],
        #     'time_start': ['startswith'],
        # }
        # together = ['first_name', 'last_name']


class EmissionViewSet(FlexFieldsModelViewSet):

    queryset = Emission.objects.all().order_by('-time_start')
    lookup_field = 'uuid'
    serializer_class = EmissionSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('time_start', 'time_end')
    filter_class = EmissionFilter

    def get_queryset(self):
        qs = super(EmissionViewSet, self).get_queryset()
        qs = qs.prefetch_related('content_object')
        return qs

    # def list(self, request, *args, **kwargs):
    #     qs = self.get_queryset()
    #
    #     page = self.paginate_queryset(qs)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(qs, many=True)
    #     return Response(serializer.data)


emission_list = EmissionViewSet.as_view({
    'get': 'list',
})

emission_detail = EmissionViewSet.as_view({
    'get': 'retrieve',
})
