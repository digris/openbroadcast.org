# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from .views import LabelDetailView, LabelListView, LabelEditView, label_autocomplete

urlpatterns = [
    url(r'^autocomplete/$', label_autocomplete, name='alibrary-label-autocomplete'),
    url(r'^$', LabelListView.as_view(), name='alibrary-label-list'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', LabelDetailView.as_view(), name='alibrary-label-detail'),
    url(r'^(?P<pk>\d+)/edit/$', LabelEditView.as_view(), name='alibrary-label-edit'),
]
