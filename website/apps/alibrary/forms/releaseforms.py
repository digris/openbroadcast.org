# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from ac_tagging.widgets import TagAutocompleteTagIt
from base.mixins import StripWhitespaceFormMixin
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Fieldset, Div
from crispy_forms_extra.layout import Row, Column, LookupField, LookupImageField
from django import forms
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet, generic_inlineformset_factory
from django.forms import ModelForm, Form
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext as _
from django_date_extensions.fields import ApproximateDateFormField
from base.fields.extra import AdvancedFileInput
from base.fields.widgets import ReadOnlyIconField
from tagging.forms import TagField

from search.forms import fields as search_fields

from ..models import Release, Relation, Media, License, Label, ReleaseAlbumartists
from ..util.storage import get_file_from_url

log = logging.getLogger(__name__)

ACTION_LAYOUT = FormActions(
    HTML('<button type="submit" name="save" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-save icon-white"></i> Save</button>'),
    HTML('<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
)


MAX_TRACKNUMBER = 100 + 1


class ReleaseActionForm(Form):

    publish = forms.BooleanField(label=_('Save & Publish'), required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', False)
        super(ReleaseActionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_layout(ACTION_LAYOUT)

    def clean(self, *args, **kwargs):

        cd = super(ReleaseActionForm, self).clean()
        publish = cd.get('publish', False)

        if publish:
            missing_licenses = []
            for media in self.instance.get_media():
                if not media.license:
                    missing_licenses.append(_('No license set for "%s"' % media.name))

            if len(missing_licenses) > 0:
                self._errors['publish'] = self.error_class(missing_licenses)
                del cd['publish']

        return cd


    def save(self, *args, **kwargs):
        return True




"""
Bulk edit - Autocomplete for fields to apply on whole listing
"""
class ReleaseBulkeditForm(Form):

    def __init__(self, *args, **kwargs):

        self.instance = kwargs.pop('instance', False)
        self.disable_license = False

        """
        # publishing removed
        if self.instance and self.instance.publish_date:
            self.disable_license = True
        """
        super(ReleaseBulkeditForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False

        form_class = 'input-xlarge'
        if self.disable_license:
            form_class = 'hidden'

        base_layout = Div(
                Div(HTML('<p>"%s": %s</p>' % (_('Bulk Edit'), _('Choose Artist name and/or license to apply on each track.')))),
                Row(
                    Column(
                           Field('bulk_artist_name', css_class='input-xlarge'),
                           css_class='main'
                           ),
                    Column(
                           HTML('<button type="button" id="bulk_apply_artist_name" value="apply" class="btn btn-mini pull-right bulk_apply" id="submit-"><i class="icon-plus"></i> %s</button>' % _('Apply Artist to all tracks')),
                           css_class='side'
                           ),
                    css_class='bulkedit-row row-fluid',
                ),
                Row(
                    Column(
                           Field('bulk_license', css_class=form_class),
                           css_class='main'
                           ),
                    Column(
                           HTML('<button type="button" id="bulk_apply_license" value="apply" class="btn btn-mini pull-right bulk_apply" id="submit-"><i class="icon-plus"></i> %s</button>' % _('Apply License to all tracks')),
                           css_class='side'
                           ),
                    css_class='bulkedit-row row-fluid',
                ),
                css_class='bulk_edit',
        )

        self.helper.add_layout(base_layout)

    bulk_artist_name = search_fields.AutocompleteField('alibrary.artist', allow_new=True, required=False, label=_('Artist'))
    bulk_license = forms.ModelChoiceField(queryset=License.objects.filter(selectable=True), required=False, label=_('License'))

    def save(self, *args, **kwargs):
        return True



class ReleaseForm(ModelForm):

    class Meta:
        model = Release
        fields = ('name',
                  'label',
                  'releasetype',
                  'totaltracks',
                  'release_country',
                  'catalognumber',
                  'description',
                  'main_image',
                  'releasedate_approx',
                  'd_tags',
                  'barcode',)


    def __init__(self, *args, **kwargs):

        self.user = kwargs['initial']['user']
        self.instance = kwargs['instance']
        self.label = kwargs.pop('label', None)

        super(ReleaseForm, self).__init__(*args, **kwargs)

        """
        Prototype function, set some fields to readonly depending on permissions
        """
        if not self.user.has_perm("alibrary.admin_release", self.instance):
            self.fields['catalognumber'].widget.attrs['readonly'] = 'readonly'


        self.helper = FormHelper()
        self.helper.form_id = "id_feedback_form_%s" % 'asd'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False

        # TODO: this is very ugly!
        unknown_label, c = Label.objects.get_or_create(slug='unknown')
        if c:
            Label.objects.filter(pk=unknown_label.pk).update(
                name='Unknown label',
                slug='unknown'
            )

        noton_label, c = Label.objects.get_or_create(slug='not-on-label-self-released')
        if c:
            Label.objects.filter(pk=unknown_label.pk).update(
                name='Not on Label / Self Released',
                slug='not-on-label-self-released'
            )

        base_layout = Fieldset(
            _('General'),
            LookupField('name', css_class='input-xlarge'),
            LookupField('releasetype', css_class='input-xlarge'),
            LookupField('totaltracks', css_class='input-xlarge'),
        )

        catalog_layout = Fieldset(
            _('Label/Catalog'),
            LookupField('label', css_class='input-xlarge'),
            HTML("""<ul class="horizontal unstyled clearfix action label-select">
                <li><a data-label="%s" data-label_id="%s" href="#"><i class="icon-double-angle-right"></i> %s</a></li>
                <li><a data-label="%s" data-label_id="%s" href="#"><i class="icon-double-angle-right"></i> %s</a></li>
            </ul>""" % (unknown_label.name, unknown_label.pk, unknown_label.name, noton_label.name, noton_label.pk, noton_label.name)),
            LookupField('catalognumber', css_class='input-xlarge'),
            LookupField('release_country', css_class='input-xlarge'),
            LookupField('releasedate_approx', css_class='input-xlarge'),
        )

        meta_layout = Fieldset(
            'Meta',
            LookupField('description', css_class='input-xxlarge'),
            LookupImageField('main_image',),
            LookupField('remote_image',),
        )

        tagging_layout = Fieldset(
            'Tags',
            LookupField('d_tags'),
        )

        identifiers_layout = Fieldset(
            _('Identifiers'),
            LookupField('barcode', css_class='input-xlarge'),
        )

        layout = Layout(
            base_layout,
            HTML('<div id="artist_relation_container"></div>'),
            meta_layout,
            catalog_layout,
            identifiers_layout,
            tagging_layout,
        )

        self.helper.add_layout(layout)


    main_image = forms.Field(widget=AdvancedFileInput(), required=False)
    remote_image = forms.URLField(required=False)
    releasedate_approx = ApproximateDateFormField(label="Releasedate", required=False)
    d_tags = TagField(widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_('Tags'))

    label = search_fields.AutocompleteField('alibrary.label', allow_new=True, required=False)

    description = forms.CharField(widget=forms.Textarea(), required=False)



    # TODO: rework clean function
    def clean(self, *args, **kwargs):

        cd = super(ReleaseForm, self).clean()

        try:
            label = cd['label']
            if not label.pk:
                label.creator = self.user
                label.save()
        except:
            pass

        if cd.get('remote_image', None):
            remote_file = get_file_from_url(cd['remote_image'])
            if remote_file:
                cd['main_image'] = remote_file

        return cd

    def save(self, *args, **kwargs):
        return super(ReleaseForm, self).save(*args, **kwargs)





class BaseReleaseMediaFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(BaseReleaseMediaFormSet, self).__init__(*args, **kwargs)



class BaseReleaseMediaForm(ModelForm):

    class Meta:
        model = Media
        parent_model = Release
        exclude = []


    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(BaseReleaseMediaForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        base_layout = Row(
                Column(
                       Field('tracknumber', css_class='input-small'),
                       Field('mediatype', css_class='input-small'),
                       Field('license', css_class='input-small'),
                       HTML('<div><span style="padding-right: 68px;">&nbsp;</span><a href="%s"><i class="icon icon-edit"></i> Edit Track</a></div>' % self.instance.get_edit_url()),
                       css_class='span3'
                       ),
                Column(
                        LookupField('name', css_class='input-large'),
                        LookupField('artist', css_class='input-large'),
                        LookupField('isrc', css_class='input-large'),
                        HTML('<div style="opacity: 0.5;"><span style="padding-right: 48px;">File:</span>%s</div>' % self.instance.filename),
                       css_class='span9'
                       ),
                css_class='releasemedia-row row-fluid',
        )

        self.helper.add_layout(base_layout)


    artist = search_fields.AutocompleteField('alibrary.artist', allow_new=True, required=False)
    TRACKNUMBER_CHOICES =  [('', '---')] + list(((str(x), x) for x in range(1, 301)))
    tracknumber =  forms.ChoiceField(label=_('No.'), required=False, choices=TRACKNUMBER_CHOICES)

    def clean(self, *args, **kwargs):
        cd = super(BaseReleaseMediaForm, self).clean()

        try:
            cd['tracknumber'] = int(cd['tracknumber'])
        except:
            cd['tracknumber'] = None

        return cd



class BaseAlbumartistFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(BaseAlbumartistFormSet, self).__init__(*args, **kwargs)


class BaseAlbumartistForm(ModelForm):

    class Meta:
        model = ReleaseAlbumartists
        parent_model = Release
        fields = ('artist', 'join_phrase', 'position',)

    def __init__(self, *args, **kwargs):
        instance = getattr(self, 'instance', None)
        super(BaseAlbumartistForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        base_layout = Row(
                Column(
                       Field('join_phrase'),
                       css_class='span3'
                       ),
                Column(
                       Field('artist'),
                       css_class='span5'
                       ),
                Column(
                       Field('DELETE'),
                       css_class='span4 delete'
                       ),
                css_class='albumartist-row row-fluid form-autogrow',
        )

        self.helper.add_layout(base_layout)

    def clean_artist(self):
        artist = self.cleaned_data['artist']
        if artist and not artist.pk:
            log.debug('saving not existant artist: %s' % artist.name)
            artist.save()
        return artist

    artist = search_fields.AutocompleteField('alibrary.artist', allow_new=True, required=False)



class BaseReleaseReleationFormSet(BaseGenericInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(BaseReleaseReleationFormSet, self).__init__(*args, **kwargs)


class BaseReleaseReleationForm(StripWhitespaceFormMixin, ModelForm):

    class Meta:
        model = Relation
        parent_model = Release
        fields = ('url','service')

    def __init__(self, *args, **kwargs):
        super(BaseReleaseReleationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['service'].widget.instance = instance
        if instance and instance.id:
            self.fields['service'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_tag = False

        base_layout = Row(
                Column(
                       Field('url', css_class='input-xlarge'),
                       css_class='span6 relation-url'
                       ),
                Column(
                       Field('service', css_class='input-mini'),
                       css_class='span4'
                       ),
                Column(
                       Field('DELETE', css_class='input-mini'),
                       css_class='span2 delete'
                       ),
                css_class='row-fluid relation-row form-autogrow',
        )

        self.helper.add_layout(base_layout)

    def clean_service(self):
        return self.instance.service

    service = forms.CharField(label='', widget=ReadOnlyIconField(**{'url': 'whatever'}), required=False)
    url = forms.URLField(label=_('Website / URL'), required=False)


# Compose Formsets
ReleaseMediaFormSet = inlineformset_factory(
    Release,
    Media,
    form=BaseReleaseMediaForm,
    formset=BaseReleaseMediaFormSet,
    can_delete=False,
    extra=0,
    fields=[
        'name',
        'tracknumber',
        'isrc',
        'artist',
        'license',
        'mediatype',
    ],
    can_order=False
)

AlbumartistFormSet = inlineformset_factory(
    Release,
    ReleaseAlbumartists,
    form=BaseAlbumartistForm,
    formset=BaseAlbumartistFormSet,
    extra=15,
    exclude=[
        'position',
    ],
    can_delete=True,
    can_order=False,
)

ReleaseRelationFormSet = generic_inlineformset_factory(
    Relation,
    form=BaseReleaseReleationForm,
    formset=BaseReleaseReleationFormSet,
    extra=15,
    exclude=[
        'action',
    ],
    can_delete=True
)
