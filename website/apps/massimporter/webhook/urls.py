# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import WebookView

urlpatterns = [
    url(r"^(?P<name>[\w-]+)$", WebookView.as_view()),
    url(r"^(?P<name>[\w-]+)/$", WebookView.as_view()),
    url(r"^$", WebookView.as_view()),
]
