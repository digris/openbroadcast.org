from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class DocumentationMenu(CMSAttachMenu):
    
    name = _("Documentation Menu")
    
    def get_nodes(self, request):
        nodes = []
        return nodes
    
menu_pool.register_menu(DocumentationMenu)


