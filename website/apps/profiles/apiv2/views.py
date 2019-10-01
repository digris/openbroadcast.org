# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import viewsets

from .serializers import ProfileSerializer
from ..models import Profile

log = logging.getLogger(__name__)


class ProfileViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    queryset = Profile.objects.all().order_by("-created")
    serializer_class = ProfileSerializer
    lookup_field = "uuid"

    def get_object(self):
        if self.kwargs.get("user_id"):
            return get_object_or_404(Profile, user__id=self.kwargs.get("user_id"))

        return get_object_or_404(Profile, uuid=self.kwargs.get("uuid"))


profile_list = ProfileViewSet.as_view({"get": "list"})

profile_detail = ProfileViewSet.as_view({"get": "retrieve"})
