# -*- coding: utf-8 -*-
from django import template

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

register = template.Library()


@register.assignment_tag
def hash_user_groups(user):

    if not user.is_authenticated():
        return 'anonymous'

    groups = ['%s' % x.pk for x in user.groups.order_by('pk').all()]
    groups_hash = '_'.join(groups)


    return groups_hash
