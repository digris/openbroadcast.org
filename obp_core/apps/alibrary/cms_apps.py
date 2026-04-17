from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from .cms_menus import (
    ReleaseMenu,
    ArtistMenu,
    LibraryMenu,
    MediaMenu,
    LabelMenu,
    PlaylistMenu,
    LicenseMenu,
)


@apphook_pool.register
class ReleaseApp(CMSApp):

    name = _("Release App")
    menus = [ReleaseMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_release"]


@apphook_pool.register
class ArtistApp(CMSApp):

    name = _("Artist App")
    menus = [ArtistMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_artist"]


@apphook_pool.register
class LabelApp(CMSApp):
    # app_name = "alibrary"
    name = _("Label App")
    menus = [LabelMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_label"]


@apphook_pool.register
class MediaApp(CMSApp):
    # app_name = 'alibrary-media'
    name = _("Media App")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_media"]

    def get_menus(self, page=None, language=None, **kwargs):
        return [MediaMenu]


@apphook_pool.register
class PlaylistApp(CMSApp):

    name = _("Playlist App")
    menus = [PlaylistMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_playlist"]


@apphook_pool.register
class LicenseApp(CMSApp):

    name = _("License App")
    menus = [LicenseMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_license"]


#######################################################################
# library app replaces single apps for:
# - release
# - artist
# - media
# - label
#######################################################################
@apphook_pool.register
class LibraryApp(CMSApp):
    app_name = "library"
    name = _("Library App")
    menus = [LibraryMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["alibrary.urls_library"]
