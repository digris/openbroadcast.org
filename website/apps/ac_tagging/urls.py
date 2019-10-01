# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from ac_tagging import views

urlpatterns = [url(r"^list$", views.list_tags, name="ac_tagging-list")]
