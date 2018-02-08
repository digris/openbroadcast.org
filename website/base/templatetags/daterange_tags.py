import datetime

from django import template

register = template.Library()

@register.filter 
def xxxx_to_now(value):
    value = int(value)

    return range(value, datetime.datetime.now().year + 2)
