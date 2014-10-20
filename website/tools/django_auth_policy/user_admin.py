import logging

from django import forms
from django import template
from django import http
from django.conf.urls import patterns, url
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django_auth_policy.models import PasswordChange, LoginAttempt, UserChange
from django_auth_policy import signals


logger = logging.getLogger(__name__)

user_model = get_user_model()


class StrictUserCreationForm(forms.ModelForm):
    """Alternative for Djangos UserCreationForm but doesn't set password
    and allows editing email and name right from the start"""
    error_messages = UserCreationForm.error_messages
    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or "
                                            "fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    'invalid': _("This value may contain only "
                                                 "letters, numbers and "
                                                 "@/./+/-/_ characters.")})

    class Meta:
        model = user_model
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(StrictUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class StrictUserAdmin(UserAdmin):
    """ Django user admin that enforces policies of django_auth_policy

    * Removes ability to set passwords of other users;
    * Adds ability to generate a temporary password;
    * Adds ability to unlock usernames / IP addresses;
    * Adds ability to re-activate disabled users;
    * Disables users that expired
    """
    readonly_fields = ('last_login', 'date_joined')
    add_form = StrictUserCreationForm
    add_fieldsets = ((None, {'classes': ('wide',),
                             'fields': ('username', 'email', 'first_name',
                                        'last_name')}),)
    list_display = ('username', 'email', 'is_active', 'last_login', 'is_staff')

    actions = ['reactivate_users', 'unlock_username',
               'temporary_password_action']

    def get_actions(self, request):
        # Disable deletion of users, because this would alter LoginAttempt and
        # PasswordChange history
        actions = super(StrictUserAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def unlock_username(self, request, queryset):
        LoginAttempt.objects.filter(username__in=queryset.values('username'),
                                    lockout=True).update(lockout=False)

        self.message_user(request, _('Unlocked selected usernames'))
    unlock_username.short_description = _('Unlock usernames of users')

    def reactivate_users(self, request, queryset):
        fixed = queryset.filter(is_active=False
                                ).update(is_active=True,
                                         last_login=timezone.now())
        self.message_user(request, _('%s users were (re)activated') % fixed)
    reactivate_users.short_description = _('(Re)activate users')

    def get_urls(self):
        urls = super(StrictUserAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^password/$',
                self.admin_site.admin_view(self.set_temporary_password),
                name='set_temporary_password'),
            url(r'^(\d+)/password/$',
                self.admin_site.admin_view(self.user_change_password))
            )
        return my_urls + urls

    def temporary_password_action(self, request, queryset):
        user_ids = ['pk=' + str(i) for i in queryset.values_list('pk',
                                                                 flat=True)]
        return http.HttpResponseRedirect(
            reverse('admin:set_temporary_password') + '?' + '&'.join(user_ids))
    temporary_password_action.short_description = _('Set temporary password')

    def user_change_password(self, request, user_id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        return http.HttpResponseRedirect(
            reverse('admin:set_temporary_password') + '?pk=' + str(user_id))

    def set_temporary_password(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied

        if not request.GET.get('pk', False):
            return http.HttpResponseRedirect(
                reverse('admin:auth_user_changelist'))

        users = user_model.objects.filter(pk__in=request.GET.getlist('pk'))
        if request.method == 'POST':
            passwords = []
            for user in users:
                password = PasswordChange.objects.set_temporary_password(user)
                passwords.append((user, password))

                signals.temporary_password_set.send(sender=user, user=user,
                                                    request=request,
                                                    password=password)

            return template.response.TemplateResponse(request,
                'admin/django_auth_policy/set_temporary_password.html',
                {'passwords': passwords})

        return template.response.TemplateResponse(request,
            'admin/django_auth_policy/confirm_temporary_password.html',
            {'for_users': users})

    def save_model(self, request, obj, form, change):
        obj.save()
        UserChange.objects.create(user=obj, by_user=request.user)
