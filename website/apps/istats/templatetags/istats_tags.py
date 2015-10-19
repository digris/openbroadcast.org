# -*- coding: utf-8 -*-
from django import template

from django.conf import settings


DEBUG = getattr(settings, 'DEBUG', False)

register = template.Library()

@register.inclusion_tag('istats/templatetags/istats_scripts.html', takes_context=True)
def istats_scripts(context):

    context.update({'DEBUG': DEBUG})
    return context