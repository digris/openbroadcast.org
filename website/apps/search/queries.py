# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from django_elasticsearch_dsl.search import Search
from base.utils.fold_to_ascii import fold
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


def format_search_results(results):

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


def autocomplete_search(q, doc_type=None, fuzzy_mode=False, **kwargs):

    query = autocomplete_query(q, fuzzy_mode)
    limit = kwargs.get('limit', 20)
    offset = kwargs.get('offset', 0)
    if limit and limit > 100:
        limit = 100

    s = Search().index('_all')

    if doc_type:
        s = s.doc_type(doc_type)


    s = s[offset:limit + offset]

    s = s.query('match', autocomplete=query)
    #s = s.query('multi_match', query='independent', fields=['description'])
    #s = s.highlight('description')

    return format_search_results(s.execute())


def autocomplete_query(q, fuzzy_mode=False):

    _ac_query = {
        'query': fold(q),
        'operator': 'and'
    }

    if fuzzy_mode:
        _ac_query.update({
            'fuzziness': 'AUTO',
        })

    return _ac_query

