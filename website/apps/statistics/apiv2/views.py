# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from ..utils.usage_statistics import get_usage_statistics


class UsageStatisticsView(GenericAPIView):

    def get_object(self, obj_ct, obj_uuid):
        try:
            obj = apps.get_model(*obj_ct.split(".")).objects.get(uuid=obj_uuid)
            return obj

        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, obj_ct, obj_uuid):
        obj = self.get_object(obj_ct, obj_uuid)

        # for the moment the range defaults to the last 12 months (including current)
        today = datetime.now()
        end = date(today.year + today.month // 12, today.month % 12 + 1, 1) - timedelta(1)
        start = end - relativedelta(years=1, days=-1)

        usage_statistics = get_usage_statistics(obj=obj, start=start, end=end)

        return Response(usage_statistics)
        # return super(UsageStatisticsView, self).list(request, *args, **kwargs)
