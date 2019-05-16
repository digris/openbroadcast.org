from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from .cms_menus import ExportMenu


class ExportApp(CMSApp):

    name = _("Export App")
    urls = ["exporter.urls_export"]
    menus = [ExportMenu]

apphook_pool.register(ExportApp)

