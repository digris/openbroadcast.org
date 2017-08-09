# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_views


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'library/playlist': reverse('api:playlist-list', request=request, format=format),
        'library/artist': reverse('api:artist-list', request=request, format=format),
        'library/release': reverse('api:release-list', request=request, format=format),
        'library/track': reverse('api:media-list', request=request, format=format),
        'auth-token': reverse('api:obtain-auth-token', request=request, format=format),
    })



urlpatterns = [
    url(r'^$', api_root),
    url(r'^api-token-auth/', auth_views.obtain_auth_token, name='obtain-auth-token'),
    url('^library/', include('alibrary.apiv2.urls')),

]
