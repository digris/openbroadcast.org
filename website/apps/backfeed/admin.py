from django.contrib import admin
from backfeed.models import Backfeed

class BackfeedAdmin(admin.ModelAdmin):

    list_display = ['user', 'get_email', 'subject', 'created']
    date_hierarchy = 'created'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'EMail'

admin.site.register(Backfeed, BackfeedAdmin)
