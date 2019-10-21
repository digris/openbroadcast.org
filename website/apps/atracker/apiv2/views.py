# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import logging

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from .serializers import EventSerializer
from ..models import Event

USER_MODEL = settings.AUTH_USER_MODEL

log = logging.getLogger(__name__)


class ObjectEventView(APIView):
    """
    Create event (with option to impersonate as user)
    """

    def get_object(self, obj_ct, obj_uuid):
        # get content_object from ct & uuid
        try:
            obj = apps.get_model(*obj_ct.split(".")).objects.get(uuid=obj_uuid)
            return obj

        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, obj_ct, obj_uuid):

        data = json.loads(request.body.decode("utf-8", "strict"))
        obj = self.get_object(obj_ct, obj_uuid)
        event_type = data.get("event_type")
        impersonate_user_id = data.get("impersonate_user_id")

        if not impersonate_user_id:
            user = request.user
        elif impersonate_user_id and request.user.has_perm("atracker.track_for_user"):
            user = get_user_model().objects.get(id=impersonate_user_id)
        else:
            raise PermissionDenied("no permission to impersonate")

        _ct = ContentType.objects.get_for_model(obj)

        log.debug("event PUT ct: {} - id: {} - user: {}".format(_ct, obj.pk, user))

        event = Event.create_event(user, obj, event_type=event_type)
        serializer = EventSerializer(event)

        return Response(serializer.data)
