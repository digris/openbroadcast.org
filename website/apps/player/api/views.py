# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PlaySerializer
from ..models import PlayerItem

SITE_URL = getattr(settings, 'SITE_URL')


@api_view(['PUT'])
def play(request, **kwargs):
    obj_ct = kwargs.get('obj_ct')
    obj_uuid = kwargs.get('obj_uuid')

    # get content_object from ctype & uuid
    try:
        obj = apps.get_model(*obj_ct.split('.')).objects.get(uuid=obj_uuid)

    except ObjectDoesNotExist:
        raise Http404

    play_item = PlayerItem(
        content_object=obj
    )

    if request.user.is_authenticated():
        play_item.user = request.user
    else:
        play_item.session_id = request.session.session_key

    play_item.save()

    play_url = '{}{}'.format(SITE_URL, reverse('api:player-play-detail', kwargs={'uuid': play_item.uuid}))

    return Response({
        'url': play_url,
    }, status=303, headers={'Location': play_url})


#######################################################################
# API Play Views
#######################################################################
class PlayViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PlayerItem.objects.all().order_by('-created')
    serializer_class = PlaySerializer
    lookup_field = 'uuid'


play_list = PlayViewSet.as_view({
    'get': 'list',
})
play_detail = PlayViewSet.as_view({
    'get': 'retrieve',
})
