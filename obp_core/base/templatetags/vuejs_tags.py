import json
from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def as_json(value, safe=False):
    if safe:
        return mark_safe(json.dumps(value, indent=2))
    try:
        return json.dumps(value)
    except TypeError:
        return json.dumps([])
