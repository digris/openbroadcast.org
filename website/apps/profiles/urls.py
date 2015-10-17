from django.conf.urls import *


urlpatterns = patterns('profiles.views',
    url(r'^edit/$',
        view='profile_edit',
        name='profile_edit',
    ),
    url(r'^(?P<username>[-\w]+)/$',
        view='profile_detail',
        name='profile_detail',
    ),
    url (r'^$',
        view='profile_list',
        name='profile_list',
    ),
)