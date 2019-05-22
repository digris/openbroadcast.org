# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django import template

from ..settings import BACKEND_DETAILS


log = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag(
    "account/templatetags/_inline.html", takes_context=True
)
def account_inline(context):
    return context


@register.inclusion_tag(
    "account/templatetags/_backend_detail.html", takes_context=True
)
def backend_detail(context, backend_key, action="login"):

    if backend_key in BACKEND_DETAILS:

        be = BACKEND_DETAILS[backend_key].copy()
        be.update({"action": action, "key": backend_key})

        context.update(be)

    else:

        context.update(
            {"action": action, "key": backend_key, "name": backend_key}
        )

    # context['action'] = action
    # context['key'] = backend_key
    # context['name'] = backend_key

    return context

    # return {
    #     'action': action,
    #     'key': backend_key,
    #     'name': backend_key,
    # }

