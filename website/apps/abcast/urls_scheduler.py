# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from abcast import views

urlpatterns = [
    url(r'^$', views.schedule, name='abcast-schedule'),
    url(r'^emssion/(?P<pk>\d+)/$', views.EmissionDetailView.as_view(), name='abcast-emission-detail'),
    url(r'^select-playlist/$', views.select_playlist, name='abcast-schedule-select-playlist'),
    url(r'^schedule-object/$', views.schedule_object, name='abcast-schedule-schedule-object'),
    url(r'^copy-paste-day/$', views.copy_paste_day, name='abcast-schedule-copy-paste-day'),
    url(r'^delete-day/$', views.delete_day, name='abcast-schedule-delete-day'),

    # next-gen views
    url(r'^ng/$', views.SchedulerIndexNG.as_view(), name='scheduler-index-ng'),
]
