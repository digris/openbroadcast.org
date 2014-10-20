# -*- coding: utf-8 -*-
from django import template

import settings


DEBUG = settings.DEBUG

register = template.Library()

@register.inclusion_tag('istats/templatetags/istats_scripts.html', takes_context=True)
def istats_scripts(context):

    context.update({'DEBUG': DEBUG})
    return context