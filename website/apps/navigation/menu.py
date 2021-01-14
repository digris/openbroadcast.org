# -*- coding: utf-8 -*-
import logging
from navutils import menu

MENU_TEMPLATE = "navigation/menu.html"
NODE_TEMPLATE = "navigation/_menu_node.html"
ACCOUNT_NODE_TEMPLATE = "navigation/_menu_account_node.html"

# menu root nodes
main_menu = menu.Menu(
    "main_menu",
    css_class="menu",
    template=MENU_TEMPLATE,
)
menu.register(main_menu)

catalog_menu = menu.Node(
    id="catalog",
    attrs={
        "data-level": 0,
    },
    label="Catalog",
    # pattern_name="alibrary-release-list",
    url="/content/library/",
    template=NODE_TEMPLATE,
    children=[
        menu.Node(
            id="releases",
            attrs={
                "data-level": 1,
                "data-parent-id": "catalog",
            },
            label="Releases",
            # pattern_name="catalog:release-list",
            pattern_name="alibrary-release-list",
            template=NODE_TEMPLATE,
        ),
        menu.Node(
            id="artists",
            attrs={
                "data-level": 1,
                "data-parent-id": "catalog",
            },
            label="Artists",
            # pattern_name="catalog:release-list",
            pattern_name="alibrary-artist-list",
            template=NODE_TEMPLATE,
        ),
    ],
)

playlist_menu = menu.Node(
    id="playlists",
    attrs={
        "data-level": 0,
    },
    label="Playlists",
    # pattern_name="alibrary-release-list",
    url="/content/library/",
    template=NODE_TEMPLATE,
    children=[
        menu.Node(
            id="public",
            attrs={
                "data-level": 1,
                "data-parent-id": "playlists",
            },
            label="Public Playlists",
            # pattern_name="catalog:release-list",
            pattern_name="alibrary-release-list",
            template=NODE_TEMPLATE,
        ),
        menu.AuthenticatedNode(
            id="private",
            attrs={
                "data-level": 1,
                "data-parent-id": "playlists",
            },
            label="My Playlists",
            # pattern_name="catalog:release-list",
            pattern_name="alibrary-artist-list",
            template=NODE_TEMPLATE,
        ),
    ],
)

program_menu = menu.Node(
    id="program",
    attrs={
        "data-level": 0,
    },
    label="Program",
    # pattern_name="alibrary-release-list",
    url="/content/library/",
    template=NODE_TEMPLATE,
)

network_menu = menu.Node(
    id="network",
    attrs={
        "data-level": 0,
    },
    label="Network",
    url="/network/",
    template=NODE_TEMPLATE,
    children=[
        menu.Node(
            id="users",
            attrs={
                "data-level": 1,
                "data-parent-id": "network",
            },
            label="Users",
            url="/network/users/",
            template=NODE_TEMPLATE,
        ),
        menu.Node(
            id="activities",
            attrs={
                "data-level": 1,
                "data-parent-id": "network",
            },
            label="Activities",
            url="/network/activities/",
            template=NODE_TEMPLATE,
        ),
    ],
)

about_menu = menu.Node(
    id="about",
    attrs={
        "data-level": 0,
    },
    label="About",
    url="/about/",
    template=NODE_TEMPLATE,
    children=[
        menu.Node(
            id="contact",
            attrs={
                "data-level": 1,
                "data-parent-id": "about",
            },
            label="Contact",
            url="/network/users/",
            template=NODE_TEMPLATE,
        ),
        menu.Node(
            id="documentation",
            attrs={
                "data-level": 1,
                "data-parent-id": "about",
            },
            label="Documentation",
            url="/network/users/",
            template=NODE_TEMPLATE,
        ),
    ],
)

main_menu.register(catalog_menu)
main_menu.register(playlist_menu)
main_menu.register(program_menu)
main_menu.register(network_menu)
main_menu.register(about_menu)
