# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

SITE_URL = getattr(settings, "SITE_URL")


class ImageSerializer(serializers.ImageField):
    def to_representation(self, instance):

        if not instance:
            return None

        url = thumbnail_url(instance, "thumbnail_240")
        if not url:
            return None

        return "{}{}".format(SITE_URL, url)


class AbsoluteUURLField(serializers.URLField):
    def to_representation(self, value):
        value = super(AbsoluteUURLField, self).to_representation(value)
        return "{}{}".format(SITE_URL, value)
