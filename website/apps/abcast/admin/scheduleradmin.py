# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from abcast.models import Emission, Daypart, DaypartSet, Weekday


class EmissionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "time_start",
        "time_end",
        "channel",
        "type",
        "user",
        "source",
        "locked",
        "status",
    )
    list_filter = ("type", "status", "channel")
    date_hierarchy = "time_start"
    readonly_fields = ("duration", "uuid", "slug")


admin.site.register(Emission, EmissionAdmin)


class DaypartInline(admin.TabularInline):
    model = Daypart
    extra = 0
    exclude = ["description", "mood", "sound", "talk"]


class DaypartSetAdmin(admin.ModelAdmin):
    list_display = ("channel", "time_start", "time_end")
    list_filter = ("channel",)
    date_hierarchy = "time_start"

    inlines = [DaypartInline]


admin.site.register(DaypartSet, DaypartSetAdmin)
admin.site.register(Daypart)
admin.site.register(Weekday)
