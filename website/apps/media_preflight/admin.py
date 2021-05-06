# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import PreflightCheck


def preflight_check_set_pending(modeladmin, request, queryset):
    for preflight_check in queryset:
        preflight_check.status = PreflightCheck.STATUS_PENDING
        preflight_check.checks = {}
        preflight_check.warnings = []
        preflight_check.errors = []
        preflight_check.save()


preflight_check_set_pending.short_description = "Reprocess selected"


@admin.register(PreflightCheck)
class PreflightCheckAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "media_display",
        "checks",
        "warnings",
        "errors",
        "created",
        "updated",
        "status",
        "has_warnings",
        "has_errors",
    ]
    list_filter = [
        "status",
    ]
    readonly_fields = [
        "checks",
        "warnings",
        "errors",
    ]

    search_fields = [
        "media__id",
        "media__uuid",
        "media__name",
    ]

    date_hierarchy = "created"
    raw_id_fields = ("media",)
    actions = [
        preflight_check_set_pending,
    ]

    def media_display(self, obj):
        if obj.media:
            return """<p><a href="{admin_url}">{name}</a><br><a href="{public_url}">View on site</a><br>{uuid}</p>""".format(
                admin_url=obj.media.get_admin_url(),
                name=obj.media.name[0:48],
                public_url=obj.media.get_absolute_url(),
                uuid=obj.media.uuid,
            )
        return "-"

    media_display.short_description = _("Media")
    media_display.allow_tags = True
