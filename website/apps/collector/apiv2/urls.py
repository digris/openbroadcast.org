# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import views


@api_view(["GET"])
def collector_api_root(request, format=None):
    return Response(
        {
            "playlist": reverse(
                "api:collector-playlist-list", request=request, format=format
            )
        }
    )


urlpatterns = [
    url(r"^$", collector_api_root, name="collector-index"),
    url(r"^playlist/$", views.playlist_list, name="collector-playlist-list"),
]
