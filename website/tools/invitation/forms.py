# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Fieldset, Div
from crispy_forms_extra.layout import Row, Column, LookupField, LookupImageField

from registration.forms import RegistrationForm


def save_user(form_instance):
    """
    Create a new **active** user from form data.

    This method is intended to replace the ``save`` of
    ``django-registration``s ``RegistrationForm``. Required form fields
    are ``username``, ``email`` and ``password1``.
    """
    username = form_instance.cleaned_data['username']
    email = form_instance.cleaned_data['email']
    password = form_instance.cleaned_data['password1']
    new_user = User.objects.create_user(username, email, password)
    new_user.save()
    return new_user


class InvitationForm(forms.Form):

    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False

        self.helper.add_layout(Layout(


            Field('email', css_class='input-xlarge'),
            Field('message', css_class='input-xlarge'),
        ))



    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('A user with the e-mail address {} already exists.'.format(data))

        return data


class RegistrationFormInvitation(RegistrationForm):
    """
    Subclass of ``registration.RegistrationForm`` that create an **active**
    user.

    Since registration is (supposedly) done via invitation, no further
    activation is required. For this reason ``email`` field always return
    the value of ``email`` argument given the constructor.
    """
    def __init__(self, email, *args, **kwargs):
        super(RegistrationFormInvitation, self).__init__(*args, **kwargs)
        self._make_email_immutable(email)

    def _make_email_immutable(self, email):
        self._email = self.initial['email'] = email
        if 'email' in self.data:
            self.data = self.data.copy()
            self.data['email'] = email
        self.fields['email'].widget.attrs.update({'readonly': True})

    def clean_email(self):
        return self._email

    save = save_user
