from django.contrib import admin

from models import Waveform

class WaveformAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'type', 'status')
    list_filter = ('type', 'status')
    raw_id_fields = ('media',)

admin.site.register(Waveform, WaveformAdmin)
