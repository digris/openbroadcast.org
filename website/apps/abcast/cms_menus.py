from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu


class SchedulerMenu(CMSAttachMenu):

    name = _("Scheduler Menu")

    def get_nodes(self, request):
        nodes = []
        return nodes


menu_pool.register_menu(SchedulerMenu)
