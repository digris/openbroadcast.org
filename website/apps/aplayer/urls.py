# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from aplayer import views

urlpatterns = [
    url(r'^popup/$', views.popup),
]
