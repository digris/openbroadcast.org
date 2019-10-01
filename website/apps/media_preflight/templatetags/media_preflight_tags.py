# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template

register = template.Library()


@register.inclusion_tag("media_preflight/templatetags/preflight_status_inline.html")
def preflight_status_inline(object):

    if hasattr(object, "preflight_check"):
        preflight_check = object.preflight_check
    else:
        preflight_check = None

    context = {"preflight_check": preflight_check}
    return context
