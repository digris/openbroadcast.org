# -*- coding: utf-8 -*-
import logging
from navutils import menu

MENU_TEMPLATE = "navigation/menu.html"
NODE_TEMPLATE = "navigation/_menu_node.html"
ACCOUNT_NODE_TEMPLATE = "navigation/_menu_account_node.html"

# menu root nodes
main_menu = menu.Menu(
    "main",
    css_class="menu",
    template=MENU_TEMPLATE,
)
menu.register(main_menu)

home = menu.Node(
    id="home",
    label="Home",
    # pattern_name="home:index",
    url="/",
    template=NODE_TEMPLATE,
)
main_menu.register(home)

# catalog main nodes
main_menu.register(
    menu.Node(
        id="releases",
        label="Releases",
        # pattern_name="catalog:release-list",
        pattern_name="alibrary-release-list",
        template=NODE_TEMPLATE,
    )
)
