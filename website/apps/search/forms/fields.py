# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from .utils import get_model_class, get_model_data
from .widgets import AutocompleteWidget

__all__ = ("AutocompleteField",)


class AutocompleteField(forms.Field):

    widget = AutocompleteWidget

    default_error_messages = {
        "invalid_choice": _(
            "Select a valid choice. That choice is not one of the available choices."
        )
    }

    def __init__(self, lookup_ctype, *args, **kwargs):

        self.allow_new = kwargs.pop("allow_new", False)
        self.lookup_ctype = lookup_ctype

        self.lookup_model = get_model_data(lookup_ctype)

        kwargs["widget"] = self.widget(
            lookup_model=self.lookup_model, allow_new=self.allow_new
        )

        super(AutocompleteField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return None
        # lookup = self.lookup_class()
        lookup = self.lookup_model

        if len(value) != 2:
            raise ValidationError(self.error_messages["invalid_choice"])
        label, pk = value
        if pk in EMPTY_VALUES:
            if not self.allow_new:
                if label:
                    raise ValidationError(self.error_messages["invalid_choice"])
                else:
                    return None
            if label in EMPTY_VALUES:
                return None
            # value = lookup.create_item(label)

            _obj = self.lookup_model.model_class(name=label.strip())
            value = _obj

        else:
            value = self.lookup_model.model_class.objects.get(pk=pk)
            if value is None:
                raise ValidationError(self.error_messages["invalid_choice"])

        return value
