# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change, {'post_change_redirect': '/network/profiles/edit/', 'password_change_form': SetPasswordForm}, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
]
