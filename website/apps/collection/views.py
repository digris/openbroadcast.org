# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.views.generic import DetailView
from el_pagination.views import AjaxListView

from .models import Collection

log = logging.getLogger(__name__)

# Create your views here.
class CollectionListView(AjaxListView):

    model = Collection

    template_name = "collection/collection_list.html"
    page_template = "collection/collection_list_page.html"

    _tagcloud = []
    _matches = []
    _filter = {}

    def get_queryset(self):

        qs = Collection.objects.all()
        qs = qs.prefetch_related("items")

        return qs

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)

        context.update({"tagcloud": self._tagcloud})

        return context


class CollectionDetailView(DetailView, AjaxListView):
    model = Collection
    slug_field = "slug"

    object_list = []
    template_name = "collection/collection_detail.html"
    page_template = "collection/collection_item_list_page.html"

    def get_context_data(self, **kwargs):
        context = super(CollectionDetailView, self).get_context_data(**kwargs)

        context.update(
            {
                "object_list": self.object.items.all(),
                "page_template": self.page_template,
            }
        )
        return context
