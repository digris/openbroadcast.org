from django.conf.urls.defaults import *
from profiles.views import *

urlpatterns = patterns('profiles.views',
                                               
    url(r'^$', ProfileListView.as_view(), name='profiles-profile-list'),
    url(r'^edit/$',  view='profile_edit', name='profiles-profile-edit'),
    url(r'^invitations/$',  InvitationListView.as_view(), name='profiles-invitations'),
    url(r'^invitations/(?P<pk>\d+)/delete/$',  InvitationDeleteView.as_view(), name='profiles-invitation-delete'),
    url(r'^force-login/(?P<username>[-\w]+)/$', view='profile_force_login', name='profiles-profile-force-login'),
    url(r'^(?P<slug>[-\w]+)/$', ProfileDetailView.as_view(), name='profiles-profile-detail'),
    
    url(r'^(?P<pk>\d+)/mentor/become/$', profile_mentor, {'cancel': False}, name='profiles-profile-mentor-become'),
    url(r'^(?P<pk>\d+)/mentor/cancel/$', profile_mentor, {'cancel': True}, name='profiles-profile-mentor-cancel'),
    url(r'^(?P<pk>\d+)/mentor/approve/(?P<level>[-\w]+)/$', profile_approve, name='profiles-profile-mentor-approve'),

)