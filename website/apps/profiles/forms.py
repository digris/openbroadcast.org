from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions

from pagedown.widgets import PagedownWidget


from tagging.forms import TagField
from ac_tagging.widgets import TagAutocompleteTagIt

from lib.fields.extra import ExtraClearableFileInput, PreviewImageInput, AdvancedFileInput

from profiles.models import *

# from invite.fields import InviteField


ACTION_LAYOUT =  action_layout = FormActions(
                HTML('<button type="submit" name="save-i-classicon-arrow-upi" value="save" class="btn btn-primary pull-right ajax_submit" id="submit-id-save-i-classicon-arrow-upi"><i class="icon-ok icon-white"></i> Save</button>'),            
                HTML('<button type="reset" name="reset" value="reset" class="reset resetButton btn btn-secondary pull-right" id="reset-id-reset"><i class="icon-trash"></i> Cancel</button>'),
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
        exclude = ('user', 'mentor',)

        widgets = {
            'image': AdvancedFileInput(image_width=76),
            'expertise': forms.CheckboxSelectMultiple(),
        }
        
        
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        profile_layout = Layout(
            Fieldset(
                _('Personal Information'),
                 Div(
                        HTML('<h2>%s</h2><p>%s</p>' % (_('Privacy!'), _('Your birth date is only visible to your mentor, and to team-members with administrative rights.'))),
                        css_class='notes-form notes-inline notes-info',
                ),
                Field('gender', css_class='input-xlarge'),
                Field('birth_date', css_class='input-xlarge'),
                Field('pseudonym', css_class='input-xlarge'),
                Field('description', css_class='input-xlarge'),
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
                        HTML('<h2>%s</h2><p>%s</p>' % (_('Privacy!'), _('Except for "City" and "Country", this information is only visible to your mentor, and to team-members with administrative rights.'))),
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
                        HTML('<h2>%s</h2><p>%s</p>' % (_('Account data'), _('In case you see a reason to recieve some money from us :) This information is not visible on the plattform.'))),
                        css_class='notes-form notes-inline notes-info',
                ),
                Field('iban', css_class='input-xlarge'),
                Field('paypal', css_class='input-xlarge'),
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
                        profile_layout,
                        contact_layout,
                        tagging_layout,
                        skills_layout,
                        account_layout,
                        )

        self.helper.add_layout(layout)
        
        
    from floppyforms.widgets import DateInput
    #birth_date = forms.DateField(widget=DateInput(), required=False, help_text=_('Format: YYYY/MM/DD'))
    #description = forms.CharField(widget=PagedownWidget(), required=False, help_text=_('Markdown enabled'))
    biography = forms.CharField(widget=PagedownWidget(), required=False, help_text=_('Markdown enabled'))
    d_tags = TagField(widget=TagAutocompleteTagIt(max_tags=9), required=False, label=_('Tags'))
    
    #invitation = InviteField()
    
        
    def clean_user(self):
        return self.instance.user



class LinkForm(ModelForm):

    class Meta:
        model = Link
        parent_model = Profile
        
        
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
                       Field('url', css_class='input-large'),
                       css_class='span4'
                       ),
                Column(
                       Field('title', css_class='input-medium'),
                       css_class='span2'
                       ),
                Column(
                       Field('DELETE', css_class='input-mini'),
                       css_class='span1'
                       ),
                css_class='row link-row',
        )

        self.helper.add_layout(base_layout)

class ServiceForm(ModelForm):

    class Meta:
        model = Service
        parent_model = Profile
        
        
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
                       Field('username', css_class='input-large'),
                       css_class='span4'
                       ),
                Column(
                       Field('service', css_class='input-medium'),
                       css_class='span2'
                       ),
                Column(
                       Field('DELETE', css_class='input-mini'),
                       css_class='span1'
                       ),
                css_class='row service-row',
        )

        self.helper.add_layout(base_layout)
        
        


LinkFormSet = inlineformset_factory(Profile, Link, form=LinkForm)
ServiceFormSet  = inlineformset_factory(Profile, Service, form=ServiceForm)

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('User Details'),
                Field('username', css_class='input-xlarge'),
                Field('email', css_class='input-xlarge'),
                Field('first_name', css_class='input-xlarge'),
                Field('last_name', css_class='input-xlarge'),
            )
        )
        super(UserForm, self).__init__(*args, **kwargs)