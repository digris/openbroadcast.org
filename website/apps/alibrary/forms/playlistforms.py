# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from ac_tagging.widgets import TagAutocompleteTagIt
from alibrary import settings as alibrary_settings
from alibrary.models import Playlist
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Field, Fieldset, Div
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from base.fields.extra import AdvancedFileInput
from pagedown.widgets import PagedownWidget
from tagging.forms import TagField

from search.forms import fields as search_fields

from ..models import Daypart, Season, Weather

ACTION_LAYOUT =  action_layout = FormActions(
                HTML('<button type="submit" name="save-i-classicon-arrow-upi" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-ok icon-white"></i> Save</button>'),
                HTML('<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-abort pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
        )



current_year = date.today().year
ROTATION_YEAR_CHOICES = [y for y in range(current_year + 10, current_year - 11, -1)]



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
        fields = [
            'name',
            'd_tags',
            'description',
            'main_image',
            #'playout_mode_random',
            'rotation',
            'rotation_date_start',
            'rotation_date_end',
            'dayparts',
            'weather',
            'seasons',
            'target_duration',
            'series',
            'series_number'
        ]



        widgets = {
            'rotation_date_start': SelectDateWidget(
                years=ROTATION_YEAR_CHOICES,
                empty_label=(_('Year'), _('Month'), _('Day')),
            ),
            'rotation_date_end': SelectDateWidget(
                years=ROTATION_YEAR_CHOICES,
                empty_label=(_('Year'), _('Month'), _('Day')),
            ),
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
                Field('description', css_class='input-xlarge'),
                'main_image',
                css_class='base'
        )


        series_layout = Fieldset(
                "%s %s" % ('<i class="icon-tags"></i>', _('Series')),
                Div(
                    Field('series', css_class='input-xlarge'),
                    css_class='series'
                ),
                Div(
                    Field('series_number', css_class='input-xlarge'),
                    css_class='series-number'
                ),
                css_class='series'
        )

        tagging_layout = Fieldset(
                "%s %s" % ('<i class="icon-tags"></i>', _('Tags')),
                'd_tags',
                css_class='tagging'
        )

        playout_mode_layout = Fieldset(
                "%s %s" % ('<i class="icon-random"></i>', _('Playout Mode')),
                'playout_mode_random',
                css_class='playout-mode'
        )

        rotation_layout = Fieldset(
                "%s %s" % ('<i class="icon-random"></i>', _('Random Rotation')),
                'rotation',
                'rotation_date_start',
                'rotation_date_end',
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
            base_layout,
            tagging_layout,
            series_layout,
            #playout_mode_layout,
            rotation_layout,
            daypart_layout,
        )

        self.helper.add_layout(layout)




    #main_image = forms.Field(widget=FileInput(), required=False)
    main_image = forms.Field(widget=AdvancedFileInput(), required=False)
    d_tags = TagField(widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_('Tags'))
    description = forms.CharField(widget=PagedownWidget(), required=False)

    rotation = forms.BooleanField(required=False, label=_('Include in rotation'), help_text=_('Allow this broadcast to be aired at random time if nothing else is scheduled.'))

    series = search_fields.AutocompleteField('alibrary.series', allow_new=True, required=False)

    target_duration = forms.ChoiceField(widget=forms.RadioSelect, choices=alibrary_settings.PLAYLIST_TARGET_DURATION_CHOICES, required=False)
    dayparts = forms.ModelMultipleChoiceField(label='...%s' % _('Dayparts'), widget=DaypartWidget(), queryset=Daypart.objects.active(), required=False)

    seasons = forms.ModelMultipleChoiceField(label='...%s' % _('Seasons'), queryset=Season.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    weather = forms.ModelMultipleChoiceField(label='...%s' % _('Weather'), queryset=Weather.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    def clean(self, *args, **kwargs):
        cd = super(PlaylistForm, self).clean()
        series = cd['series']
        try:
            if not series.pk:
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
