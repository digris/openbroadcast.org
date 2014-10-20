import logging
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from django_auth_policy.models import PasswordChange
from django_auth_policy.handlers import (PasswordStrengthPolicyHandler,
                                         AuthenticationPolicyHandler,
                                         PasswordChangePolicyHandler)


logger = logging.getLogger(__name__)


class StrictAuthenticationForm(AuthenticationForm):
    auth_policy = AuthenticationPolicyHandler()
    password_change_policy = PasswordChangePolicyHandler()

    def __init__(self, request, *args, **kwargs):
        """ Make request argument required
        """
        return super(StrictAuthenticationForm, self).__init__(
            request, *args, **kwargs)

    def clean(self):
        remote_addr = self.request.META['REMOTE_ADDR']
        host = self.request.get_host()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        attempt = self.auth_policy.pre_auth_checks(username, password,
                                                   remote_addr, host)

        self.user_cache = authenticate(username=username, password=password)
        attempt.user = self.user_cache

        self.auth_policy.post_auth_checks(attempt)

        self.password_change_policy.update_session(self.request, self.user_cache)

        return self.cleaned_data


class StrictSetPasswordForm(forms.Form):
    password_strength_policy = PasswordStrengthPolicyHandler()
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(StrictSetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password1(self):
        pw = self.cleaned_data.get('new_password1')
        self.password_strength_policy.validate(pw, self.user)
        return pw

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def is_valid(self):
        valid = super(StrictSetPasswordForm, self).is_valid()
        if self.is_bound:
            PasswordChange.objects.create(user=self.user, successful=valid,
                                          is_temporary=False)
            if valid:
                logger.info('Password change successful for user %s',
                            self.user)
            else:
                logger.info('Password change failed for user %s',
                            self.user)
        return valid

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class StrictPasswordChangeForm(StrictSetPasswordForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
        'password_unchanged': _("The new password must not be the same as "
                                "the old password"),
        }
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password1(self):
        pw = super(StrictPasswordChangeForm, self).clean_new_password1()

        # Check that old and new password differ
        if (self.cleaned_data.get('old_password') and
                self.cleaned_data['old_password'] == pw):

            raise forms.ValidationError(
                self.error_messages['password_unchanged'],
                'password_unchanged')

        return pw


StrictPasswordChangeForm.base_fields = OrderedDict(
    (k, StrictPasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)
