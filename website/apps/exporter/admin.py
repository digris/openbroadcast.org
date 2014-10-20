from django.contrib import admin

from exporter.models import *


class ExportExportItemInline(admin.TabularInline):
    model = ExportItem
    extra = 0
    #readonly_fields = ('filename',)

class ExportAdmin(admin.ModelAdmin):  

    list_display = ('filename', 'created', 'user', 'status', 'type', 'fileformat', 'filesize')
    list_filter = ('status', 'type', 'fileformat',)
    readonly_fields = ('created', 'updated', 'token',)
    date_hierarchy = 'created'
    inlines = [ExportExportItemInline]
    
    
class ExportItemAdmin(admin.ModelAdmin):    
    list_display = ( 'content_object', 'export_session',)
    """
    list_display = ('created', 'filename', 'status',)
    list_filter = ('status', 'import_session__user',)    
    readonly_fields = ('created', 'updated', 'mimetype', 'import_session', 'results_tag', 'import_tag', 'results_musicbrainz', 'results_discogs',)
    date_hierarchy = 'created'
    """

admin.site.register(Export, ExportAdmin)
admin.site.register(ExportItem, ExportItemAdmin)













