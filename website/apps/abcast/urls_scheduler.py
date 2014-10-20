from django.conf.urls.defaults import *

from abcast.views import *

urlpatterns = patterns('',   
    url(r'^$', schedule, name='abcast-schedule'),              
    url(r'^emssion/(?P<pk>\d+)/$', EmissionDetailView.as_view(), name='abcast-emission-detail'),
    url(r'^select-playlist/$', select_playlist, name='abcast-schedule-select-playlist'),  
    url(r'^schedule-object/$', schedule_object, name='abcast-schedule-schedule-object'),  
    url(r'^copy-paste-day/$', copy_paste_day, name='abcast-schedule-copy-paste-day'),
    url(r'^delete-day/$', delete_day, name='abcast-schedule-delete-day'),
)