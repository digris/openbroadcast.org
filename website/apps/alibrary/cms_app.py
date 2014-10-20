from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from alibrary.menu import ReleaseMenu, ArtistMenu, LibraryMenu, MediaMenu, LabelMenu, PlaylistMenu, LicenseMenu


class ReleaseApp(CMSApp):
    
    name = _("Release App")
    urls = ["alibrary.urls_release"]
    menus = [ReleaseMenu]

apphook_pool.register(ReleaseApp)


class ArtistApp(CMSApp):
    
    name = _("Artist App")
    urls = ["alibrary.urls_artist"]
    menus = [ArtistMenu]

apphook_pool.register(ArtistApp)


class LabelApp(CMSApp):
    
    name = _("Label App")
    urls = ["alibrary.urls_label"]
    menus = [LabelMenu]

apphook_pool.register(LabelApp)


class MediaApp(CMSApp):
    
    name = _("Media App")
    urls = ["alibrary.urls_media"]
    menus = [MediaMenu]

apphook_pool.register(MediaApp)


class LibraryApp(CMSApp):
    
    name = _("Library App")
    urls = ["alibrary.urls_library"]
    menus = [LibraryMenu]

apphook_pool.register(LibraryApp)


class PlaylistApp(CMSApp):
    
    name = _("Playlist App")
    urls = ["alibrary.urls_playlist"]
    menus = [PlaylistMenu]

apphook_pool.register(PlaylistApp)


class LicenseApp(CMSApp):
    
    name = _("License App")
    urls = ["alibrary.urls_license"]
    menus = [LicenseMenu]

apphook_pool.register(LicenseApp)