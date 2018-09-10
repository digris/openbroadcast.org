import time

from django import template

register = template.Library()

@register.filter
def text_replace(value, arg):
    """
        {% text_replace:"foo:bar" %}
    """
    try:
        return value.replace(*arg.split(':'))
    except (AttributeError, ValueError):
        return value
