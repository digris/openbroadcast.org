from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from profiles.menu import ProfileMenu


class ProfileApp(CMSApp):
    
    name = _("Profile App")
    urls = ["profiles.urls_profile"]
    menus = [ProfileMenu]

apphook_pool.register(ProfileApp)

