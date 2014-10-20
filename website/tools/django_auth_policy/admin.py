import logging

from django import http
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.auth.views import password_change
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings

from django_auth_policy.models import PasswordChange, LoginAttempt, UserChange
from django_auth_policy.forms import (StrictAuthenticationForm,
                                      StrictPasswordChangeForm)


logger = logging.getLogger(__name__)


class LoginAttemptAdmin(admin.ModelAdmin):
    readonly_fields = ('username', 'source_address', 'hostname', 'successful',
                       'user', 'timestamp', 'lockout')
    list_display = ('username', 'source_address', 'successful', 'timestamp')
    list_filter = ('successful',)
    search_fields = ('username',)
    date_hierarchy = 'timestamp'
    actions = ('unlock',)

    def get_actions(self, request):
        # Disable deletion of login attempts
        actions = super(LoginAttemptAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        if not request.user.has_perm('django_auth_policy.unlock'):
            del actions['unlock']

        return actions

    def unlock(self, request, queryset):
        if not request.user.has_perm('django_auth_policy.unlock'):
            self.message_user(request, _('You don\'t have unlock permissions'))
            return
        count = LoginAttempt.objects.unlock_queryset(queryset)
        self.message_user(request, _('Unlocked %s failed attempts') % count)
    unlock.short_description = _('Unlock')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Do not actually save anything to prevent changes
        logger.info('Prevented change in LoginAttempt item by user %s',
                    request.user)


class PasswordChangeAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'timestamp', 'successful', 'is_temporary')
    list_display = ('user', 'successful', 'is_temporary', 'timestamp')
    list_filter = ('successful', 'is_temporary')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Do not actually save anything to prevent changes
        logger.info('Prevented change in PasswordChange item by user %s',
                    request.user)

    def get_actions(self, request):
        # Disable deletion of user changes action
        actions = super(PasswordChangeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class UserChangeAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'timestamp', 'by_user')
    list_display = ('user', 'by_user', 'timestamp')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # Do not actually save anything to prevent changes
        logger.info('Prevented change in UserChange item by user %s',
                    request.user)

    def get_actions(self, request):
        # Disable deletion of user changes action
        actions = super(UserChangeAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


def admin_login(request, extra_context=None):
    """ Redirects to default login view which enforces the authentication
    policy
    """
    q = REDIRECT_FIELD_NAME + '=' + request.get_full_path()
    return http.HttpResponseRedirect(reverse('login') + '?' + q)


def admin_password_change(request):
    """
    Handles the "change password" task -- both form display and validation.
    """
    to_url = reverse('admin:password_change_done', current_app=admin.site.name)
    defaults = {
        'current_app': admin.site.name,
        'post_change_redirect': to_url,
        'password_change_form': StrictPasswordChangeForm
    }
    if admin.site.password_change_template is not None:
        defaults['template_name'] = admin.site.password_change_template
    return password_change(request, **defaults)


admin.site.register(LoginAttempt, LoginAttemptAdmin)
admin.site.register(PasswordChange, PasswordChangeAdmin)
admin.site.register(UserChange, UserChangeAdmin)

admin.site.login = admin_login
admin.site.login_form = StrictAuthenticationForm
admin.site.password_change = admin_password_change

# django_auth_policy replaces the default Django auth UserAdmin to enforce
# authentication policies on the admin interface. Set this to False when
# django_auth_policy shouldn't replace UserAdmin.
replace_auth_user_admin = getattr(settings, 'REPLACE_AUTH_USER_ADMIN', True)

# UserAdmin is never replaced when a custom Auth model is in use
if replace_auth_user_admin and settings.AUTH_USER_MODEL == 'auth.User':
    # Import this here to avoid unwanted registering of django auth admin
    from django.contrib.auth import get_user_model
    from django_auth_policy.user_admin import StrictUserAdmin
    user_model = get_user_model()
    try:
        admin.site.unregister(user_model)
    except admin.sites.NotRegistered:
        logger.warning('Could not unregister django.contrib.auth User model '
                       'from admin site. Make sure your custom user admin '
                       'enforces all authentication policies and set '
                       'REPLACE_AUTH_USER_ADMIN to False.')
    else:
        admin.site.register(user_model, StrictUserAdmin)
