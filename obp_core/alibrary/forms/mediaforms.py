import logging

from ac_tagging.widgets import TagAutocompleteTagIt
from alibrary.models import Media, Relation, MediaExtraartists, MediaArtists
from base.mixins import StripWhitespaceFormMixin
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Fieldset, Row, Column
from crispy_forms_extra.layout import LookupField
from django import forms
from django.contrib.contenttypes.forms import (
    BaseGenericInlineFormSet,
    generic_inlineformset_factory,
)
from django.forms import ModelForm, Form
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from base.fields.widgets import ReadOnlyIconField
from tagging.forms import TagField

from search.forms import fields as search_fields

log = logging.getLogger(__name__)

MAX_TRACKNUMBER = 300 + 1

ACTION_LAYOUT = action_layout = FormActions(
    HTML(
        '<button type="submit" name="save" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi">Save</button>'
    ),
    HTML(
        '<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset">Cancel</button>'
    ),
)


class MediaActionForm(Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", False)
        super().__init__(*args, **kwargs)

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


class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = (
            "name",
            "description",
            "lyrics",
            "lyrics_language",
            "artist",
            "tracknumber",
            "medianumber",
            "opus_number",
            "mediatype",
            "version",
            # 'filename',
            "license",
            "release",
            "d_tags",
            "isrc",
        )

    def __init__(self, *args, **kwargs):

        self.user = kwargs["initial"]["user"]
        self.instance = kwargs["instance"]

        self.label = kwargs.pop("label", None)

        super().__init__(*args, **kwargs)

        """
        Prototype function, set some fields to readonly depending on permissions
        """
        # if not self.user.has_perm("alibrary.admin_release", self.instance) and self.instance.release and self.instance.release.publish_date:
        if not self.user.has_perm("alibrary.admin_release", self.instance):
            # self.fields['license'].widget.attrs['disabled'] = 'disabled'
            self.fields["license"].widget.attrs["readonly"] = "readonly"

        self.helper = FormHelper()
        self.helper.form_tag = False

        # rewrite labels
        self.fields["medianumber"].label = "Disc number"
        self.fields["opus_number"].label = "Opus N."
        # self.fields['filename'].label = 'Orig. Filename'

        base_layout = Fieldset(
            "General",
            LookupField("name", css_class="input-xlarge"),
            LookupField("release", css_class="input-xlarge"),
            LookupField("artist", css_class="input-xlarge"),
            LookupField("mediatype", css_class="input-xlarge"),
            LookupField("tracknumber", css_class="input-xlarge"),
            Field("medianumber", css_class="input-xlarge"),
            Field("opus_number", css_class="input-xlarge"),
            Field("version", css_class="input-xlarge"),
            HTML(
                f'<div style="opacity: 0.5;"><span style="padding: 0 44px 0 0;">Orig. Filename:</span>{self.instance.original_filename}</div>'
            ),
        )

        identifiers_layout = Fieldset(
            "Identifiers", LookupField("isrc", css_class="input-xlarge")
        )

        license_layout = Fieldset(
            "License/Source", Field("license", css_class="input-xlarge")
        )

        meta_layout = Fieldset(
            "Meta", LookupField("description", css_class="input-xlarge")
        )

        lyrics_layout = Fieldset(
            "Lyrics",
            LookupField("lyrics_language", css_class="input-xlarge"),
            LookupField("lyrics", css_class="input-xlarge"),
        )

        tagging_layout = Fieldset("Tags", LookupField("d_tags"))

        layout = Layout(
            base_layout,
            HTML('<div id="artist_relation_container"></div>'),
            identifiers_layout,
            license_layout,
            meta_layout,
            lyrics_layout,
            tagging_layout,
        )

        self.helper.add_layout(layout)

    d_tags = TagField(
        widget=TagAutocompleteTagIt(max_tags=9), required=False, label="Tags"
    )
    release = search_fields.AutocompleteField(
        "alibrary.release", allow_new=True, required=False, label="Release"
    )

    name = forms.CharField(required=True, label="Title")
    artist = search_fields.AutocompleteField(
        "alibrary.artist", allow_new=True, required=False, label="Artist"
    )
    description = forms.CharField(widget=forms.Textarea(), required=False)

    def clean_license(self):
        instance = getattr(self, "instance", None)
        if (
            instance
            and instance.pk
            and not self.user.has_perm("alibrary.admin_release", instance)
        ):
            return instance.license
        else:
            return self.cleaned_data["license"]

    def clean(self, *args, **kwargs):

        cd = super().clean()

        # hack. allow_new in AutoCompleteSelectField does _not_ automatically create new objects???
        try:
            artist = cd["artist"]
            if not artist.pk:
                artist.creator = self.user
                artist.save()
        except BaseException:
            pass

        try:
            release = cd["release"]
            if not release.pk:
                release.creator = self.user
                release.save()

        except BaseException:
            pass

        return cd

    # TODO: take a look at save
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


"""
Album Artists
"""


class BaseExtraartistFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):

        self.instance = kwargs["instance"]

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id_artists_form_{}".format("inline")
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.form_tag = False

        base_layout = Row(
            Column(Field("profession"), css_class="span3"),
            Column(Field("artist"), css_class="span5"),
            Column(Field("DELETE", css_class="input-mini"), css_class="span4"),
            css_class="extraartist-row row-fluid form-autogrow",
        )

        self.helper.add_layout(base_layout)


