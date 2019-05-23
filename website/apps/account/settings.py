# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

# mapping for auth services display
# TODO: this is not really nice... think about a better implementation

BACKEND_DETAILS = {
    "email": {
        "name": "Login",
        "icon": "icon-email-secure slim",
        "cta": _("Continue with your Email account"),
    },
    "facebook": {
        "name": "Facebook",
        "icon": "icon-facebook",
        "cta": _("Continue with Facebook"),
    },
    "google-oauth2": {
        "name": "Google",
        "icon": "icon-google-plus",
        "cta": _("Continue with Google"),
    },
    "github": {
        "name": "Github",
        "icon": "github",
        "cta": _("Continue with Github"),
    },
    "vk-oauth2": {"name": "VK", "icon": "vk", "hint": _("Continue with VK")},
    "spotify": {
        "name": "Spotify",
        "icon": "spotify",
        "cta": _("Continue with Spotify"),
    },
}
