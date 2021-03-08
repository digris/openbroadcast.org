# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ac_tagging.widgets import TagAutocompleteTagIt
from alibrary.models import Relation, Label, Artist, LabelFoundingArtist
from alibrary.util.storage import get_file_from_url
from base.mixins import StripWhitespaceFormMixin
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Fieldset, Row, Column
from crispy_forms_extra.layout import LookupField, LookupImageField
from django import forms
from django.forms import ModelForm, Form
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.contrib.contenttypes.forms import (
    BaseGenericInlineFormSet,
    generic_inlineformset_factory,
)
from django.forms import ModelForm, Form
from django.forms.widgets import FileInput
from django.utils.translation import ugettext as _
from base.fields.widgets import ReadOnlyIconField
from tagging.forms import TagField

from search.forms import fields as search_fields

ACTION_LAYOUT = action_layout = FormActions(
    HTML(
        '<button type="submit" name="save" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-save icon-white"></i> Save</button>'
    ),
    HTML(
        '<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'
    ),
)
ACTION_LAYOUT_EXTENDED = action_layout = FormActions(
    Field("publish", css_class="input-hidden"),
    HTML(
        '<button type="submit" name="save" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-save icon-white"></i> Save</button>'
    ),
    HTML(
        '<button type="submit" name="save-and-publish" value="save" class="btn pull-right ajax_submit save-and-publish" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-bullhorn icon-white"></i> Save & Publish</button>'
    ),
    HTML(
        '<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'
    ),
)


