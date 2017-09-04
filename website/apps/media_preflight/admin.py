# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import PreflightCheck


def preflight_check_set_init(modeladmin, request, queryset):
    for item in queryset:
        item.status = PreflightCheck.STATUS_INIT
        item.result = None
        item.preflight_ok = False
        item.save()
preflight_check_set_init.short_description = "Reprocess selected"

@admin.register(PreflightCheck)
class PreflightCheckAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'media_display',
        'result',
        'status',
        'preflight_ok',
    ]
    list_filter = [
        'status',
        'preflight_ok',
    ]
    readonly_fields = [
        'result',
    ]
    #date_hierarchy = 'created'
    raw_id_fields = ('media',)
    actions = [preflight_check_set_init]

    def media_display(self, obj):
        if obj.media:
            return """<p><a href="{admin_url}">{name}</a><br><a href="{public_url}">View on site</a><br>{uuid}</p>""".format(
                admin_url=obj.media.get_admin_url(),
                name=obj.media.name[0:48],
                public_url=obj.media.get_absolute_url(),
                uuid=obj.media.uuid
            )
        return '-'
    media_display.short_description = _('Media')
    media_display.allow_tags = True
