from django.contrib import admin

from importer.models import *



def status_set_ready(modeladmin, request, queryset):
    queryset.update(status=2)
status_set_ready.short_description = 'Set status to "ready"'

def status_set_queued(modeladmin, request, queryset):
    queryset.update(status=6)


def requeue(modeladmin, request, queryset):

    for item in queryset:
        item.status = 6
        item.save()


status_set_queued.short_description = 'Set status to "queued"'


class ImportImportFileInline(admin.TabularInline):
    model = ImportFile
    extra = 0
    readonly_fields = ('filename', 'mimetype', 'media')
    exclude = ('messages', 'results_tag', 'results_acoustid', 'results_musicbrainz', 'results_discogs', 'import_tag', 'imported_api_url', 'settings')
    
class ImportItemnline(admin.TabularInline):
    model = ImportItem
    extra = 0
    readonly_fields = ('content_type', 'object_id',)

class ImportAdmin(admin.ModelAdmin):    
    
    list_display = ('created', 'user', 'status', 'type', 'uuid_key',)
    list_filter = ('status', 'user',)    
    readonly_fields = ('created', 'updated',)
    date_hierarchy = 'created'
    inlines = [ImportImportFileInline, ImportItemnline]
    actions = [status_set_ready]

class ImportFileAdmin(admin.ModelAdmin):    
    
    list_display = ('created', 'filename', 'status',)
    list_filter = ('status', 'import_session',)
    readonly_fields = ('created', 'updated', 'mimetype', 'import_session', 'media', 'results_tag', 'results_musicbrainz', 'results_discogs',)
    date_hierarchy = 'created'
    actions = [status_set_ready, status_set_queued, requeue]

admin.site.register(Import, ImportAdmin)
admin.site.register(ImportFile, ImportFileAdmin)
admin.site.register(ImportItem)













