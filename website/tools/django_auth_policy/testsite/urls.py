from django import http
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from django_auth_policy.urls import urlpatterns


@login_required
def login_required_view(request):
    return http.HttpResponse('ok')

def another_view(request):
    return http.HttpResponse('another view')

urlpatterns = urlpatterns + patterns('',
    url(r'^$', login_required_view, name='login_required_view'),
    url(r'^another/$', another_view, name='another_view'),
    )
