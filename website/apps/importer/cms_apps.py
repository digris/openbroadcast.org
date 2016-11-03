from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from importer.menu import ImportMenu


class ImportApp(CMSApp):
    
    name = _("Import App")
    urls = ["importer.urls_import"]
    menus = [ImportMenu]

apphook_pool.register(ImportApp)