class BaseExtraartistForm(ModelForm):
    class Meta:
        model = MediaExtraartists
        parent_model = Media
        fields = ("artist", "profession")
        # labels in django 1.6 only... leave them here for the future...
        labels = {"profession": "Credited as"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _unused = getattr(self, "instance", None)

        self.fields["profession"].label = "Credited as"

    artist = search_fields.AutocompleteField(
        "alibrary.artist", allow_new=True, required=False, label="Artist"
    )

    def clean_artist(self):

        artist = self.cleaned_data["artist"]
        try:
            if not artist.pk:
                log.debug("saving not existant artist: %s", artist.name)
                artist.save()
            return artist
        except BaseException:
            return None


"""
Media Artists
"""


class BaseMediaartistFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):

        self.instance = kwargs["instance"]

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id_artists_form_{}".format("inline")
        self.helper.form_class = "form-horizontal"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.form_tag = False

        base_layout = Row(
            Column(Field("join_phrase"), css_class="span3"),
            Column(Field("artist"), css_class="span5"),
            Column(Field("DELETE", css_class="input-mini"), css_class="span4"),
            css_class="mediaartist-row row-fluid form-autogrow",
        )

        self.helper.add_layout(base_layout)


class BaseMediaartistForm(ModelForm):
    class Meta:
        model = MediaArtists
        parent_model = Media
        fields = ("artist", "join_phrase", "position")

    def clean_artist(self):
        artist = self.cleaned_data["artist"]
        if not artist.pk:
            artist.save()

        return artist

    artist = search_fields.AutocompleteField(
        "alibrary.artist", allow_new=True, required=False
    )


class BaseMediaReleationFormSet(BaseGenericInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs["instance"]
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id_releasemediainline_form_{}".format("asdfds")
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


class BaseMediaReleationForm(StripWhitespaceFormMixin, ModelForm):
    class Meta:
        model = Relation
        parent_model = Media
        formset = BaseMediaReleationFormSet
        fields = ("url", "service")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        self.fields["service"].widget.instance = instance
        if instance and instance.id:
            self.fields["service"].widget.attrs["readonly"] = True

    def clean_service(self):
        return self.instance.service

    service = forms.CharField(label="", widget=ReadOnlyIconField(), required=False)
    url = forms.URLField(label="Website / URL", required=False)


# Compose Formsets
MediaRelationFormSet = generic_inlineformset_factory(
    Relation,
    form=BaseMediaReleationForm,
    formset=BaseMediaReleationFormSet,
    extra=15,
    exclude=("action",),
    can_delete=True,
)

MediaartistFormSet = inlineformset_factory(
    Media,
    MediaArtists,
    form=BaseMediaartistForm,
    formset=BaseMediaartistFormSet,
    extra=15,
    exclude=("position",),
    can_delete=True,
    can_order=False,
)

ExtraartistFormSet = inlineformset_factory(
    Media,
    MediaExtraartists,
    form=BaseExtraartistForm,
    formset=BaseExtraartistFormSet,
    fk_name="media",
    extra=15,
    # exclude=('position',),
    can_delete=True,
    can_order=False,
)
