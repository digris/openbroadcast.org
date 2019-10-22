# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import logging

from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Avg
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from ..models import Vote
from .serializers import ObjectRatingSerializer

USER_MODEL = settings.AUTH_USER_MODEL

log = logging.getLogger(__name__)


class ObjectRatingView(APIView):
    """
    Create/update rating (a.k.a. "vote") (with option to impersonate as user)
    """

    def get_object(self, obj_ct, obj_uuid):
        try:
            obj = apps.get_model(*obj_ct.split(".")).objects.get(uuid=obj_uuid)
            return obj

        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, obj_ct, obj_uuid):
        obj = self.get_object(obj_ct, obj_uuid)
        user_id = request.GET.get("user_id")

        if not request.user.is_authenticated():
            user = None
        elif user_id and request.user.has_perm("arating.vote_for_user"):
            user = get_user_model().objects.get(id=user_id)
        else:
            user = request.user

        log.debug("vote GET obj: {} - user: {}".format(obj, user))

        serializer = ObjectRatingSerializer(instance=obj, user=user)
        return Response(serializer.data)

    def put(self, request, obj_ct, obj_uuid):

        data = json.loads(request.body.decode("utf-8", "strict"))
        obj = self.get_object(obj_ct, obj_uuid)
        vote = data.get("vote")
        impersonate_user_id = data.get("impersonate_user_id")

        if not impersonate_user_id:
            user = request.user
        elif impersonate_user_id and request.user.has_perm("arating.vote_for_user"):
            user = get_user_model().objects.get(id=impersonate_user_id)
        else:
            raise PermissionDenied("no permission to impersonate")

        _ct = ContentType.objects.get_for_model(obj)

        if vote == 0:
            Vote.objects.filter(content_type=_ct, object_id=obj.pk, user=user).delete()
        elif vote in [-1, 1]:
            try:
                vote_obj = Vote.objects.get(
                    content_type=_ct, object_id=obj.pk, user=user
                )
                vote_obj.vote = vote
            except Vote.DoesNotExist:
                vote_obj = Vote(
                    content_type=_ct, object_id=obj.pk, user=user, vote=vote
                )
            vote_obj.save()
        else:
            raise ValidationError("invalid value")

        log.debug(
            "vote PUT ct: {} - id: {} - user: {} - user id: {} - vote: {}".format(
                _ct, obj.pk, user, user.pk, vote
            )
        )

        obj.refresh_from_db()

        serializer = ObjectRatingSerializer(instance=obj, user=user)
        return Response(serializer.data)