class LabelActionForm(Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", False)
        super(LabelActionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.form_tag = False

        self.helper.add_layout(ACTION_LAYOUT)
        """
        if self.instance and self.instance.publish_date:
            self.helper.add_layout(ACTION_LAYOUT)
        else:
            self.helper.add_layout(ACTION_LAYOUT_EXTENDED)
        """

    publish = forms.BooleanField(required=False)

    def save(self, *args, **kwargs):
        return True


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = (
            "name",
            "type",
            "labelcode",
            "parent",
            "date_start",
            "date_end",
            "description",
            "address",
            "country",
            "phone",
            "fax",
            "email",
            "main_image",
            "d_tags",
        )

    def __init__(self, *args, **kwargs):

        self.user = kwargs["initial"]["user"]
        self.instance = kwargs["instance"]

        self.label = kwargs.pop("label", None)

        super(LabelForm, self).__init__(*args, **kwargs)

        """
        Prototype function, set some fields to readonly depending on permissions
        """
        """
        if not self.user.has_perm("alibrary.admin_release", self.instance):
            self.fields['catalognumber'].widget.attrs['readonly'] = 'readonly'
        """

        self.helper = FormHelper()
        self.helper.form_id = "id_feedback_form_%s" % "asd"
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.form_tag = False

        base_layout = Fieldset(
            _("General"),
            LookupField("name", css_class="input-xlarge"),
            LookupField("type", css_class="input-xlarge"),
            LookupField("labelcode", css_class="input-xlarge"),
            LookupField("parent", css_class="input-xlarge"),
        )

        activity_layout = Fieldset(
            _("Activity"),
            LookupField("date_start", css_class="input-xlarge"),
            LookupField("date_end", css_class="input-xlarge"),
        )

        contact_layout = Fieldset(
            _("Contact"),
            LookupField("address", css_class="input-xlarge"),
            LookupField("country", css_class="input-xlarge"),
            LookupField("phone", css_class="input-xlarge"),
            LookupField("fax", css_class="input-xlarge"),
            LookupField("email", css_class="input-xlarge"),
        )

        meta_layout = Fieldset(
            "Meta",
            LookupField("description", css_class="input-xxlarge"),
            LookupImageField("main_image"),
            LookupField("remote_image"),
        )

        tagging_layout = Fieldset("Tags", LookupField("d_tags"))

        layout = Layout(
            base_layout,
            activity_layout,
            contact_layout,
            HTML('<div id="founding_artist_container"></div>'),
            meta_layout,
            tagging_layout,
        )

        self.helper.add_layout(layout)

    main_image = forms.Field(widget=FileInput(), required=False)
    remote_image = forms.URLField(required=False)
    d_tags = TagField(
        widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_("Tags")
    )
    description = forms.CharField(widget=forms.Textarea(), required=False)
    parent = search_fields.AutocompleteField(
        "alibrary.label", allow_new=True, required=False, label=_("Parent Label")
    )

    def clean(self, *args, **kwargs):
        cd = super(LabelForm, self).clean()

        try:
            parent = cd["parent"]
            if not parent.pk:
                parent.creator = self.user
                parent.save()
        except:
            pass

        try:
            if parent.pk == self.instance.pk:
                self._errors["parent"] = self.error_class(
                    [_("The parent label can not be itself!")]
                )
        except:
            pass

        if cd.get("remote_image", None):
            remote_file = get_file_from_url(cd["remote_image"])
            if remote_file:
                cd["main_image"] = remote_file

        return cd

    def save(self, *args, **kwargs):
        return super(LabelForm, self).save(*args, **kwargs)


class BaseFoundingArtistFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs["instance"]
        super(BaseFoundingArtistFormSet, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        base_layout = Row(
            Column(Field("artist", css_class="input-xlarge"), css_class="span8"),
            Column(Field("DELETE", css_class="input-mini"), css_class="span4 delete"),
            css_class="albumartist-row row-fluid form-autogrow",
        )

        self.helper.add_layout(base_layout)


class BaseFoundingArtistForm(ModelForm):
    class Meta:
        model = LabelFoundingArtist
        parent_model = Artist
        fields = ["artist"]

    artist = search_fields.AutocompleteField(
        "alibrary.artist", allow_new=True, required=False, label=_("Artist")
    )

    def clean_artist(self):
        artist = self.cleaned_data["artist"]
        try:
            if not artist.pk:
                artist.save()
                return artist
        except:
            return None
        return artist

    def save(self, *args, **kwargs):
        instance = super(BaseFoundingArtistForm, self).save(*args, **kwargs)
        return instance


FoundingArtistFormSet = inlineformset_factory(
    Label,
    LabelFoundingArtist,
    form=BaseFoundingArtistForm,
    formset=BaseFoundingArtistFormSet,
    fk_name="label",
    extra=15,
    can_delete=True,
    can_order=False,
)


class BaseLabelReleationFormSet(BaseGenericInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs["instance"]
        super(BaseLabelReleationFormSet, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id_releasemediainline_form_%s" % "asdfds"
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.form_tag = False

        base_layout = Row(
            Column(
                Field("url", css_class="input-xlarge"), css_class="span6 relation-url"
            ),
            Column(Field("service", css_class="input-mini"), css_class="span4"),
            Column(Field("DELETE", css_class="input-mini"), css_class="span2"),
            css_class="row-fluid relation-row form-autogrow",
        )

        self.helper.add_layout(base_layout)


class BaseLabelReleationForm(StripWhitespaceFormMixin, ModelForm):
    class Meta:
        model = Relation
        parent_model = Label
        formset = BaseLabelReleationFormSet
        fields = ("url", "service")

    def __init__(self, *args, **kwargs):
        super(BaseLabelReleationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        self.fields["service"].widget.instance = instance
        if instance and instance.id:
            self.fields["service"].widget.attrs["readonly"] = True

    def clean_service(self):
        return self.instance.service

    service = forms.CharField(label="", widget=ReadOnlyIconField(), required=False)
    url = forms.URLField(label=_("Website / URL"), required=False)


LabelRelationFormSet = generic_inlineformset_factory(
    Relation,
    form=BaseLabelReleationForm,
    formset=BaseLabelReleationFormSet,
    extra=15,
    exclude=("action",),
    can_delete=True,
)
