from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from django.views.generic.base import RedirectView

OPTION_MESSAGES = 'm'
OPTIONS = OPTION_MESSAGES

# urlpatterns = patterns('postman.views',
#     url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', 'inbox', name='postman_inbox'),
#     url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', 'sent', name='postman_sent'),
#     url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', 'archives', name='postman_archives'),
#     url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', 'trash', name='postman_trash'),
#     url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', 'write', name='postman_write'),
#     url(r'^reply/(?P<message_id>[\d]+)/$', 'reply', name='postman_reply'),
#     url(r'^view/(?P<message_id>[\d]+)/$', 'view', name='postman_view'),
#     url(r'^view/t/(?P<thread_id>[\d]+)/$', 'view_conversation', name='postman_view_conversation'),
#     url(r'^archive/$', 'archive', name='postman_archive'),
#     url(r'^delete/$', 'delete', name='postman_delete'),
#     url(r'^undelete/$', 'undelete', name='postman_undelete'),
#     (r'^$', RedirectView.as_view(url='inbox/', permanent=False)),
# )

from postman import views

urlpatterns = [
    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', views.inbox, name='postman_inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', views.sent, name='postman_sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', views.archives, name='postman_archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', views.trash, name='postman_trash'),
    url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', views.write, name='postman_write'),
    url(r'^reply/(?P<message_id>[\d]+)/$', views.reply, name='postman_reply'),
    url(r'^view/(?P<message_id>[\d]+)/$', views.view, name='postman_view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', views.view_conversation, name='postman_view_conversation'),
    url(r'^archive/$', views.archive, name='postman_archive'),
    url(r'^delete/$', views.delete, name='postman_delete'),
    url(r'^undelete/$', views.undelete, name='postman_undelete'),
    url(r'^$', RedirectView.as_view(url='inbox/', permanent=False)),
]
