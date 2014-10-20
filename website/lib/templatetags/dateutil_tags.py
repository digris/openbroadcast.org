from django import template

register = template.Library()

@register.filter
def is_weekend(value):
    if value.date().weekday() in [5, 6]:
        return True
