# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.views.generic import TemplateView

log = logging.getLogger(__name__)


class PlayerIndexView(TemplateView):

    template_name = "player/index.html"

    def get_context_data(self, **kwargs):
        context = super(PlayerIndexView, self).get_context_data(**kwargs)

        return context


class PlayerNextIndexView(TemplateView):

    template_name = "player/index_next.html"

    def get_context_data(self, **kwargs):
        context = super(PlayerNextIndexView, self).get_context_data(**kwargs)

        return context
