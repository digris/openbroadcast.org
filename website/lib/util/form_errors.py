from django.utils.translation import ugettext_lazy as _
from django.forms import BaseForm
from django.forms.formsets import BaseFormSet
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorDict

NON_FIELD_MESSAGE = _('General form errors')

def merge_form_errors(forms_to_merge=[]):
    form_errors = ErrorDict()
    for form in forms_to_merge:
        # check if form
        if isinstance(form, BaseForm):
            for field, errors in form.errors.items():
                if field == NON_FIELD_ERRORS:
                    key = NON_FIELD_MESSAGE
                else:
                    key = form.fields[field].label
                form_errors[key] = errors

        # check if formset
        if isinstance(form, BaseFormSet):
            for inner_form in form.forms:
                for field, errors in inner_form.errors.items():
                    if field == NON_FIELD_ERRORS:
                        key = NON_FIELD_MESSAGE
                    else:
                        key = inner_form.fields[field].label
                        if not key:
                            key = 'Other'

                    form_errors[key] = errors


    print form_errors


    return form_errors
