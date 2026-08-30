from crispy_forms.layout import Div, Field

TEMPLATE_PACK = "forms_vue"


class Grid(Div):
    css_class = "form-grid-container"


class Cell(Div):
    css_class = "form-grid-cell"


class InputContainer(Field):
    template = f"{TEMPLATE_PACK}/input_container.html"
    css_class = "input-container"


class TagInputContainer(Field):
    template = f"{TEMPLATE_PACK}/tag_input_container.html"
    css_class = "input-container input-container--tag"
