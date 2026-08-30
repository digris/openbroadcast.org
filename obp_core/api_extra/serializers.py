from django.conf import settings
from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

SITE_URL = settings.SITE_URL


class ImageSerializer(serializers.ImageField):
    def to_representation(self, instance):

        if not instance:
            return None

        url = thumbnail_url(instance, "thumbnail_240")
        if not url:
            return None

        return f"{SITE_URL}{url}"


class AbsoluteURLField(serializers.URLField):
    def to_representation(self, value):
        value = super().to_representation(value)
        return f"{SITE_URL}{value}"
