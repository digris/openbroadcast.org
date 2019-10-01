# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from abcast.models import Station, Channel, Role


class MembersInline(admin.TabularInline):
    model = Station.members.through


class ChannelsInline(admin.TabularInline):
    model = Channel
    readonly_fields = ("teaser", "type")
    exclude = ("description", "stream_url", "teaser")


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "website")
    readonly_fields = ("uuid", "slug")

    inlines = [ChannelsInline, MembersInline]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "station", "type", "stream_url", "mount")
    list_filter = ("station", "type")
    readonly_fields = ("uuid", "slug")


admin.site.register(Role)
