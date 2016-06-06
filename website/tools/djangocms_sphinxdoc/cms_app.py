from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from djangocms_sphinxdoc.menu import DocumentationMenu

class DocumentationApp(CMSApp):
    name = _("Documentation App")
    urls = ["djangocms_sphinxdoc.urls"]
    menus = [DocumentationMenu]

apphook_pool.register(DocumentationApp)
