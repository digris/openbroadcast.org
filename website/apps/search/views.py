# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from django.views.generic import ListView
from django.db.models import Case, When
from django.http import HttpResponseBadRequest
from django.core.exceptions import SuspiciousOperation

from elasticsearch_dsl import FacetedSearch
from elasticsearch_dsl import Q as ESQ

from .queries import format_search_results
from . import utils


__all__ = ["BaseFacetedSearch", "BaseSearchListView"]


class SearchFacetException(Exception):
    pass


class SearchQueryException(Exception):
    pass


class BaseFacetedSearch(FacetedSearch):
    doc_types = []
    fields = ["tags", "name", "id"]

    facets = {
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html
        # 'tags': TermsFacet(field='tags', size=100),
    }

    def __init__(self, **kwargs):

        if not isinstance(self.facets, (list, OrderedDict)):
            raise SearchFacetException(
                "facets attribute must be a list or ordered dict"
            )

        self.facets = OrderedDict(self.facets)
        super(BaseFacetedSearch, self).__init__(**kwargs)

    def query(self, search, query):

        s = search

        _searches = query.get("searches", None)
        _options = query.get("options", None)

        if not _searches:
            return s

        # elasticsearch 'must' queries
        _musts = []
        _must_nots = []

        for key, value in _searches.items():
            # not particularly nice - maybe there is a better way to build queries here
            # 'q' - the main search query
            if key == "q":
                if _options.get("fuzzy", True):
                    _q = ESQ(
                        "match",
                        autocomplete={
                            "query": " ".join(value),
                            "operator": "and",
                            "fuzziness": "AUTO",
                        },
                    )
                else:
                    _q = ESQ(
                        "match",
                        autocomplete={"query": " ".join(value), "operator": "and"},
                    )
                _musts.append(_q)

            # 'id' - for pre-filtered querysets
            elif key == "ids":
                _musts.append(ESQ("terms", _id=value))

            # 'tags' - for 'intersection-style' tagcloud
            elif key == "tags":
                for tag in value:
                    _musts.append(ESQ("term", tags=tag))
            else:
                for v in value:
                    if not v[0:1] == "-":
                        # print('must', v)
                        _musts.append(ESQ("term", **{key: v}))
                    else:
                        # print('must not', v[1:])
                        _must_nots.append(ESQ("term", **{key: v[1:]}))

        if _musts or _must_nots:
            s.query = ESQ("bool", must=_musts, must_not=_must_nots)

        return s


class BaseSearchListView(ListView):

    search_class = None
    order_by = []
    _search_result = None
    _formatted_search_result = None

    def get(self, request, *args, **kwargs):
        try:
            return super(BaseSearchListView, self).get(request, *args, **kwargs)
        except (SearchFacetException, SearchQueryException) as e:
            return HttpResponseBadRequest("{}".format(e))

    def get_search_query(self, **kwargs):
        return utils.parse_search_query(request=self.request)

    def get_queryset(self, limit_ids=None, **kwargs):

        search_query = self.get_search_query()

        if limit_ids:
            search_query["searches"]["ids"] = limit_ids

        # initialize search class
        try:
            s = self.search_class(
                query=search_query,
                filters=search_query["filters"],
                sort=search_query["order_by"],
            )
        except KeyError:
            raise SearchQueryException("Invalid search criteria")

        # handle pagination
        pagination_query = utils.parse_pagination_query(request=self.request)
        s = s[pagination_query["start"] : pagination_query["end"]]

        # execute elasticsearch query
        try:
            result = s.execute()
        except Exception as e:
            raise SearchQueryException("Unable to execute search query: {}".format(e))

        formatted_result = format_search_results(result)

        # get object pks and create corresponding queryset
        pks = [r["id"] for r in formatted_result["results"] if r["ct"]]
        qs = self.model.objects.filter(pk__in=pks)
        qs = qs.order_by(Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)]))

        # add search query & result as reference
        self._search_query = search_query
        self._search_result = result
        self._formatted_search_result = formatted_result

        return qs

    def get_context_data(self, **kwargs):
        context = super(BaseSearchListView, self).get_context_data(**kwargs)

        search_result = self._search_result
        formatted_search_result = self._formatted_search_result
        pagination_query = utils.parse_pagination_query(request=self.request)
        pagination = utils.get_pagination_data(
            result=search_result, query=pagination_query
        )

        try:
            tagcloud = utils.get_tagcloud_data(
                tags=search_result.facets.tags, request=self.request
            )
        except:
            tagcloud = []

        filters = utils.get_filter_data(
            facets=search_result.facets, facets_definition=self.search_class.facets
        )
        ordering = utils.get_ordering_data(
            order_options=self.order_by,
            search_query=self._search_query,
            request=self.request,
        )

        context.update(
            {
                # 'facets': search_result.facets,
                # 'num_results': search_result.hits.total,
                "search_result": search_result,  # raw search result
                "search_results_by_id": formatted_search_result.get(
                    "results_by_id", {}
                ),
                "pagination": pagination,
                "tagcloud": tagcloud,
                "filters": filters,
                "ordering": ordering,
            }
        )

        return context
