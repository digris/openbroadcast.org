from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import Modifier, Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu


class ActionMenu(CMSAttachMenu):
    
    name = _("Action Menu")
    
    def get_nodes(self, request):
        nodes = []
        
        """"""
        node = NavigationNode(
            _('All Activities'),
            reverse('actstream-action-list'),
            201
        )
        nodes.append(node)

        if request.user.is_active:
        
            node = NavigationNode(
                _('My Activities'),
                '%s?username=%s' % (reverse('actstream-action-list'), request.user.username),
                211
            )
            nodes.append(node)

        
        return nodes
    
menu_pool.register_menu(ActionMenu)


