# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

register = template.Library()


@register.assignment_tag()
def preflight_status_as(obj):

    if hasattr(obj, "preflight_check"):
        data = {
            # "checks": obj.preflight_check.checks,
            "status": obj.preflight_check.status,
            "warnings": obj.preflight_check.warnings,
            "errors": obj.preflight_check.errors,
        }
        print("PFC", data)

        return data

    return None
