# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Waveform, Format


def waveform_set_init(modeladmin, request, queryset):
    for item in queryset:
        item.status = Waveform.INIT
        item.save()


def format_set_init(modeladmin, request, queryset):
    for item in queryset:
        item.status = Format.INIT
        item.save()


waveform_set_init.short_description = "Reprocess selected"
format_set_init.short_description = "Reprocess selected"


@admin.register(Waveform)
class WaveformAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "media_display",
        "type",
        "created",
        "accessed",
        "status",
    ]
    list_filter = [
        "type",
        "status",
    ]
    date_hierarchy = "created"
    search_fields = [
        "media__id",
        "media__name",
        "media__uuid",
    ]
    raw_id_fields = [
        "media",
    ]
    actions = [waveform_set_init]

    def media_display(self, obj):
        if obj.media:
            return """<p><a href="{admin_url}">{name}</a><br><a href="{public_url}">View on site</a></p>""".format(
                admin_url=obj.media.get_admin_url(),
                name=obj.media.name[0:48],
                public_url=obj.media.get_absolute_url(),
            )
        return "-"

    media_display.short_description = _("Media")
    media_display.allow_tags = True


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "media_display",
        "encoding",
        "quality",
        "filesize_display",
        "created",
        "accessed",
        "status",
    ]
    list_filter = [
        "encoding",
        "quality",
        "status",
    ]
    date_hierarchy = "created"
    search_fields = [
        "media__id",
        "media__name",
        "media__uuid",
    ]
    raw_id_fields = [
        "media",
    ]
    actions = [format_set_init]

    def media_display(self, obj):
        if obj.media:
            return """<p><a href="{admin_url}">{name}</a><br><a href="{public_url}">View on site</a></p>""".format(
                admin_url=obj.media.get_admin_url(),
                name=obj.media.name[0:48],
                public_url=obj.media.get_absolute_url(),
            )
        return "-"

    media_display.short_description = _("Media")
    media_display.allow_tags = True
