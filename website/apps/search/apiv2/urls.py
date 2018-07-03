# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import views

@api_view(['GET'])
def search_api_root(request, format=None):
    return Response({
        'search': reverse('api:search-global', request=request, format=format),
    })

urlpatterns = [
    url(r'^$', search_api_root, name='search-index'),
    url(r'^global/$', views.search_global, name='search-global'),
    url(r'^(?P<ct>[a-z.]+)/$', views.search_global, name='search-by-ctype'),
]
