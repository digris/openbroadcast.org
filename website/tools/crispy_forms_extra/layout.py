import itertools

from django.conf import settings
from django.utils.html import conditional_escape
from crispy_forms.layout import LayoutObject, Div

from crispy_forms.utils import render_field

TEMPLATE_PACK = getattr(settings, "CRISPY_TEMPLATE_PACK", "bootstrap")


class Row(Div):
    """
    Layout object. It wraps fields in a div whose default class is "formRow". Example::
        Row('form_field_1', 'form_field_2', 'form_field_3')
    """

    css_class = "form-row"


class Column(Div):
    """
    Layout object. It wraps fields in a div whose default class is "formColumn". Example::
        Column('form_field_1', 'form_field_2')
    """

    css_class = "form-column"


class LookupField(LayoutObject):
    """
    Layout object, It contains one field name, and you can add attributes to it easily.
    For setting class attributes, you need to use `css_class`, as `class` is a Python keyword.

    Example::

        Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
    """

    template = "%s/lookup_field.html" % TEMPLATE_PACK

    def __init__(self, *args, **kwargs):
        self.fields = list(args)

        if not hasattr(self, "attrs"):
            self.attrs = {}

        if kwargs.has_key("css_class"):
            if "class" in self.attrs:
                self.attrs["class"] += " %s" % kwargs.pop("css_class")
            else:
                self.attrs["class"] = kwargs.pop("css_class")

        self.template = kwargs.pop("template", self.template)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(
            dict(
                [
                    (k.replace("_", "-"), conditional_escape(v))
                    for k, v in kwargs.items()
                ]
            )
        )

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = ""
        for field in self.fields:
            html += render_field(
                field,
                form,
                form_style,
                context,
                template=self.template,
                attrs=self.attrs,
            )
        return html


class LookupImageField(LayoutObject):
    """
    Layout object, It contains one field name, and you can add attributes to it easily.
    For setting class attributes, you need to use `css_class`, as `class` is a Python keyword.

    Example::

        Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
    """

    template = "%s/lookup_image_field.html" % TEMPLATE_PACK

    def __init__(self, *args, **kwargs):
        self.fields = list(args)

        if not hasattr(self, "attrs"):
            self.attrs = {}

        if kwargs.has_key("css_class"):
            if "class" in self.attrs:
                self.attrs["class"] += " %s" % kwargs.pop("css_class")
            else:
                self.attrs["class"] = kwargs.pop("css_class")

        self.template = kwargs.pop("template", self.template)

        # We use kwargs as HTML attributes, turning data_id='test' into data-id='test'
        self.attrs.update(
            dict(
                [
                    (k.replace("_", "-"), conditional_escape(v))
                    for k, v in kwargs.items()
                ]
            )
        )

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = ""
        for field in self.fields:
            html += render_field(
                field,
                form,
                form_style,
                context,
                template=self.template,
                attrs=self.attrs,
            )
        return html
