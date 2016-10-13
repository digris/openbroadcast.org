from django.contrib import admin

from importer.models import ImportFile, Import, ImportItem


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
    exclude = ('messages', 'results_tag', 'results_acoustid', 'results_musicbrainz', 'results_discogs', 'import_tag',
               'imported_api_url', 'settings')


class ImportItemnline(admin.TabularInline):
    model = ImportItem
    extra = 0
    readonly_fields = ('content_type', 'object_id',)


class ImportAdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = (
        'created',
        'user',
        'status',
        'type',
    )

    raw_id_fields = ['user', ]

    search_fields = (
        'user__username',
        'files__filename',
        # 'files__media__name',
    )
    list_filter = ('status',)
    readonly_fields = (
        'created',
        'updated',
        'notes',
    )
    date_hierarchy = 'created'
    inlines = [ImportImportFileInline, ImportItemnline]
    actions = [status_set_ready]

admin.site.register(Import, ImportAdmin)

class ImportFileAdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = (
        'created',
        'filename',
        'media',
        'error',
        'status',
        'mimetype',
    )

    search_fields = (
        'id',
        'filename',
        'media__name',
    )

    list_filter = (
        'status',
    )
    readonly_fields = (
        'created',
        'updated',
        'mimetype',
        'import_session',
        'media',
        'results_tag',
        'results_musicbrainz',
        'results_discogs',
    )
    date_hierarchy = 'created'
    actions = [status_set_ready, status_set_queued, requeue]



admin.site.register(ImportFile, ImportFileAdmin)


class ImportItemAdmin(admin.ModelAdmin):
    save_on_top = True

    list_display = (
        'import_session',
        'content_type',
        'object_id',
        'content_object',
    )

admin.site.register(ImportItem, ImportItemAdmin)
