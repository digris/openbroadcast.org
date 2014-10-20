# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('backfeed/templatetags/inline.html', takes_context=True)
def backfeed_inline(context):
    #context.update({'foo': '...'})
    request = context['request']
    context.update({'lala': 123})

    return context

