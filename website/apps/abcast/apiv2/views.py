# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

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
