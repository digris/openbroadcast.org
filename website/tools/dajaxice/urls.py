# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from .views import DajaxiceRequest

urlpatterns = [
    url(r"^(.+)/$", DajaxiceRequest.as_view(), name="dajaxice-call-endpoint"),
    url(r"", DajaxiceRequest.as_view(), name="dajaxice-endpoint"),
]
