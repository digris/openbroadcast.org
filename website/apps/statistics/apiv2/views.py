# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from collections import OrderedDict
from django.conf import settings
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param
from rest_framework.views import APIView
from elasticsearch_dsl import Q as ESQ

from alibrary.documents import MediaDocument

SITE_URL = getattr(settings, "SITE_URL")


log = logging.getLogger(__name__)


class MostPlayedMediaList(APIView):
    def get_search_query(self):

        _date_start = self.request.query_params.get("date_start", None)
        _date_end = self.request.query_params.get("date_end", None)

        if _date_start:
            date_start = datetime.strptime(_date_start, '%Y-%m-%d')
        else:
            date_start = None

        if _date_end:
            date_end = datetime.strptime(_date_end, '%Y-%m-%d')
        else:
            date_end = None

        s = MediaDocument.search().query("bool", must_not=[ESQ("match", type="Jingle")])

        _range = {}

        if date_start:
            _range.update({"gte": date_start})

        if date_end:
            _range.update({"lte": date_end})

        if date_start or date_end:
            s = s.query("range", last_emission=_range)

        s = s.sort({"num_emissions": {"order": "desc"}})

        return s

    def get(self, request, *args, **kwargs):

        search_query = self.get_search_query()

        count = search_query.count()
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))

        # pagination links
        if offset + limit >= count:
            next_link = None
        else:
            url = request.build_absolute_uri()
            url = replace_query_param(url, "limit", limit)
            next_link = replace_query_param(url, "offset", offset + limit)

        if offset <= 0:
            previous_link = None
        else:
            url = request.build_absolute_uri()
            url = replace_query_param(url, "limit", limit)

            if offset - limit <= 0:
                previous_link = remove_query_param(url, "offset")
            else:
                previous_link = replace_query_param(url, "offset", offset - limit)

        results = []
        for r in search_query[offset : (offset + limit)]:
            results.append(
                {
                    "num_emissions": r.num_emissions,
                    "uuid": r.uuid,
                    "url": SITE_URL + r.url,
                    "api_url": SITE_URL + r.api_url,
                    "name": r.name,
                    "artist": r.artist_display,
                    "release": r.release_display,
                }
            )

        return Response(
            OrderedDict(
                [
                    ("count", count),
                    ("next", next_link),
                    ("previous", previous_link),
                    ("results", results),
                ]
            )
        )
