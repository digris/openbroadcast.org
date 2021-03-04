# -*- coding: utf-8 -*-
import logging

from abcast.models import Emission, Channel
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

log = logging.getLogger(__name__)


class EmissionDetailView(DetailView):

    model = Emission
    template_name = "abcast/emission/detail.html"

    def get_context_data(self, **kwargs):
        context = super(EmissionDetailView, self).get_context_data(**kwargs)
        return context


class SchedulerIndex(TemplateView):

    template_name = "abcast/scheduler.html"

    def get_context_data(self, **kwargs):
        context = super(SchedulerIndex, self).get_context_data(**kwargs)

        channel_id = 1
        read_only = not self.request.user.is_authenticated() or not self.request.user.has_perm(
            "abcast.schedule_emission"
        )

        context.update(
            {
                "channel": get_object_or_404(Channel, id=channel_id),
                "read_only": read_only,
            }
        )

        return context
