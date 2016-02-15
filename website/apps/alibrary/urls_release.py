# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import *
from alibrary.views import *

urlpatterns = patterns('',
    
    url(r'^autocomplete/$', release_autocomplete, name='release_autocomplete'),

    url(r'^$', ReleaseListView.as_view(), name='alibrary-release-list'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', ReleaseDetailView.as_view(), name='alibrary-release-detail'),
    url(r'^(?P<pk>\d+)/edit/$', ReleaseEditView.as_view(), name='alibrary-release-edit'),

)
