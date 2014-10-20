from django.utils.translation import ugettext_lazy as _

from menus.base import Modifier, Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu


#from abcast.models import Emission


class SchedulerMenu(CMSAttachMenu):
    
    name = _("Scheduler Menu")
    
    def get_nodes(self, request):
        nodes = []

        node = NavigationNode(
            _('Week'),
            '#',
            7202
        )
        nodes.append(node)
        node = NavigationNode(
            _('Two weeks'),
            '#',
            7203
        )
        nodes.append(node)
        
        
        return nodes
    
menu_pool.register_menu(SchedulerMenu)


