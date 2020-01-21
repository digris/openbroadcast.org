# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import TextInput
from django.template import loader
from django.utils.safestring import mark_safe


class TagAutocompleteWidget(TextInput):
    # TODO: template_name supported from django 1.11
    template_name = "tagging/forms/witgets/autocomplete.html"
    instance = None

    def __init__(self, attrs=None, options={}, *args, **kwargs):
        super(TagAutocompleteWidget, self).__init__(attrs)
        print(self.__dict__)

        self.options = options

    def render(self, name, value, attrs=None):
        print(self.__dict__)
        tpl = loader.get_template(self.template_name)
        context = {
            "ct": self.instance.get_ct() if self.instance else None,
            "instance": self.instance,
            "name": name,
            "value": value,
            "attrs": attrs,
            "options": self.options,
        }
        return mark_safe(tpl.render(context))
