from navutils import menu

main_menu = menu.Menu(
    id='main',
    template='element/topbar/_menu.html',
    css_class='menu menu-level-1',
)
menu.register(main_menu)


#######################################################################
# catalog
#######################################################################
catalog_menu = menu.Node(
    id='catalog',
    template='element/topbar/_menu-node.html',
    label='Catalog',
    pattern_name='alibrary:release-list'
)
main_menu.register(catalog_menu)

catalog_menu.add(
    menu.Node(
        id='release-list',
        template='element/topbar/_menu-node.html',
        label='Releases',
        pattern_name='alibrary:release-list'
    )
)

catalog_menu.add(
    menu.Node(
        id='artist-list',
        template='element/topbar/_menu-node.html',
        label='Artists',
        pattern_name='alibrary:artist-list'
    )
)

catalog_menu.add(
    menu.Node(
        id='media-list',
        template='element/topbar/_menu-node.html',
        label='Tracks',
        pattern_name='alibrary:media-list'
    )
)

catalog_menu.add(
    menu.Node(
        id='label-list',
        template='element/topbar/_menu-node.html',
        label='Labels',
        pattern_name='alibrary:label-list'
    )
)


#######################################################################
# catalog playlists
#######################################################################
catalog_playlists_menu = menu.Node(
    id='catalog-playlists',
    template='element/topbar/_menu-node.html',
    label='Playlists',
    pattern_name='alibrary:playlist-list',
    # css_class='selected',
)
main_menu.register(catalog_playlists_menu)

catalog_playlists_menu.add(
    menu.Node(
        id='playlist-list',
        template='element/topbar/_menu-node.html',
        label='Public Playlists',
        pattern_name='alibrary:playlist-list'
    )
)

catalog_playlists_menu.add(
    menu.Node(
        id='playlist-list-own',
        template='element/topbar/_menu-node.html',
        label='My Playlists',
        pattern_name='alibrary:playlist-list-own'
    )
)


#######################################################################
# scheduler
#######################################################################
scheduler_menu = menu.Node(
    id='scheduler',
    template='element/topbar/_menu-node.html',
    label='Scheduler',
    pattern_name='abcast:scheduler',
)
main_menu.register(scheduler_menu)


#######################################################################
# profiles / network
#######################################################################
network_menu = menu.Node(
    id='network',
    template='element/topbar/_menu-node.html',
    label='Newtork',
    pattern_name='profiles:profile-list',
)
main_menu.register(network_menu)

network_menu.add(
    menu.Node(
        id='profile-list',
        template='element/topbar/_menu-node.html',
        label='Users',
        pattern_name='profiles:profile-list'
    )
)

network_menu.add(
    menu.Node(
        id='station-list',
        template='element/topbar/_menu-node.html',
        label='Stations',
        pattern_name='abcast-network:station-list'
    )
)

network_menu.add(
    menu.Node(
        id='activity-list',
        template='element/topbar/_menu-node.html',
        label='Activities',
        pattern_name='actstream:action-list'
    )
)



#######################################################################
# external links
#######################################################################
docs_menu = menu.Node(
    id='docs',
    label='Docs',
    url='http://openbroadcast-platform.readthedocs.io/',
    link_attrs={
        'target': '_blank'
    }
)
main_menu.register(docs_menu)
