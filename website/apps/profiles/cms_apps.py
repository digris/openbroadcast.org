# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .cms_menus import ProfileMenu


@apphook_pool.register
class ProfileApp(CMSApp):
    # app_name = 'profiles'
    name = _("Profile App")
    menus = [ProfileMenu]

    def get_urls(self, page=None, language=None, **kwargs):
        return ["profiles.urls_profile"]
