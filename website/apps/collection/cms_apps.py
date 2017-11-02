# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


#######################################################################
# collection app
#######################################################################
class CollectionApp(CMSApp):
    name = _('Collection App')
    app_name = 'collection'

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            'collection.urls',
        ]

apphook_pool.register(CollectionApp)
