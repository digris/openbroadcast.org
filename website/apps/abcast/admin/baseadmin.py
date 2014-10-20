from django.contrib import admin

from abcast.models import *


class MembersInline(admin.TabularInline):
    model = Station.members.through


class ChannelsInline(admin.TabularInline):
    model = Channel
    readonly_fields = ('teaser', 'type', 'stream_server', )
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
    
    #list_display = ('name', 'duration', 'set', 'type' )
    #list_filter = ('type',)
    readonly_fields = ('uuid', 'slug', )
    
    inlines = [JingleInline, ]
    

#class MountpointInline(admin.TabularInline):
#    model = StreamMountpoint
#    extra = 1

class StreamServerAdmin(admin.ModelAdmin):    
    
    list_display = ('name', 'host', 'type' )
    list_filter = ('type',)
    readonly_fields = ('uuid',)
    inlines = []
    
    

admin.site.register(Station, StationAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Jingle, JingleAdmin)
admin.site.register(JingleSet, JingleSetAdmin)




admin.site.register(StreamServer, StreamServerAdmin)
admin.site.register(StreamFormat)
admin.site.register(Role)














