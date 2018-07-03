# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from haystack.query import SearchQuerySet

# from elasticsearch_dsl import DocType, Date, Search
# from elasticsearch_dsl.query import MultiMatch, Match, Fuzzy, Term, Q

#from elasticsearch_dsl import Search
from django_elasticsearch_dsl.search import Search

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.apps import apps

from ..queries import autocomplete_search, format_search_results


@api_view()
def search_global(request, **kwargs):

    q = request.GET.get('q', None)
    fuzzy_mode = request.GET.get('fuzzy', False) == '1'
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))
    # get ct from either GET or kwargs
    doc_type = request.GET.get('ct', kwargs.get('ct', None))

    if q:
        q = q.strip().lower()
        if len(q) > 1 and q[1] == ':':
            q = q[2:].strip()

        if doc_type == '_all':
            doc_type = None

        response = autocomplete_search(q, doc_type=doc_type, fuzzy_mode=fuzzy_mode, limit=limit, offset=offset)

        return Response(response)

    return Response({
        'q': q
    })


CT_MAP = [
    ('a', 'catalog.artist'),
    ('r', 'catalog.release'),
    ('l', 'catalog.label'),
    ('p', 'catalog.playlist'),
    ('t', 'catalog.media'),
]


def parse_query_string(q):

    query = {
        'scope': None,
        'q': q.strip()
    }

    for ct in CT_MAP:
        if q.startswith('{}:'.format(ct[0])):
            query.update({
                'scope': ct[1],
                'q': q[2:].strip()
            })
            return query

    return query
