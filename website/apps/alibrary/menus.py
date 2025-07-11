from django.core.urlresolvers import reverse
from simple_menu import Menu, MenuItem

print("simple_menu -----")


library_children = (
    MenuItem("Edit Profile",
        reverse("accounts.views.editprofile"),
        weight=10,
        icon="user"
    ),
)


Menu.add_item(
    "library", 
    MenuItem("My Account",
        reverse("accounts.views.myaccount"),
        weight=10,
        children=library_children
    )
)