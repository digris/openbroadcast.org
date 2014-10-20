from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import Modifier, Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu


class LibraryMenu(CMSAttachMenu):
    
    name = _("Library Menu")
    
    def get_nodes(self, request):
        nodes = []
        """
        node = NavigationNode(
            _('Releases'),
            reverse('alibrary-release-list', args=[]),
            123
        )
        nodes.append(node)
        node = NavigationNode(
            _('Artists'),
            reverse('ArtistListlView', args=[]),
            123
        )
        nodes.append(node)
        """
        
        return nodes
    
menu_pool.register_menu(LibraryMenu)






class ReleaseMenu(CMSAttachMenu):
    
    name = _("Release Menu")
    
    def get_nodes(self, request):
        nodes = []
        """
        for release in Release.objects.active():
            try:
                node = NavigationNode(
                    release.name,
                    reverse('alibrary-release-detail', args=[release.slug]),
                    release.pk
                )
                nodes.append(node)
                #print 'added'
            except Exception, e:
                print e
        """    

        return nodes
    
menu_pool.register_menu(ReleaseMenu)



class MediaMenu(CMSAttachMenu):
    
    name = _("Media/Track Menu")
    
    def get_nodes(self, request):
        nodes = []
        return nodes
    
menu_pool.register_menu(MediaMenu)




class ArtistMenu(CMSAttachMenu):
    
    name = _("Artist Menu")
    
    def get_nodes(self, request):
        nodes = []
        """
        for artist in Artist.objects.listed():
            try:
                node = NavigationNode(
                    artist.name,
                    reverse('alibrary-artist-detail', args=[artist.slug]),
                    artist.pk
                )
                nodes.append(node)
                print 'added'
            except Exception, e:
                print e
        """

        return nodes
    
menu_pool.register_menu(ArtistMenu)

class LabelMenu(CMSAttachMenu):
    
    name = _("Label Menu")
    
    def get_nodes(self, request):
        nodes = []
        return nodes
    
menu_pool.register_menu(LabelMenu)


class PlaylistMenu(CMSAttachMenu):
    
    name = _("Playlist Menu")
    
    def get_nodes(self, request):
        nodes = []


        """
        node = NavigationNode(
            _('Broadcast Playlists'),
            reverse('alibrary-playlist-type-list', args=['broadcast']),
            301
        )
        nodes.append(node)

        node = NavigationNode(
            _('My Broadcast Playlists'),
            reverse('alibrary-playlist-type-list', kwargs={'type': 'broadcast', 'user': request.user}),
            302
        )
        nodes.append(node)
        
        node = NavigationNode(
            _('All Shared Playlists'),
            reverse('alibrary-playlist-type-list', args=['playlist']),
            311
        )
        nodes.append(node)
        
        node = NavigationNode(
            _('My Shared Playlists'),
            reverse('alibrary-playlist-type-list', kwargs={'type': 'playlist', 'user': request.user}),
            312
        )
        nodes.append(node)
        
        node = NavigationNode(
            _('My Private Playlists'),
            reverse('alibrary-playlist-type-list', kwargs={'type': 'basket', 'user': request.user}),
            321
        )
        nodes.append(node)
        """


        node = NavigationNode(
            _('All Playlists'),
            reverse('alibrary-playlist-list'),
            301
        )
        nodes.append(node)

        node = NavigationNode(
            _('My Playlists'),
            reverse('alibrary-playlist-user-list', kwargs={'user': request.user}),
            302
        )
        nodes.append(node)

        
        return nodes
    
menu_pool.register_menu(PlaylistMenu)


class LicenseMenu(CMSAttachMenu):
    
    name = _("License Menu")
    
    def get_nodes(self, request):
        nodes = []
        return nodes
    
menu_pool.register_menu(LicenseMenu)





























class Level(Modifier):
    """
    marks all node levels
    """
    post_cut = True

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        if breadcrumb:
            return nodes
        for node in nodes:
            if not node.parent:
                if post_cut:
                    node.menu_level = 0
                else:
                    node.level = 0
                self.mark_levels(node, post_cut)
        return nodes

    def mark_levels(self, node, post_cut):
        for child in node.children:
            
            # print child
            
            if post_cut:
                child.menu_level = node.menu_level + 1
            else:
                child.level = node.level + 1
            self.mark_levels(child, post_cut)

menu_pool.register_modifier(Level)