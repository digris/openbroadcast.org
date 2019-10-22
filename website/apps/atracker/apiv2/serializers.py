# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers


class ObjectEventSerializer(serializers.Serializer):

    ct = serializers.CharField(read_only=True, source="content_object.get_ct")
    uuid = serializers.UUIDField(read_only=True, source="content_object.uuid")
    created = serializers.DateTimeField(read_only=True)
    event_type = serializers.CharField(read_only=True)
