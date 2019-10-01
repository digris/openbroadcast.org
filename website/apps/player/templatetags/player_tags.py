# -*- coding: utf-8 -*-
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("player/templatetags/_inline.html", takes_context=True)
def player_inline(context):
    return context
