# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json

from django import forms
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from selectable import __version__
from selectable.compat import force_text
from selectable.forms.base import import_lookup_class

__all__ = (
    'AutocompleteWidget',
)


class AutocompleteInputWidget(forms.TextInput):
    """
    renders the autocomplete *inner* `<input>` field
    """

    def __init__(self, lookup_model, *args, **kwargs):
        self.lookup_model = lookup_model
        self.allow_new = kwargs.pop('allow_new', False)
        super(AutocompleteInputWidget, self).__init__(*args, **kwargs)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutocompleteInputWidget, self).build_attrs(extra_attrs, **kwargs)
        attrs['autocomplete'] = 'off'
        attrs['data-autocomplete-widget-url'] = self.lookup_model.url
        attrs['data-autocomplete-widget-type'] = 'text'
        attrs['data-autocomplete-widget-allow-new'] = str(self.allow_new).lower()
        return attrs


class AutocompleteWidget(forms.MultiWidget):
    """
    combo widget to render representation text and hidden id field
    """

    def __init__(self, lookup_model, *args, **kwargs):
        self.lookup_model = lookup_model
        self.allow_new = kwargs.pop('allow_new', False)
        widgets = [
            AutocompleteInputWidget(
                lookup_model=lookup_model,
                allow_new=self.allow_new,
                attrs=kwargs.get('attrs'),
            ),
            forms.HiddenInput(attrs={'data-autocomplete-widget-type': 'hidden'})
            #forms.TextInput(attrs={'data-autocomplete-widget-type': 'hidden'})
        ]
        super(AutocompleteWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            repr = self.lookup_model.model_class.objects.get(pk=value)
            return [repr, value]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        value = super(AutocompleteWidget, self).value_from_datadict(data, files, name)
        if not self.allow_new:
            return value[1]
        return value
