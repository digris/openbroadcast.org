# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^most-played/tracks/$", views.MostPlayedMediaList.as_view(), name="statistics-most-played-media"),
]
