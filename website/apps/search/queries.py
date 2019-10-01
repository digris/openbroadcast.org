# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_elasticsearch_dsl.search import Search
from base.utils.fold_to_ascii import fold


def format_search_results(results):

    ignored_keys = ["autocomplete"]

    results = results.to_dict()

    _results = []
    _results_by_id = {}

    for hit in results["hits"]["hits"]:

        source = hit["_source"]
        item = {"score": hit["_score"], "id": int(hit["_id"]), "ct": hit["_type"]}

        for k, v in source.items():
            if not k in [ignored_keys]:
                item[k] = v

        _results.append(item)
        _results_by_id[int(hit["_id"])] = item

    response = {
        "results": _results,
        "results_by_id": _results_by_id,
        #'results_raw': results['hits']['hits'],
        "total": results["hits"]["total"],
        "max_score": results["hits"]["max_score"],
    }

    return response


def autocomplete_search(q, doc_type=None, fuzzy_mode=False, **kwargs):

    query = autocomplete_query(q, fuzzy_mode)
    limit = kwargs.get("limit", 20)
    offset = kwargs.get("offset", 0)
    filters = kwargs.get("filters", {})

    if limit and limit > 100:
        limit = 100

    s = Search().index("_all")

    if doc_type:
        s = s.doc_type(doc_type)

    s = s.query("match", autocomplete=query)

    # TODO: implement in a generic way
    # add filters like: `&filter_status=Ready&filter_type=Broadcasts`
    for key, value in filters.iteritems():
        s = s.query("term", **{key: value[0]})

    s = s[offset : limit + offset]

    return format_search_results(s.execute())


def autocomplete_query(q, fuzzy_mode=False):

    _ac_query = {"query": fold(q), "operator": "and"}

    if fuzzy_mode:
        _ac_query.update({"fuzziness": "AUTO"})

    return _ac_query
