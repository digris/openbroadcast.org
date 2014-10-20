from django.contrib import admin
from guardian.admin import GuardedModelAdmin

class BaseAdmin(admin.ModelAdmin):
    
    search_fields = ['name']
    save_on_top = True

from ashop.models import *


class HardwarereleaseAdmin(BaseAdmin):
    """
    release products always are tied to a release. slug & name are inherited
    """
    list_display   = ('name', 'format', 'unit_price', 'active')
    
    readonly_fields = ['name', 'slug']

admin.site.register(Hardwarerelease, HardwarereleaseAdmin)


class DownloadreleaseAdmin(BaseAdmin, GuardedModelAdmin):
    
    list_display   = ('name', 'format', 'unit_price', 'active')

    """
    release products always are tied to a release. slug & name are inherited
    """
    readonly_fields = ['name', 'slug']
    
admin.site.register(Downloadrelease, DownloadreleaseAdmin)


class DownloadmediaAdmin(BaseAdmin, GuardedModelAdmin):
    
    list_display   = ('name', 'format', 'get_release', 'unit_price')
    
    def get_release(self, obj):
        return obj.media.release

    """
    media products always are tied to a release. slug & name are inherited
    """
    readonly_fields = ['name', 'slug']
    
admin.site.register(Downloadmedia, DownloadmediaAdmin)




