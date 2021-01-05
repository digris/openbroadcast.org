import json
from django import template

register = template.Library()


@register.filter
def tag_names_as_json(tags):
    return json.dumps([t.name for t in tags])
