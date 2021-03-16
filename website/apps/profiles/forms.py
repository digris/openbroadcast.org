# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _


from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Fieldset, Div, Field, Row, Column
from crispy_forms_vue.layout import Cell, Grid, InputContainer, TagInputContainer

from tagging.forms import TagField
from tagging_extra.widgets import TagAutocompleteWidget
from ac_tagging.widgets import TagAutocompleteTagIt

from base.fields.extra import AdvancedFileInput
from profiles.models import Profile, Link, Service

ACTION_LAYOUT = action_layout = FormActions(
    HTML(
        '<button type="submit" name="save-i-classicon-arrow-upi" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-ok icon-white"></i> Save</button>'
    ),
    HTML(
        '<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'
    ),
)


class ActionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.form_tag = False
        self.helper.add_layout(ACTION_LAYOUT)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("user", "mentor", "description", "fax", "d_tags")

        widgets = {
            "image": AdvancedFileInput(image_width=100),
            "expertise": forms.CheckboxSelectMultiple(),
            # "birth_date": forms.TextInput(attrs={"type": "date"}),
            # "tags": TagAutocompleteWidget(required=False, label=_("Tags"), options={'max_tags': 9}),
        }

    # d_tags = TagField(
    #     # widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_("Tags"),
    #     # NOTE: see `instance` in `__init__` below.
    #     widget=TagAutocompleteWidget(required=False, label=_("Tags"), options={'max_tags': 9})
    # )

    tags = TagField(required=False, label=_("Tags"))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)

        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.fields['d_tags'].widget.instance = instance

        appearance_layout = Layout(
            Fieldset(
                _("Appearance"),
                InputContainer("pseudonym"),
            )
        )

        profile_layout = Layout(
            Fieldset(
                _("Personal Information"),
                Div(
                    HTML(
                        "Your birth date is only visible to your mentor, and to team-members with administrative rights."
                    ),
                    css_class="fieldset-hint fieldset-hint--info",
                ),
                Grid(
                    Cell(InputContainer("gender")),
                    Cell(InputContainer("birth_date")),
                ),
                InputContainer("biography"),
                InputContainer("image"),
            )
        )
        contact_layout = Layout(
            Fieldset(
                _("Contact"),
                Div(
                    HTML(
                        'Except for "City" and "Country", this information is only visible to your mentor, and to team-members with administrative rights.'
                    ),
                    css_class="fieldset-hint fieldset-hint--info",
                ),
                Grid(
                    Cell(InputContainer("address1")),
                ),
                Grid(
                    Cell(InputContainer("address2")),
                ),
                Grid(
                    Cell(InputContainer("city")),
                    Cell(InputContainer("zip")),
                    Cell(InputContainer("country")),
                ),
                Grid(
                    Cell(InputContainer("mobile")),
                    Cell(InputContainer("phone")),
                    Cell(InputContainer("skype")),
                ),
            )
        )
        account_layout = Layout(
            Fieldset(
                _("Accounts"),
                Div(
                    HTML(
                        "In case you see a reason to recieve some money from us :) This information is not visible on the plattform."
                    ),
                    css_class="fieldset-hint fieldset-hint--info",
                ),
                Grid(
                    Cell(InputContainer("iban")),
                    Cell(InputContainer("paypal")),
                ),
            )
        )
        settings_layout = Layout(
            Fieldset(
                _("Settings"),
                InputContainer("enable_alpha_features"),
                InputContainer("settings_show_media_history"),
                InputContainer("settings_show_media_appearances"),
            )
        )
        skills_layout = Layout(
            Fieldset(
                _("Skills & Knowledge"), InputContainer("expertise", hide_label=True)
            )
        )

        # tagging_layout = Fieldset("Tags", "d_tags")
        tagging_layout = Layout(
            # Fieldset(
            #     _("Tags"),
            #     InputContainer("d_tags", hide_label=True)
            # ),
            Fieldset(_("Tags"), TagInputContainer("tags", hide_label=True))
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

    def clean_user(self):
        return self.instance.user

    def clean_tags(self):
        c_tags = self.cleaned_data["tags"]
        print("c_tags", c_tags)
        return c_tags
        # return self.cleaned_data["tags"].lower()
        # tags = self.cleaned_data["tags"]
        # if len(tags) < 3:
        #     return None
        #
        # print('---', tags)
        #
        # return tags.lower()


class LinkForm(ModelForm):
    class Meta:
        model = Link
        parent_model = Profile
        exclude = []

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        base_layout = Grid(
            Cell(InputContainer("url")),
            Cell(InputContainer("title")),
            Cell(InputContainer("DELETE")),
            data_autogrow="autogrow",
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
        layout_profile = Layout(Fieldset(_("Link"), "url", "title", "DELETE"))

        base_layout = Row(
            Column(Field("username", css_class="input-medium"), css_class="span5"),
            Column(Field("service", css_class="input-medium"), css_class="span5"),
            Column(Field("DELETE", css_class="input-mini"), css_class="span2 delete"),
            css_class="row-fluid service-row form-autogrow",
        )

        self.helper.add_layout(base_layout)


LinkFormSet = inlineformset_factory(Profile, Link, form=LinkForm, extra=15)
ServiceFormSet = inlineformset_factory(Profile, Service, form=ServiceForm, extra=15)


class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")
        help_texts = {"username": _("Letters, digits and @/./+/-/_ only")}

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                _("User Details"),
                InputContainer("email"),
                Grid(
                    Cell(InputContainer("first_name")),
                    Cell(InputContainer("last_name")),
                ),
            )
        )
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            get_user_model()
            .objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("This e-mail address is already in use.")

        return email


class UserCredentialsForm(ModelForm):

    error_messages = {"password_mismatch": _("The two password fields didn't match.")}
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        required=False,
        # help_text=_("Please make sure to use a 'not so easy to guess' password!"),
    )
    new_password2 = forms.CharField(
        label=_("Confirmation"),
        widget=forms.PasswordInput,
        required=False,
        # help_text=_("Verify your new password"),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email")
        help_texts = {"username": _("Letters, digits and @/./+/-/_ only")}

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                _('Email & Username/"Login Name"'),
                InputContainer("email"),
                InputContainer("username"),
            ),
            Fieldset(
                _("Update Password"),
                Grid(
                    Cell(InputContainer("new_password1")),
                    Cell(InputContainer("new_password2")),
                ),
            ),
        )
        super(UserCredentialsForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if (
            get_user_model()
            .objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("This e-mail address is already in use.")

        return email

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages["password_mismatch"], code="password_mismatch"
                )
        return password2
