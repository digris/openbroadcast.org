# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings

from rest_framework import serializers

from ..models import (
    PreflightCheck
)

SITE_URL = getattr(settings, 'SITE_URL')


class PreflightCheckSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='api:preflight-check-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = PreflightCheck
        depth = 1
        fields = [
            'url',
            'status',
            'result',
        ]
