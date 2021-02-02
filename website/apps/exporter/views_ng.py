# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView


class ExporterIndexView(TemplateView):
    template_name = "exporter/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExporterIndexView, self).get_context_data(**kwargs)
        return context
