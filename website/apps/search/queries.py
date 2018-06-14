# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from django_elasticsearch_dsl.search import Search
from alibrary.documents import ArtistDocument, LabelDocument

ALL_DOCUMENT_CLASSES = [
    ArtistDocument,
    LabelDocument
]

# class GlobalSearch(FacetedSearch):
#     doc_types = ALL_DOCUMENT_CLASSES
#     fields = ['name', 'description']
#
# def global_search_query(query=None):
#     s = GlobalSearch(query)
#
#     pass


def format_results(results):

    ignored_keys = [
        'autocomplete',
    ]

    results = results.to_dict()

    _results = []

    for hit in results['hits']['hits']:

        source = hit['_source']
        item = {
            'score': hit['_score'],
            'id': int(hit['_id']),
            'ct': hit['_type'],
        }

        for k, v in source.items():
            if not k in [ignored_keys]:
                item[k] = v

        _results.append(item)

        # _results.append({
        #     'name': source['name'],
        #     'tags': source['tags'],
        # })

    response = {
        'results': _results,
        #'results_raw': results['hits']['hits'],
        'total': results['hits']['total'],
        'max_score': results['hits']['max_score'],
    }

    return response


def autocomplete_search(q, exact_mode=False):

    _ac_query = {
        'query': q,
        'operator': 'and'
    }

    if not exact_mode:
        _ac_query.update({
            'fuzziness': 'AUTO',
        })

    s = Search().index('_all')
    s = s.query("match", autocomplete=_ac_query)

    return format_results(s.execute())
