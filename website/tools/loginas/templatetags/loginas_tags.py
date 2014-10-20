from __future__ import unicode_literals
from django.template import Library

register = Library()

@register.assignment_tag(takes_context=True)
def loginas_is_active(context):
    request = context['request']
    return request.session.get('loginas_original_user_id', None)
