# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import views


@api_view(["GET"])
def player_api_root(request, format=None):
    return Response(
        {"play": reverse("api:player-play", request=request, format=format)}
    )


urlpatterns = [
    url(r"^$", player_api_root, name="player-index"),
    url(r"^play/$", views.play, name="player-play"),
]
