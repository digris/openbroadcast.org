# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

#from .serializers import ReleaseSerializer
from alibrary.apiv2.serializers import PlaylistSerializer
from alibrary.models.playlistmodels import Playlist

SITE_URL = getattr(settings, 'SITE_URL')

SERIALIZER_MAP = {
    'alibrary.playlist': PlaylistSerializer,
}

log = logging.getLogger(__name__)

@api_view(['GET'])
def playlist_list(request, **kwargs):

    results = []

    q = request.GET.get('q', '').strip()

    qs = Playlist.objects.filter(
        user=request.user,
        type__in=['basket', 'playlist']
    ).order_by('-updated')

    if q != '':
        qs = qs.filter(
            Q(name__istartswith=q) | Q(series__name__istartswith=q)
        )

    serializer = PlaylistSerializer(
        qs[0:100],
        many=True,
        context={'request': request}
    )

    return Response({
        'results': serializer.data,
    })
