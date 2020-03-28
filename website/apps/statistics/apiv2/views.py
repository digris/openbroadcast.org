# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import OrderedDict, Counter
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import serializers
from elasticsearch_dsl import Q as ESQ

from alibrary.documents import MediaDocument

from alibrary.models import Media
from atracker.models import Event

PLAYOUT_EVENT_TYPE_ID = 3

SITE_URL = getattr(settings, "SITE_URL")


log = logging.getLogger(__name__)


class MSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["name", "uuid"]


class ObjSerializer(serializers.Serializer):

    num_emissions = serializers.IntegerField()
    obj = serializers.SerializerMethodField()

    def get_obj(self, *args, **kwargs):
        obj_id = args[0]["obj_id"]
        return MSerializer(Media.objects.get(pk=obj_id)).data


class MostPlayedMediaList(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = ObjSerializer

    def get_date_range(self):

        _date_start = self.request.query_params.get("date_start", None)
        _date_end = self.request.query_params.get("date_end", None)

        if _date_start:
            date_start = datetime.strptime(_date_start, "%Y-%m-%d")
        else:
            date_start = None

        if _date_end:
            date_end = datetime.strptime(_date_end, "%Y-%m-%d")
        else:
            date_end = None

        return date_start, date_end

    def get_queryset(self):

        date_start, date_end = self.get_date_range()

        ct = ContentType.objects.get_for_model(Media)

        event_qs = Event.objects.filter(
            created__range=(date_start, date_end),
            content_type__pk=ct.pk,
            event_type_id=PLAYOUT_EVENT_TYPE_ID,
        ).values_list("object_id", flat=True)

        _counter = Counter(list(event_qs))
        counter = OrderedDict(_counter.most_common())

        x = []
        for obj_id, num_emissions in counter.items():
            x.append(
                {"num_emissions": num_emissions, "obj_id": obj_id,}
            )

        return x

    def get(self, request, *args, **kwargs):
        return super(MostPlayedMediaList, self).list(request, *args, **kwargs)
