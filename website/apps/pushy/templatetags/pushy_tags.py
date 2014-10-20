# -*- coding: utf-8 -*-
from django import template

from pushy.settings import SETTINGS


SOCKET_SERVER = SETTINGS.get('SOCKET_SERVER', None)
DEBUG = SETTINGS.get('PUSHY_DEBUG', False)

register = template.Library()

@register.inclusion_tag('pushy/templatetags/pushy_scripts.html', takes_context=True)
def pushy_scripts(context):
    context.update({'SOCKET_SERVER': SOCKET_SERVER})
    context.update({'DEBUG': DEBUG})
    return context