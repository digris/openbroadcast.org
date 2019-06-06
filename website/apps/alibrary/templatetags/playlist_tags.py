# -*- coding: utf-8 -*-
from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.assignment_tag
def nearby_scheduled_as(obj, num_hours=48):

    now = timezone.now()
    if obj.last_emission and obj.last_emission.time_start > now - timedelta(hours=num_hours):
        return True

    if obj.next_emission and obj.next_emission.time_start < now + timedelta(hours=num_hours):
        return True

    return False
