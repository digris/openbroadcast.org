from django import template
from ..settings import BACKEND_DETAILS

register = template.Library()


@register.assignment_tag
def backend_detail_as(backend_key):
    return BACKEND_DETAILS.get(backend_key)
