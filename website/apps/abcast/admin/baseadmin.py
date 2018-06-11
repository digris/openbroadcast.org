# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from abcast.models import Station, Channel, Jingle, JingleSet, Role

class MembersInline(admin.TabularInline):
    model = Station.members.through

class ChannelsInline(admin.TabularInline):
    model = Channel
    readonly_fields = ('teaser', 'type', )
    exclude = ('description', 'stream_url', 'teaser',)

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'website',)
    readonly_fields = ('uuid', 'slug', )

    inlines = [ChannelsInline, MembersInline,]

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'station', 'type', 'stream_url', 'mount', )
    list_filter = ('station', 'type',)
    readonly_fields = ('uuid', 'slug', )

class JingleInline(admin.TabularInline):
    exclude = ['description', 'slug', 'processed', 'conversion_status']
    model = Jingle

class JingleAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'set', 'type' )
    list_filter = ('type',)
    readonly_fields = ('uuid', 'slug', 'folder')

class JingleSetAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid', 'slug', )
    inlines = [JingleInline, ]


admin.site.register(Station, StationAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Jingle, JingleAdmin)
admin.site.register(JingleSet, JingleSetAdmin)
admin.site.register(Role)
