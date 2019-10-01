from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from .cms_menus import ExportMenu


@apphook_pool.register
class ExportApp(CMSApp):

    name = _("Export App")
    menus = [ExportMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["exporter.urls_export"]
