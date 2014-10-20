from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from actstream.menu import ActionMenu


class ActionApp(CMSApp):
    
    name = _("Action App")
    urls = ["actstream.urls_actstream"]
    menus = [ActionMenu]

apphook_pool.register(ActionApp)

