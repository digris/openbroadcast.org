# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from models import Waveform, Format

class WaveformAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'type',
        'status'
    )
    list_filter = (
        'type',
        'status'
    )
    raw_id_fields = ('media',)

admin.site.register(Waveform, WaveformAdmin)

class FormatAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'encoding',
        'quality',
        'status'
    )
    list_filter = (
        'encoding',
        'quality',
        'status'
    )
    raw_id_fields = ('media',)

admin.site.register(Format, FormatAdmin)
