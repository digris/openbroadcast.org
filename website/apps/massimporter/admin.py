from django.contrib import admin

from massimporter.models import Massimport, MassimportFile


class MassimportFileAdmin(admin.ModelAdmin):

    list_display = ("path", "massimport", "created", "status")
    readonly_fields = ("created", "updated")
    date_hierarchy = "created"


class MassimportFileInline(admin.TabularInline):

    model = MassimportFile
    exclude = ["import_file"]
    readonly_fields = ["uuid", "path"]

    extra = 0


class MassimportAdmin(admin.ModelAdmin):

    list_display = ("directory", "created", "user", "status")
    list_filter = ("status",)
    readonly_fields = ("created", "updated")
    date_hierarchy = "created"
    inlines = [MassimportFileInline]


admin.site.register(Massimport, MassimportAdmin)
admin.site.register(MassimportFile, MassimportFileAdmin)
