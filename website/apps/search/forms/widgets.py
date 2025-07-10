from django import forms

__all__ = ("AutocompleteWidget",)


class AutocompleteInputWidget(forms.TextInput):
    """
    renders the autocomplete *inner* `<input>` field
    """

    def __init__(self, lookup_model, *args, **kwargs):
        self.lookup_model = lookup_model
        self.allow_new = kwargs.pop("allow_new", False)
        super().__init__(*args, **kwargs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["autocomplete"] = "off"
        attrs["data-autocomplete-widget-url"] = self.lookup_model.url
        attrs["data-autocomplete-widget-type"] = "text"
        attrs["data-autocomplete-widget-allow-new"] = str(self.allow_new).lower()
        return attrs



class AutocompleteWidget(forms.MultiWidget):
    """
    combo widget to render representation text and hidden id field
    """

    def __init__(self, lookup_model, *args, **kwargs):
        self.lookup_model = lookup_model
        self.allow_new = kwargs.pop("allow_new", False)
        widgets = [
            AutocompleteInputWidget(
                lookup_model=lookup_model,
                allow_new=self.allow_new,
                attrs=kwargs.get("attrs"),
            ),
            forms.HiddenInput(attrs={"data-autocomplete-widget-type": "hidden"}),
        ]
        super().__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            repr = self.lookup_model.model_class.objects.get(pk=value)
            return [repr, value]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if not self.allow_new:
            return value[1]
        return value
