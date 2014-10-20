from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import FormActions

from importer.models import Import


class ImportCreateForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(ImportCreateForm, self).__init__(*args, **kwargs)        
        
        self.helper = FormHelper()
        self.helper.form_id = "bulk_edit%s" % 'asd'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = True
        """"""
        layout = Layout(

              Field('agree_terms'),
              Field('agree_documentation'),
  
            FormActions(
                Submit('submit', 'Continue', css_class='btn btn-primary')
            ),
        )
        self.helper.add_layout(layout)
    
    agree_terms = forms.BooleanField(
        label = _('I agree to the Terms & Conditions'),
        initial = False,
        required = True,
    )

    agree_documentation = forms.BooleanField(
        label = _('I read the ducumentation and know how Importing works'),
        initial = False,
        required = True,
    )


class ImportCreateModelForm(forms.ModelForm):
    
    class Meta:
        model = Import
        exclude = ('user', 'type', 'status', 'uuid_key', )

        widgets = {
            #'image': AdvancedFileInput(image_width=76),
            'notes': forms.Textarea(attrs={'rows':2, 'cols':30}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ImportCreateModelForm, self).__init__(*args, **kwargs)        
        
        self.helper = FormHelper()
        self.helper.form_id = "bulk_edit%s" % 'asd'
        self.helper.form_class = 'form-horizontal form-compact'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_tag = True
        """"""
        layout = Layout(

            Fieldset(
                _('Information'),
                  Field('notes', css_class='input-xxlarge'),
              ),

            Fieldset(
                _('Terms & Legal'),
                  Field('agree_terms'),
                  Field('agree_documentation'),
              ),
  
            FormActions(
                HTML('<button type="submit" value="Submit" class="btn btn-primary pull-right"><i class="icon-ok icon-white"></i> Agree & Continue</button>'),            
                HTML('<button type="reset" name="reset" value="reset" class="reset btn btn-secondary pull-right"><i class="icon-trash"></i> Cancel</button>'),
            ),
        )
        self.helper.add_layout(layout)
    
    agree_terms = forms.BooleanField(
        #label = _('I agree to the Terms & Conditions'),
        label = mark_safe('%s <a href="%s">%s</a>' % (_('I agree to the'), '/legal/terms-and-conditions/', _('Terms & Conditions'))),
        initial = False,
        required = True,
    )

    agree_documentation = forms.BooleanField(
        #label = _('I did read the ducumentation and know how Importing works'),
        label = mark_safe('%s <a href="%s">%s</a> %s' % (_('I did read the'), '/documentation/plattform/', _('ducumentation'), _(' and understand how Importing works'))),
        initial = False,
        required = True,
    )
