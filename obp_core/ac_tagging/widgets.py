from django.forms.widgets import TextInput
from django.conf import settings
from django.utils.safestring import mark_safe


class TagAutocompleteTagIt(TextInput):
    def __init__(self, max_tags, *args, **kwargs):
        self.max_tags = (
            max_tags
            if max_tags
            else getattr(settings, "TAGGING_AUTOCOMPLETE_MAX_TAGS", 20)
        )
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):

        html = super().render(name, value, attrs)

        return mark_safe(html)

    class Media:
        # JS Base url defaults to STATIC_URL/jquery-autocomplete/
        js_base_url = getattr(
            settings,
            "TAGGING_AUTOCOMPLETE_JS_BASE_URL",
            f"{settings.STATIC_URL}js/jquery-tag-it/",
        )
        # jQuery ui is loaded from google's CDN by default
        jqueryui_default = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js"
        )
        jqueryui_file = getattr(
            settings, "TAGGING_AUTOCOMPLETE_JQUERY_UI_FILE", jqueryui_default
        )
        # if a custom jquery ui file has been specified
        if jqueryui_file != jqueryui_default:
            # determine path
            jqueryui_file = f"{js_base_url}{jqueryui_file}"

        # load js
        js = (
            f"{js_base_url}ac_tagging.js",
            jqueryui_file,
            f"{js_base_url}jquery.tag-it.js",
        )

        # custom css can also be overriden in settings
        css_list = getattr(
            settings,
            "TAGGING_AUTOCOMPLETE_CSS",
            [f"{js_base_url}css/ui-autocomplete-tag-it.css"],
        )
        # check is a list, if is a string convert it to a list
        if type(css_list) is str:
            css_list = [css_list]
        css = {"screen": css_list}

    def _format_value(self, value):
        return value.replace(",", ", ")

    def value_from_datadict(self, data, files, name):
        current_value = data.get(name, None)
        if current_value and current_value[-1] != ",":
            current_value = f"{current_value},"
            # current_value = u'"%s"' % current_value
            # current_value = u'%s' % current_value
        return current_value
