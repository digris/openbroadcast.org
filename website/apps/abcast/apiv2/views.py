# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

from django.apps import apps
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .serializers import EmissionSerializer, EmissionHistorySerializer
from ..models import Emission
from ..utils.scheduler import check_slot_availability

log = logging.getLogger(__name__)


class EmissionPermission(permissions.BasePermission):
    message = "insufficient permission"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated() and request.user.has_perm('abcast.schedule_emission')


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
    permission_classes = (EmissionPermission,)
    serializer_class = EmissionSerializer
    filter_class = EmissionFilter

    def get_queryset(self):
        qs = super(EmissionViewSet, self).get_queryset()
        qs = qs.prefetch_related('content_object')
        return qs

    # def dispatch(self, request, *args, **kwargs):
    #
    #     if not request.method.upper() == 'GET':
    #
    #         if not request.user.is_authenticated():
    #             raise Exception('not authenticated')
    #
    #         if not request.user.has_perms('alibrary.schedule_playlist'):
    #             raise Exception('no permission')
    #
    #     return super(EmissionViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        obj_ct = request.data.get('obj_ct')
        obj_uuid = request.data.get('obj_uuid')
        time_start = datetime.datetime.strptime(request.data.get('time_start'), '%Y-%m-%d %H:%M')
        color = request.data.get('color', 0)

        # raise ValidationError('you cannot schedule in the past...')
        content_object = get_object_or_404(
            apps.get_model(*obj_ct.split(".")),
            uuid=obj_uuid
        )

        available, message = check_slot_availability(
            time_start=time_start,
            time_end=time_start + datetime.timedelta(milliseconds=content_object.duration)
        )

        if not available:
            raise ValidationError(message)

        emission = Emission(
            content_object=content_object,
            time_start=time_start,
            user=request.user,
            color=color,
        )

        emission.save()
        serializer = EmissionSerializer(emission, context={'request': request})

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=False)
        # self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):

        emission = self.get_object()

        if request.data.get('time_start'):
            time_start = datetime.datetime.strptime(request.data.get('time_start'), '%Y-%m-%d %H:%M')
            available, message = check_slot_availability(
                time_start=time_start,
                time_end=time_start + datetime.timedelta(milliseconds=emission.content_object.duration),
                excluded_emission=emission
            )

            if not available:
                raise ValidationError(message)

        return super(EmissionViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.has_lock:
            raise ValidationError('Emission is locked.')

        return super(EmissionViewSet, self).destroy(request, *args, **kwargs)

emission_list = EmissionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

emission_detail = EmissionViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
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
