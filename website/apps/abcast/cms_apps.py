from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from .cms_menus import SchedulerMenu


@apphook_pool.register
class SchedulerApp(CMSApp):

    name = _("Scheduler App")
    menus = [SchedulerMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ['abcast.urls_scheduler',]


@apphook_pool.register
class StationApp(CMSApp):

    name = _("Station App")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['abcast.urls_station',]
