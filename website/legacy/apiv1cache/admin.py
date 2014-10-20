from django.contrib import admin

from models import ResourceMap

class ResourceMapAdmin(admin.ModelAdmin):

    list_display = ['__unicode__',  'v1_id',  'v2_id',  'status']
    list_filter = ['type', 'status']
    #date_hierarchy = 'created'
    search_fields = ['v1_id', ]

admin.site.register(ResourceMap, ResourceMapAdmin)