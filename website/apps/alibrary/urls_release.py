# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from .views import ReleaseListView, ReleaseDetailView, ReleaseEditView

urlpatterns = [
    url(r'^$', ReleaseListView.as_view(), name='alibrary-release-list'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', ReleaseDetailView.as_view(), name='alibrary-release-detail'),
    url(r'^(?P<pk>\d+)/edit/$', ReleaseEditView.as_view(), name='alibrary-release-edit'),
]
