# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from selectable import registry, views

registry.autodiscover()

urlpatterns = [
    url(r'^(?P<lookup_name>[-\w]+)/$', views.get_lookup, name="selectable-lookup"),
]
