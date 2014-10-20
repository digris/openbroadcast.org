from django import forms
from django.forms import ModelForm, Form
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions
from pagedown.widgets import PagedownWidget
from django.forms.widgets import FileInput
from tagging.forms import TagField

from filer.models.imagemodels import Image
from alibrary.models import Playlist
import selectable.forms as selectable
from alibrary.lookups import *
from ac_tagging.widgets import TagAutocompleteTagIt
from lib.widgets.widgets import ReadOnlyIconField
from lib.fields.extra import AdvancedFileInput


from alibrary import settings as alibrary_settings



ACTION_LAYOUT =  action_layout = FormActions(
                HTML('<button type="submit" name="save-i-classicon-arrow-upi" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-ok icon-white"></i> Save</button>'),            
                HTML('<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-secondary pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
        )


class ActionForm(Form):
    
    def __init__(self, *args, **kwargs):
        super(ActionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.add_layout(ACTION_LAYOUT)
 
 
from django.forms import SelectMultiple, CheckboxInput
from django.utils.encoding import force_unicode
from itertools import chain
class DaypartWidget(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        cs = []
        for c in self.choices:
            c = list(c)
            c.append(True)
            cs.append(c)

        dps = Daypart.objects.active()
        cs = []
        t_dp_day = None
        for dp in dps:
            row_title = False
            if not t_dp_day == dp.get_day_display():
                row_title = dp.get_day_display()
                t_dp_day = dp.get_day_display()
                 
            c = [dp.pk, '%02d - %02d' % (dp.time_start.hour, dp.time_end.hour), row_title]
            cs.append(c)

        self.choices = cs
        
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul class="unstyled" style="float: left;">']
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label, row_title) in enumerate(chain(self.choices, choices)):
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
        
            if row_title:
                output.append(u'</ul><ul class="unstyled" style="float: left;"><li class="title">%s</li>' % row_title)
            
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        if id_:
            id_ += '_0'
        return id_


class PlaylistForm(ModelForm):

    class Meta:
        model = Playlist
        #fields = ('name','label','releasetype','release_country','catalognumber','description', 'main_image', 'releasedate', 'd_tags')
        fields = ('name', 'd_tags', 'description', 'main_image', 'rotation', 'dayparts', 'weather', 'seasons', 'target_duration', 'series', 'series_number')
        
        
        widgets = {
            #{ 'target_duration': forms.RadioSelect() }
        }
        

    def __init__(self, *args, **kwargs):
        
        try:
            self.user = kwargs['initial']['user']
            self.instance = kwargs['instance']
        except:
            pass
        
        super(PlaylistForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.fields['name'].label = _('Title')

        if self.instance.type == 'broadcast':
            self.fields['d_tags'].required = True
            self.fields['dayparts'].required = True
            self.fields['target_duration'].required = True
            self.fields['target_duration'].widget.attrs['disabled'] = 'disabled'

        if self.instance.type == 'playlist':
            self.fields['d_tags'].required = True


        
        base_layout = Fieldset(
        
                _('General'),
                #Div(HTML('<h4>%s</h4><p>%s</p>' % (_('Bulk Edit'), _('Choose Artist name and/or license to apply on every track.'))), css_class='form-help'),
                Field('name', css_class='input-xlarge'),
                Div(
                    Field('target_duration'),
                    css_class='target-duration'
                ),
                Field('description', css_class='input-xxlarge'),
                'main_image',
                css_class='base'
        )

        
        series_layout = Fieldset(
                "%s %s" % ('<i class="icon-tags"></i>', _('Series')),
                Div(
                    Field('series'),
                    css_class='series'
                ),
                Div(
                    Field('series_number'),
                    css_class='series-number'
                ),
                css_class='series'
        )

        tagging_layout = Fieldset(
                "%s %s" % ('<i class="icon-tags"></i>', _('Tags')),
                'd_tags',
                css_class='tagging'
        )

        rotation_layout = Fieldset(
                "%s %s" % ('<i class="icon-random"></i>', _('Random Rotation')),
                'rotation',
                css_class='rotation'
        )
        
        daypart_layout = Fieldset(
                "%s %s" % ('<i class="icon-calendar"></i>', _('Best Broadcast...')),
                Div(
                    Field('dayparts'),
                    css_class='dayparts'
                ),
                Div(
                    Field('seasons'),
                    css_class='seasons'
                ),
                Div(
                    Field('weather'),
                    css_class='weather'
                ),
                css_class='daypart'
                
        )
            
        layout = Layout(
                        #ACTION_LAYOUT,
                        base_layout,
                        tagging_layout,
                        series_layout,
                        rotation_layout,
                        daypart_layout,
                        #ACTION_LAYOUT,
                        )

        self.helper.add_layout(layout)

        

    
    #main_image = forms.Field(widget=FileInput(), required=False)
    main_image = forms.Field(widget=AdvancedFileInput(), required=False)
    d_tags = TagField(widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_('Tags'))
    description = forms.CharField(widget=PagedownWidget(), required=False, help_text="Markdown enabled text")

    rotation = forms.BooleanField(required=False, label=_('Include in rotation'), help_text=_('Allow this broadcast to be aired at random time if nothing else is scheduled.'))

    series = selectable.AutoCompleteSelectField(PlaylistSeriesLookup, allow_new=True, required=False)

    target_duration = forms.ChoiceField(widget=forms.RadioSelect, choices=alibrary_settings.PLAYLIST_TARGET_DURATION_CHOICES, required=False)
    dayparts = forms.ModelMultipleChoiceField(label='...%s' % _('Dayparts'), widget=DaypartWidget(), queryset=Daypart.objects.active(), required=False)

    seasons = forms.ModelMultipleChoiceField(label='...%s' % _('Seasons'), queryset=Season.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    weather = forms.ModelMultipleChoiceField(label='...%s' % _('Weather'), queryset=Weather.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    def clean(self, *args, **kwargs):
        cd = super(PlaylistForm, self).clean()

        series = cd['series']
        try:
            if not series.pk:
                print "SEEMS TO BE NEW SERIES..."
                series.save()
        except:
            pass

        return cd

    def clean_target_duration(self):
        target_duration = self.cleaned_data['target_duration']

        try:
            return int(target_duration)
        except:
            return None

    def save(self, *args, **kwargs):
        return super(PlaylistForm, self).save(*args, **kwargs)
   
    
    
 

""" 
class BaseReleaseMediaFormSet(BaseInlineFormSet): 
        

    def __init__(self, *args, **kwargs):

        self.instance = kwargs['instance']

        super(BaseReleaseMediaFormSet, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_id = "id_releasemediainline_form_%s" % 'asd'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        
        
        base_layout = Row(
                Column(
                       Field('tracknumber', css_class='input-small'),
                       Field('mediatype', css_class='input-small'),
                       Field('license', css_class='input-small'),
                       css_class='span2'
                       ),
                Column(
                                Field('name', css_class='input-xlarge'),
                                Field('artist', css_class='input-xlarge'),
                                Field('isrc', css_class='input-xlarge'),
                       css_class='span5'
                       ),
                css_class='releasemedia-row row',
        )
 
        self.helper.add_layout(base_layout)
        

        
 
    def add_fields(self, form, index):
        # allow the super class to create the fields as usual
        super(BaseReleaseMediaFormSet, self).add_fields(form, index)
 
        # created the nested formset
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance=None
            pk_value = hash(form.prefix)
 
 

class BaseReleaseMediaForm(ModelForm):

    class Meta:
        model = Media
        parent_model = Release
        formset = BaseReleaseMediaFormSet
        fields = ('name','tracknumber',)
        
    def __init__(self, *args, **kwargs):
        self.instance = kwargs['instance']
        super(BaseReleaseMediaForm, self).__init__(*args, **kwargs)
        

    artist = selectable.AutoCompleteSelectField(ArtistLookup, allow_new=True, required=False)
    tracknumber =  forms.CharField(label=_('No.'))   




  
class BaseReleaseReleationFormSet(BaseGenericInlineFormSet):

        
        
    def __init__(self, *args, **kwargs):

        self.instance = kwargs['instance']
        super(BaseReleaseReleationFormSet, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "id_releasemediainline_form_%s" % 'asdfds'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = False
        
        base_layout = Row(
                Column(
                       Field('url', css_class='input-xlarge'),
                       css_class='span5'
                       ),
                Column(
                       Field('service', css_class='input-small'),
                       css_class='span1'
                       ),
                Column(
                       Field('DELETE', css_class='input-mini'),
                       css_class='span1'
                       ),
                css_class='row relation-row',
        )
 
        self.helper.add_layout(base_layout)
        


class BaseReleaseReleationForm(ModelForm):

    class Meta:
        model = Relation
        parent_model = Release
        formset = BaseReleaseReleationFormSet
        fields = ('url','service',)
        
    def __init__(self, *args, **kwargs):
        super(BaseReleaseReleationForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['service'].widget.attrs['readonly'] = True
        
    def clean_service(self):
        return self.instance.service

    service = forms.CharField(label='', widget=ReadOnlyIconField(), required=False)
    url = forms.URLField(label=_('Website / URL'), required=False)

    #name = selectable.AutoCompleteSelectField(ArtistLookup, allow_new=True, required=False)
    #tracknumber =  forms.CharField(label=_('No.'))  
"""

# Compose Formsets
"""
ReleaseMediaFormSet = inlineformset_factory(Release, Media, form=BaseReleaseMediaForm, formset=BaseReleaseMediaFormSet, can_delete=False, extra=0, fields=('name', 'tracknumber', 'isrc', 'artist', 'license', 'mediatype',), can_order=False)
ReleaseRelationFormSet = generic_inlineformset_factory(Relation, form=BaseReleaseReleationForm, formset=BaseReleaseReleationFormSet, extra=3, exclude=('action',), can_delete=True)
"""





    