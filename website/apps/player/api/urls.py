# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import views


@api_view(['GET'])
def player_api_root(request, format=None):
    return Response({
        'play': reverse('api:player-play-list', request=request, format=format),
    })


urlpatterns = [
    url(r'^$', player_api_root, name='player-index'),
    url(r'^play/$', views.play_list, name='player-play-list'),
    # url(r'^play/(?P<uuid>[0-9A-Fa-f-]+)/$', views.play_detail, name='player-play-detail'),
    # url(r'^play/(?P<obj_ct>[a-z-_\.]+):(?P<obj_uuid>[0-9A-Fa-f-]+)/$', views.play_detail, name='player-play-detail'),
    url(r'^play/(?P<uuid>[0-9A-Fa-f-]+)/$', views.play_detail, name='player-play-detail'),
    url(r'^play/(?P<obj_ct>[a-z-_\.]+):(?P<obj_uuid>[0-9A-Fa-f-]+)/$', views.play, name='player-play'),
]
