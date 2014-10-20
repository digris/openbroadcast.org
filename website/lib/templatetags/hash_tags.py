from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.assignment_tag
def hash_user_groups(user):

    if not user.is_authenticated():
        return 'anonymous'

    groups = ['%s' % x.pk for x in user.groups.order_by('pk').all()]

    groups_hash = '_'.join(groups)

    return groups_hash
