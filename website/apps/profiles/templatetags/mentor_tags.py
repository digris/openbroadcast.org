# -*- coding: utf-8 -*-
from django import template

from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.inclusion_tag('profiles/templatetags/mentor_for_user.html', takes_context=True)
def mentor_for_user(context, profile, mentor):
    
    actions = []
    notes = None
    
    if profile.mentor == mentor and not profile.is_approved:
        
        notes = _("You're mentoring this user. Approving his/her profile will give full platform-access to the respective user. Think twice before handling!\nPlease remember, only professionals (radio or music business) should be given access to the platform!")


        actions.append({
                        'description': _('asd'),
                        'name': _('Approve as MUSIC PROFESSIONAL'),
                        'icon': 'star',
                        'url': reverse('profiles-profile-mentor-approve',
                                       kwargs={
                                           'pk': profile.pk,
                                           'level': 'music_pro',
                                       }),
                        })
        actions.append({
                        'description': _('asd'),
                        'name': _('Approve as RADIO PROFESSIONAL'),
                        'icon': 'star',
                        'url': reverse('profiles-profile-mentor-approve',
                                       kwargs={
                                           'pk': profile.pk,
                                           'level': 'radio_pro',
                                       }),
                        })
        actions.append({
                        'description': _('asd'),
                        'name': _('Cancel mentorship'),
                        'icon': 'remove',
                        'url': reverse('profiles-profile-mentor-cancel', kwargs={'pk': profile.pk}),
                        })
    
    if not profile.mentor and mentor.has_perm('profiles.mentor_profiles'):
        
        # notes = _("Do youwant to become the mentor of this user?")
        
        actions.append({
                        'description': _('asd'),
                        'name': _('Become the mentor'),
                        'icon': 'female' if mentor.profile.gender == 1 else 'male',
                        'url': reverse('profiles-profile-mentor-become', kwargs={'pk': profile.pk}),
                        })
    
    
    context.update({
                    'user': profile.user,
                    'profile': profile,
                    'mentor': mentor,
                    'actions': actions,
                    'notes': notes,
                    })
    return context



