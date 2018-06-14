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

from ..queries import autocomplete_search, format_results


# def format_results(results):
#
#     results = results.to_dict()
#
#     response = {
#         'results': results['hits']['hits'],
#         'total': results['hits']['total'],
#         'max_score': results['hits']['max_score'],
#     }
#
#     return response
#
#
# def autocomplete_search(q, exact_mode=False):
#
#     _ac_query = {
#         'query': q,
#         'operator': 'and'
#     }
#
#     if not exact_mode:
#         _ac_query.update({
#             'fuzziness': 'AUTO',
#         })
#
#     s = Search().index('_all')
#     s = s.query("match", autocomplete=_ac_query)
#
#     return s.execute()


@api_view()
def search_global(request):

    q = request.GET.get('q', None)
    exact_mode = request.GET.get('exact', False) == '1'

    if q:
        q = q.strip().lower()

        response = autocomplete_search(q, exact_mode=exact_mode)
        # response = format_results(results)

        return Response(response)

    return Response({
        'q': q
    })


# @api_view()
# def search_global(request):
#
#     q = request.GET.get('q', None)
#
#     if q:
#
#         q = q.strip()
#         s = Search().index('library')
#
#         print('q: {}'.format(q))
#
#
#         # query
#         #q = Term(name={"term": q})
#         q = Q("multi_match", query=q, fields=['name', 'members'])
#
#         x = s.query(q)
#
#         _results_q = x.execute()
#
#         print('/' * 72)
#         print(x)
#         print('/' * 72)
#         print(_results_q)
#         print('/' * 72)
#
#
#
#         # suggest
#
#
#
#         # results_q = []
#         # for r in _results_q:
#         #     results_q.append({
#         #         'name': r.name,
#         #         #'members': r.members,
#         #         #'aliases': r.aliases,
#         #     })
#
#         results_q = _results_q.to_dict()['hits']['hits']
#
#         return Response({
#             'results': results_q,
#             'results_raw': results_q
#         })
#
#     return Response({
#         'q': q
#     })



# @api_view()
# def search_global(request):
#
#     q = request.GET.get('q', None)
#
#     if q:
#
#         query = parse_query_string(q.strip())
#
#
#
#         sqs = SearchQuerySet().autocomplete(content=query['q'])
#
#         if query['scope']:
#             search_models = [
#                 apps.get_model(*query['scope'].split('.'))
#             ]
#             sqs = sqs.models(*search_models)
#
#         sqs = sqs.load_all()
#
#         results = []
#         for r in sqs[:20]:
#             results.append({
#                 'name': r.name,
#                 'uuid': r.object.uuid,
#                 'ct': r.object.__class__.__name__.lower(),
#                 'detail_url': r.object.get_absolute_url(),
#                 #'image': r.object.key_image.file.crop['512x512'].url if r.object.key_image else None,
#             })
#
#         return Response({
#             'results': results
#         })
#
#     return Response({
#         'q': q
#     })




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
