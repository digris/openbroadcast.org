from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import mptt


# enhance Group class

models.ForeignKey(
    Group,
    null            = True,
    blank           = True,
    related_name    = 'children',
    verbose_name    = _('parent'),
    help_text       = _('The group\'s parent group. None, if it is a root node.')
).contribute_to_class(Group, 'parent')

mptt.register(Group)


# enhance User class

def get_all_groups(self):
    """
    Returns all groups the user is member of AND all parent groups of those
    groups.
    """
    direct_groups = self.groups.all()
    groups = set()

    for group in direct_groups:
        ancestors = group.get_ancestors().all()
        for anc in ancestors:
            groups.add(anc)
        groups.add(group)

    return groups

setattr(User, 'get_all_groups', get_all_groups)


# register special auth backend to handle inheritance of permissions
settings.AUTHENTICATION_BACKENDS += ('django_hgroups.util.AuthBackend',)

