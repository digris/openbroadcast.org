from django.conf.urls.defaults import *

import views

    

urlpatterns = patterns('',

    url(r'^chat/rooms/$', views.RoomList.as_view(), name='room-list'),
    url(r'^chat/rooms/(?P<pk>\d+)/$', views.RoomDetail.as_view(), name='room-detail'),

    url(r'^chat/(?P<room>[\w.]+).(?P<mimetype>(json)|(html))$', views.chat, name = 'chat'),


)