# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django import template
from django.template.defaultfilters import escapejs, urlencode

from ..utils import get_object_actions_for_user

register = template.Library()


@register.simple_tag()
def get_object_actions_as_json(obj, user):
    """
    used to pass as `props` to vue.js components.
    generate json formatted actions for given object.
    """
    return json.dumps(get_object_actions_for_user(obj, user), indent=4)
