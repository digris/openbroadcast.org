from django.conf.urls import patterns, url

from abcast.views import schedule, EmissionDetailView, select_playlist, schedule_object, copy_paste_day, delete_day

urlpatterns = patterns('',   
    url(r'^$', schedule, name='abcast-schedule'),              
    url(r'^emssion/(?P<pk>\d+)/$', EmissionDetailView.as_view(), name='abcast-emission-detail'),
    url(r'^select-playlist/$', select_playlist, name='abcast-schedule-select-playlist'),  
    url(r'^schedule-object/$', schedule_object, name='abcast-schedule-schedule-object'),  
    url(r'^copy-paste-day/$', copy_paste_day, name='abcast-schedule-copy-paste-day'),
    url(r'^delete-day/$', delete_day, name='abcast-schedule-delete-day'),
)
