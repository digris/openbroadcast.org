from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from abcast.menu import SchedulerMenu


class JingleApp(CMSApp):
    
    name = _("Jingle App")
    urls = ["abcast.urls_jingle"]
    # menus = [JingleMenu]

apphook_pool.register(JingleApp)

class SchedulerApp(CMSApp):
    
    name = _("Scheduler App")
    urls = ["abcast.urls_scheduler"]
    menus = [SchedulerMenu]

apphook_pool.register(SchedulerApp)

class StationApp(CMSApp):

    name = _("Station App")
    urls = ["abcast.urls_station"]
    #menus = [StationMenu]

apphook_pool.register(StationApp)
