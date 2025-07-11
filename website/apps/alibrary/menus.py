from django.core.urlresolvers import reverse
from simple_menu import Menu, MenuItem

print("simple_menu -----")


library_children = (
    MenuItem("Edit Profile",
        reverse("alibrary:release-list"),
        weight=10,
        icon="user"
    ),
)


Menu.add_item(
    "library", 
    MenuItem("My Account",
        reverse("alibrary:artist-list"),
        weight=10,
        children=library_children
    )
)