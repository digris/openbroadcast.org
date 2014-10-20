from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.test_utils.project.sampleapp.menu import SampleAppMenu
from cms.apphook_pool import apphook_pool


class SampleApp(CMSApp):
    name = _("Sample App")
    urls = ["cms.test_utils.project.sampleapp.urls"]
    menus = [SampleAppMenu]
    
apphook_pool.register(SampleApp)
