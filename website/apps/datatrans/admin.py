from django.contrib import admin

from datatrans.models import KeyValue


class KeyValueAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'field',
                    'value', 'language', 'edited', 'fuzzy')
    ordering = ('digest', 'language')
    search_fields = ('content_type__app_label', 'content_type__model', 'value',)
    list_filter = ('content_type', 'language', 'edited', 'fuzzy')

admin.site.register(KeyValue, KeyValueAdmin)
