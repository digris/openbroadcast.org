# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

app_name = 'player'
urlpatterns = [
    url(
        r'^$',
        views.PlayerIndexView.as_view(),
        name='player-index'
    ),
]
