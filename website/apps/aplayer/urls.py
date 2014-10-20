from django.conf.urls.defaults import *


urlpatterns = patterns('',

    #(r'^popup/$', direct_to_template, {'template': 'aplayer/popup.html'}),
    
    (r'^popup/$', 'aplayer.views.popup'),
    (r'^proxy/$', 'aplayer.views.sc_proxy'),

)