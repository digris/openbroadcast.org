from django.contrib import admin
from profiles.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    date_hierarchy = 'created'
    readonly_fields = ('legacy_id','legacy_legacy_id',)
admin.site.register(Profile, ProfileAdmin)

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country')
    list_filter = ('country',)
    date_hierarchy = 'created'
    readonly_fields = ('legacy_id','legacy_legacy_id',)
admin.site.register(Community, CommunityAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'service')
    list_filter = ('profile', 'service')
admin.site.register(Service, ServiceAdmin)


admin.site.register(MobileProvider)
admin.site.register(ServiceType)
admin.site.register(Link)
admin.site.register(Expertise)