# -*- coding: utf-8 -*-
from django import template

from pushy_asset.settings import DEBUG

register = template.Library()


@register.inclusion_tag('pushy_asset/templatetags/pushy_asset_scripts.html', takes_context=True)
def pushy_asset_scripts(context):
    context.update({'DEBUG': DEBUG})
    return context