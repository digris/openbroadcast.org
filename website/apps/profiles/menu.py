from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import Modifier, Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu


class ProfileMenu(CMSAttachMenu):
    
    name = _("Profile Menu")
    
    def get_nodes(self, request):
        nodes = []
        
        """"""
        node = NavigationNode(
            _('All Users'),
            reverse('profiles-profile-list'),
            110
        )
        nodes.append(node)
        
        if request.user.is_active:
            node = NavigationNode(
                _('My Profile'),
                reverse('profiles-profile-detail', args=[request.user.username]),
                111
            )
            nodes.append(node)
            
            
            node = NavigationNode(
                _('Edit my Profile'),
                reverse('profiles-profile-edit'),
                121
            )
            nodes.append(node)

        if request.user.has_perm('invitation.change_invitation'):

            node = NavigationNode(
                _('My Invitations'),
                reverse('profiles-invitations'),
                123
            )
            nodes.append(node)
        
        return nodes
    
menu_pool.register_menu(ProfileMenu)


