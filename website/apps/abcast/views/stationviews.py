# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from abcast.models import Station
from django.db.models import Q
from django.views.generic import DetailView, ListView
from pure_pagination.mixins import PaginationMixin


class StationListView(PaginationMixin, ListView):

    object = Station
    paginate_by = 24

    model = Station
    extra_context = {}

    def __init__(self, **kwargs):
        super(StationListView, self).__init__(**kwargs)
        self.relation_filter = []

    def get_context_data(self, **kwargs):
        context = super(StationListView, self).get_context_data(**kwargs)
        self.extra_context["list_style"] = self.request.GET.get("list_style", "s")
        self.extra_context["get"] = self.request.GET
        context.update(self.extra_context)

        return context

    def get_queryset(self, **kwargs):

        q = self.request.GET.get("q", None)

        if q:
            qs = Station.objects.filter(Q(name__istartswith=q)).distinct()
        else:
            qs = Station.objects.all()

        order_by = self.request.GET.get("order_by", None)
        direction = self.request.GET.get("direction", None)

        if order_by and direction:
            if direction == "descending":
                qs = qs.order_by("-%s" % order_by)
            else:
                qs = qs.order_by("%s" % order_by)

        return qs


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
