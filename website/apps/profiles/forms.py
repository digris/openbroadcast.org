# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ac_tagging.widgets import TagAutocompleteTagIt
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Fieldset, Div, Field, Row, Column
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from base.fields.extra import AdvancedFileInput
from pagedown.widgets import PagedownWidget
from profiles.models import Profile, Link, Service
from tagging.forms import TagField

ACTION_LAYOUT = action_layout = FormActions(
    HTML(
        '<button type="submit" name="save-i-classicon-arrow-upi" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-ok icon-white"></i> Save</button>'),
    HTML(
        '<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
)

class ActionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.add_layout(ACTION_LAYOUT)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'mentor', 'description')

        widgets = {
            'image': AdvancedFileInput(image_width=76),
            'expertise': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        appearance_layout = Layout(
            Fieldset(
                _('Appearance'),
                Field('pseudonym', css_class='input-xlarge'),
                # Field('description', css_class='input-xlarge'),
            )
        )

        profile_layout = Layout(
            Fieldset(
                _('Personal Information'),
                Div(
                    HTML('<p>%s</p>' % (_('Your birth date is only visible to your mentor, and to team-members with administrative rights.'))),
                    css_class='notes-form notes-inline notes-info',
                ),
                Field('gender', css_class='input-xlarge'),
                Field('birth_date', css_class='input-xlarge'),
                Field('biography', css_class='input-xlarge'),
                Div(
                    Field('image'),
                    css_class='input-image'
                )
            )
        )
        contact_layout = Layout(

            Fieldset(
                _('Contact'),
                Div(
                    HTML('<p>%s</p>' % (_('Except for "City" and "Country", this information is only visible to your mentor, and to team-members with administrative rights.'))),
                    css_class='notes-form notes-inline notes-info',
                ),
                Field('mobile', css_class='input-xlarge'),
                Field('phone', css_class='input-xlarge'),
                Field('fax', css_class='input-xlarge'),
                Field('address1', css_class='input-xlarge'),
                Field('address2', css_class='input-xlarge'),
                Field('state', css_class='input-xlarge'),
                Field('city', css_class='input-xlarge'),
                Field('zip', css_class='input-xlarge'),
                Field('country', css_class='input-xlarge'),
            )
        )
        account_layout = Layout(

            Fieldset(
                _('Accounts'),
                Div(
                    HTML('<p>%s</p>' % (_(
                        'In case you see a reason to recieve some money from us :) This information is not visible on the plattform.'))),
                    css_class='notes-form notes-inline notes-info',
                ),
                Field('iban', css_class='input-xlarge'),
                Field('paypal', css_class='input-xlarge'),
            )
        )
        settings_layout = Layout(

            Fieldset(
                _('Settings'),
                # Div(
                #        HTML('<h2>%s</h2><p>%s</p>' % (_('Account data'), _('In case you see a reason to recieve some money from us :) This information is not visible on the plattform.'))),
                #        css_class='notes-form notes-inline notes-info',
                # ),
                Field('enable_alpha_features', css_class='input-xlarge'),
            )
        )
        skills_layout = Layout(

            Fieldset(
                _('Skills & Knowledge'),
                Field('expertise', css_class='input-xlarge'),

            )
        )

        tagging_layout = Fieldset(
            'Tags',
            'd_tags',
        )

        layout = Layout(
            appearance_layout,
            profile_layout,
            contact_layout,
            account_layout,
            tagging_layout,
            skills_layout,
            settings_layout,
        )

        self.helper.add_layout(layout)

    biography = forms.CharField(widget=PagedownWidget(), required=False)
    d_tags = TagField(widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_('Tags'))

    def clean_user(self):
        return self.instance.user


class LinkForm(ModelForm):
    class Meta:
        model = Link
        parent_model = Profile
        exclude = []

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_profile = Layout(
            Fieldset(
                _('Link'),
                'url',
                'title',
                'DELETE',
            )
        )

        base_layout = Row(
            Column(
                Field('url', css_class='input-medium'),
                css_class='span5'
            ),
            Column(
                Field('title', css_class='input-medium'),
                css_class='span5'
            ),
            Column(
                Field('DELETE', css_class='input-mini'),
                css_class='span2 delete'
            ),
            css_class='row-fluid link-row form-autogrow',
        )

        self.helper.add_layout(base_layout)


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        parent_model = Profile
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        layout_profile = Layout(
            Fieldset(
                _('Link'),
                'url',
                'title',
                'DELETE',
            )
        )

        base_layout = Row(
            Column(
                Field('username', css_class='input-medium'),
                css_class='span5'
            ),
            Column(
                Field('service', css_class='input-medium'),
                css_class='span5'
            ),
            Column(
                Field('DELETE', css_class='input-mini'),
                css_class='span2 delete'
            ),
            css_class='row-fluid service-row form-autogrow',
        )

        self.helper.add_layout(base_layout)

LinkFormSet = inlineformset_factory(Profile, Link, form=LinkForm, extra=15)
ServiceFormSet = inlineformset_factory(Profile, Service, form=ServiceForm, extra=15)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            #'username',
            'email'
        )
        help_texts = {
            'username': _('Letters, digits and @/./+/-/_ only'),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('User Details'),
                #Field('username', css_class='input-xlarge'),
                Field('email', css_class='input-xlarge'),
                Field('first_name', css_class='input-xlarge'),
                Field('last_name', css_class='input-xlarge'),
            )
        )
        super(UserForm, self).__init__(*args, **kwargs)







class UserCredentialsForm(ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput,
                                    required=False,
                                    help_text=_("Please make sure to use a 'not so easy to guess' password!"))
    new_password2 = forms.CharField(label=_("Confirmation"),
                                    widget=forms.PasswordInput,
                                    required=False,
                                    help_text=_("Verify your new password"))

    class Meta:
        model = User
        fields = (
            'username',
        )
        help_texts = {
            'username': _('Letters, digits and @/./+/-/_ only'),
        }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                _('Username / a.k.a. "Login Name"'),
                Field('username', css_class='input-xlarge'),
            ),
            Fieldset(
                _('Update Password'),
                Field('new_password1', css_class='input-xlarge'),
                Field('new_password2', css_class='input-xlarge'),
            )
        )
        super(UserCredentialsForm, self).__init__(*args, **kwargs)

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






