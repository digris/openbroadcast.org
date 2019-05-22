# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

# mapping for auth services display
# TODO: this is not really nice... think about a better implementation

BACKEND_DETAILS = {
    "email": {
        "name": "Login",
        "icon": "icon-email-secure slim",
        "hint": _("your Email Account"),
    },
    "facebook": {
        "name": "Facebook",
        "icon": "facebook",
        "hint": _("Continue with Facebook"),
    },
    "google-oauth2": {
        "name": "Google",
        "icon": "google",
        "hint": _("your Google Account"),
    },
    "github": {
        "name": "Github",
        "icon": "github",
        "hint": _("your Github Account"),
    },
    "vk-oauth2": {"name": "VK", "icon": "vk", "hint": _("your VK Account")},
    "spotify": {
        "name": "Spotify",
        "icon": "spotify",
        "hint": _("your Spotify Account"),
    },
}
