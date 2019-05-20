from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from .cms_menus import ActionMenu


@apphook_pool.register
class ActionApp(CMSApp):

    name = _("Action App")
    menus = [ActionMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ['actstream.urls_actstream',]
