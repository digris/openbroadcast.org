# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

from operator import itemgetter
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .serializers import (
    EmissionSerializer,
    EmissionHistorySerializer,
    PlayoutScheduleSerializer,
)
from ..models import Emission, Channel
from ..utils import scheduler

DEFAULT_CHANNEL_ID = 1

log = logging.getLogger(__name__)


class EmissionPermission(permissions.BasePermission):
    message = "insufficient permission"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated() and request.user.has_perm(
            "abcast.schedule_emission"
        )


class EmissionFilter(filters.FilterSet):
    # query:
    # /api/v2/abcast/emission/?time_start_0=2019-06-03+06:00&time_start_1=2019-06-04+06:00
    time_start = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Emission
        fields = ["time_start"]


class EmissionViewSet(FlexFieldsModelViewSet):
    queryset = Emission.objects.all().order_by("-time_start")
    lookup_field = "uuid"
    permission_classes = (EmissionPermission,)
    serializer_class = EmissionSerializer
    filter_class = EmissionFilter

    def get_queryset(self):
        qs = super(EmissionViewSet, self).get_queryset()
        qs = qs.prefetch_related("content_object")
        return qs

    def create(self, request, *args, **kwargs):

        obj_ct = request.data.get("obj_ct")
        obj_uuid = request.data.get("obj_uuid")
        time_start = datetime.datetime.strptime(
            request.data.get("time_start"), "%Y-%m-%d %H:%M"
        )
        color = request.data.get("color", 0)

        # raise ValidationError('you cannot schedule in the past...')
        content_object = get_object_or_404(
            apps.get_model(*obj_ct.split(".")), uuid=obj_uuid
        )

        available, message = scheduler.check_slot_availability(
            time_start=time_start,
            time_end=time_start
            + datetime.timedelta(milliseconds=content_object.duration),
        )

        if not available:
            raise ValidationError(message)

        channel = Channel.objects.filter(pk=DEFAULT_CHANNEL_ID).first()

        emission = Emission(
            content_object=content_object,
            time_start=time_start,
            user=request.user,
            channel=channel,
            color=color,
        )

        emission.save()
        serializer = EmissionSerializer(emission, context={"request": request})

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=False)
        # self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):

        emission = self.get_object()

        if request.data.get("time_start"):
            time_start = datetime.datetime.strptime(
                request.data.get("time_start"), "%Y-%m-%d %H:%M"
            )
            available, message = scheduler.check_slot_availability(
                time_start=time_start,
                time_end=time_start
                + datetime.timedelta(milliseconds=emission.content_object.duration),
                excluded_emission=emission,
            )

            if not available:
                raise ValidationError(message)

        return super(EmissionViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.has_lock:
            raise ValidationError("Emission is locked.")

        return super(EmissionViewSet, self).destroy(request, *args, **kwargs)


emission_list = EmissionViewSet.as_view({"get": "list", "post": "create"})

emission_detail = EmissionViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)


class EmissionHistory(APIView):
    def get_object(self):
        obj_ct = self.kwargs.get("obj_ct")
        obj_uuid = self.kwargs.get("obj_uuid")

        return get_object_or_404(apps.get_model(*obj_ct.split(".")), uuid=obj_uuid)

    def get(self, request, obj_ct, obj_uuid):
        obj = self.get_object()
        serializer = EmissionHistorySerializer(
            instance=obj.emissions.order_by("-time_start"), many=True
        )

        return Response(serializer.data)


emission_history = EmissionHistory.as_view()


class FlattenedSchedule(APIView):
    """
    "flattened" data for channel's schedule:
        ...
        {
            "emission": "/api/v1/abcast/emission/28169/",
            "item": "/api/v1/library/track/95d416f8-6343-448e-8928-953cc127ede6/",
            "time_start": "2019-10-23T11:37:29.279000",
            "time_end": "2019-10-23T11:40:38.529000",
            "verbose_name": "CafiCreme Dda proc"
        },
        ...

    """

    def get(self, request):
        _time_range = request.GET.get("time_range")
        if _time_range:
            time_range = list(map(int, _time_range.split(",")))
        else:
            time_range = (-3600, 3600)

        channel = Channel.objects.get(pk=1)

        schedule = scheduler.get_schedule(
            range_start=abs(time_range[0]), range_end=time_range[1], channel=channel
        )

        return Response({"meta": {"total_count": len(schedule)}, "objects": schedule})


flattened_schedule = FlattenedSchedule.as_view()


class PlayoutSchedule(APIView):

    """
    raw / track-based schedule for playout (pypo)
    # TODO: check implementation in pypo (currently not used, see pypo-ng)
    """

    def get_content_items(self, emissions, time_start, time_end):
        for emission in emissions:
            for content_item in emission.get_content_items():
                if (
                    content_item.time_end >= time_start
                    and content_item.time_start <= time_end
                ):
                    yield content_item

    def get(self, request):

        time_start = timezone.now() - datetime.timedelta(seconds=60 * 30)
        time_end = timezone.now() + datetime.timedelta(seconds=60 * 30)

        emissions = Emission.objects.filter(
            time_end__gte=time_start, time_start__lte=time_end
        )

        print("time_start", time_start)
        print("time_end", time_end)

        content_items = list(self.get_content_items(emissions, time_start, time_end))
        print("emissions", emissions)
        print("content_items", content_items)

        # serializer = PlayoutScheduleSerializer(instance=emissions)
        serializer = PlayoutScheduleSerializer(instance=content_items)
        return Response(serializer.data)


playout_schedule = PlayoutSchedule.as_view()
