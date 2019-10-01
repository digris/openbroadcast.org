from django.contrib import admin

from exporter.models import Export, ExportItem


class ExportExportItemInline(admin.TabularInline):
    model = ExportItem
    extra = 0


class ExportAdmin(admin.ModelAdmin):
    list_display = (
        "filename",
        "created",
        "user",
        "status",
        "type",
        "fileformat",
        "filesize",
    )
    list_filter = ("status", "type", "fileformat")
    readonly_fields = ("created", "updated", "token")
    date_hierarchy = "created"
    inlines = [ExportExportItemInline]


class ExportItemAdmin(admin.ModelAdmin):
    list_display = ("content_object", "export_session")


admin.site.register(Export, ExportAdmin)
admin.site.register(ExportItem, ExportItemAdmin)
