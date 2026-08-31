from django.contrib import admin

from .models import PreflightCheck


def preflight_check_set_pending(modeladmin, request, queryset):
    for preflight_check in queryset:
        preflight_check.status = PreflightCheck.STATUS_PENDING
        preflight_check.checks = {}
        preflight_check.warnings = []
        preflight_check.errors = []
        preflight_check.save()


preflight_check_set_pending.short_description = "Reprocess selected"


@admin.register(PreflightCheck)
class PreflightCheckAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "media_display",
        "checks",
        "warnings",
        "errors",
        "created",
        "updated",
        "status",
        "has_warnings",
        "has_errors",
    ]
    list_filter = [
        "status",
    ]
    readonly_fields = [
        "checks",
        "warnings",
        "errors",
    ]

    search_fields = [
        "media__id",
        "media__uuid",
        "media__name",
    ]

    date_hierarchy = "created"
    raw_id_fields = ("media",)
    actions = [
        preflight_check_set_pending,
    ]

    def media_display(self, obj):
        if obj.media:
            return f"""<p><a href="{obj.media.get_admin_url()}">{obj.media.name[0:48]}</a><br><a href="{obj.media.get_absolute_url()}">View on site</a><br>{obj.media.uuid}</p>"""
        return "-"

    media_display.short_description = "Media"
    media_display.allow_tags = True
