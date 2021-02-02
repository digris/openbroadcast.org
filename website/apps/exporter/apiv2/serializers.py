# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from rest_flex_fields.serializers import FlexFieldsSerializerMixin

from ..models import Export


class ExportSerializer(
    FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer
):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:export-detail", lookup_field="uuid"
    )

    ct = serializers.CharField(source="get_ct", read_only=True)
    name = serializers.CharField(source="filename", read_only=True)
    format = serializers.CharField(source="fileformat", read_only=True)
    download_url = serializers.CharField(source="get_download_url", read_only=True)

    class Meta:
        model = Export
        depth = 1
        fields = [
            "url",
            "ct",
            "uuid",
            "created",
            "status",
            "name",
            "filesize",
            "format",
            "download_url",
        ]
