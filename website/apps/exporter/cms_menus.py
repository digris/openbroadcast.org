from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import Modifier, Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu


class ExportMenu(CMSAttachMenu):
    
    name = _("Export Menu")
    
    def get_nodes(self, request):
        nodes = []
        
        """"""
        node = NavigationNode(
            _('My Downloads'),
            reverse('exporter-export-list'),
            191,
        )
        nodes.append(node)
        
        """
        node = NavigationNode(
            _('Settings'),
            reverse('exporter-export-settings'),
            192,

        )
        nodes.append(node)
        """
        
        
        return nodes
    
menu_pool.register_menu(ExportMenu)
