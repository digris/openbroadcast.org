# -*- coding: utf-8 -*-
from django import template

register = template.Library()

from nunjucks import settings as nunjucks_settings


@register.inclusion_tag(
    "nunjucks/templatetags/nunjucks_scripts.html", takes_context=True
)
def nunjucks_scripts(context):
    context.update({"DEBUG": nunjucks_settings.DEBUG})
    return context
