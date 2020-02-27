# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from abcast.models import Station
from django.db.models import Q
from django.views.generic import DetailView, ListView
from pure_pagination.mixins import PaginationMixin


class StationListView(PaginationMixin, ListView):

    paginate_by = 24

    model = Station
    extra_context = {}

    def __init__(self, **kwargs):
        super(StationListView, self).__init__(**kwargs)
        self.relation_filter = []

    def get_context_data(self, **kwargs):
        context = super(StationListView, self).get_context_data(**kwargs)
        context.update(self.extra_context)

        return context

    def get_queryset(self, **kwargs):

        return self.model.objects.all().order_by('name')



class StationDetailView(DetailView):

    context_object_name = "station"
    model = Station
    extra_context = {}

    def render_to_response(self, context, **kwargs):
        return super(StationDetailView, self).render_to_response(
            context, content_type="text/html"
        )

    def get_context_data(self, **kwargs):

        obj = kwargs.get("object", None)
        context = super(StationDetailView, self).get_context_data(**kwargs)
        self.extra_context["members"] = obj.members.all()
        context.update(self.extra_context)

        return context
