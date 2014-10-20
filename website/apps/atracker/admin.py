"""Admin classes for the ``object_events`` app."""
from django.contrib import admin

from .models import Event, EventType
from lib.admin.actions import export_as_csv_action

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['title', ]


class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_object', 'event_content_object', 'type_title', 'created', 'archived', 'distributed', ]
    list_filter = ('event_type', 'archived')
    date_hierarchy = ('created')
    
    #actions = [export_as_csv_action("CSV Export", fields=['user', 'content_object__name', 'event_content_object__name', 'event_type__title', 'created'])]

    def content_object(self, obj):
        return obj.content_object
    content_object.short_description = 'Content object'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'

    def type_title(self, obj):
        return obj.event_type.title
    type_title.short_description = 'Type'


admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)