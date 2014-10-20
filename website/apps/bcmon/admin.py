from django.contrib import admin

from bcmon.models import *

from lib.admin.actions import export_as_csv_action

#class ChannelInline(admin.TabularInline):
#    model = Channel



class PlayoutAdmin(admin.ModelAdmin):    
    
    list_display = ('title', 'time_start', 'time_end', 'channel', 'status', 'score', 'dummy_result', 'media')
    list_filter = ('channel', 'status', 'score',)
    
    readonly_fields = ('created', 'updated', 'uuid', 'enmfp', 'analyzer_data', 'echoprintfp', 'echoprint_data', 'score', 'time_start', 'time_end')

    date_hierarchy = 'created'
    
    inlines = []
    
    actions = [export_as_csv_action("CSV Export", fields=['title', 'created', 'channel'])]
    
class ChannelAdmin(admin.ModelAdmin):    
    
    list_display = ('name', 'slug', 'stream_url', )
    
    readonly_fields = ('created', 'updated', 'uuid', 'slug', )



admin.site.register(Playout, PlayoutAdmin)
admin.site.register(Channel, ChannelAdmin)














