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
        "icon": "facebook",
        "cta": _("Login with Facebook"),
    },
    "soundcloud": {
        "name": "Soundcloud",
        "icon": "icon-soundcloud",
        "cta": _("Continue with Soundcloud"),
    },
    "twitter": {
        "name": "Twitter",
        "icon": "icon-twitter",
        "cta": _("Continue with Twitter"),
    },
    "google-oauth2": {
        "name": "Google",
        "icon": "google",
        "cta": _("Login with Google"),
    },
    "dropbox-oauth2": {
        "name": "Dropbox",
        "icon": "icon-dropbox",
        "cta": _("Continue with Dropbox"),
    },
    "github": {"name": "Github", "icon": "github", "cta": _("Continue with Github")},
    "vk-oauth2": {"name": "VK", "icon": "vk", "hint": _("Continue with VK")},
    "spotify": {
        "name": "Spotify",
        "icon": "spotify",
        "cta": _("Continue with Spotify"),
    },
}
