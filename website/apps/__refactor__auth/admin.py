from django.contrib import admin

from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django_extensions.admin import ForeignKeyAutocompleteAdmin

from .models import UserProfile


# UserProfile inline
class UserProfileInline(admin.TabularInline):
    model = UserProfile
    readonly_fields = ['device', ]


# add api/profile inline to user admin
class UserModelAdmin(UserAdmin):
    save_on_top = True
    inlines = UserAdmin.inlines + [UserProfileInline, ApiKeyInline]


# un-/re-register default user admin
admin.site.unregister(User)
admin.site.register(User, UserModelAdmin)


class UserProfileAdmin(ForeignKeyAutocompleteAdmin):
    save_on_top = True

    list_display = ('user', 'user_email', 'email_confirmed', 'serial_number', )
    list_filter = ('email_confirmed', )
    search_fields = ('user__email', 'device__serial_number')

    def user_email(self, object):
        return object.user.email

    def serial_number(self, object):
        if object.device:
            return object.device.serial_number
        return 'No device'

    related_search_fields = {
        'user': ('email', ),
        'device': ('serial_number', ),
    }


admin.site.register(UserProfile, UserProfileAdmin)

