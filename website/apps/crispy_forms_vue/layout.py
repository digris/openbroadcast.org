# -*- coding: utf-8 -*-

from crispy_forms.layout import LayoutObject, Div, Field

TEMPLATE_PACK = "forms_vue"


class Grid(Div):
    css_class = "form-grid-container"


class Cell(Div):
    css_class = "form-grid-cell"


class InputContainer(Field):

    template = "{}/input_container.html".format(TEMPLATE_PACK)
    css_class = "input-container"


class TagInputContainer(Field):

    template = "{}/tag_input_container.html".format(TEMPLATE_PACK)
    css_class = "input-container input-container--tag"
