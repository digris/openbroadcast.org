# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import requests
from elasticsearch import Elasticsearch
from django.conf import settings

ELASTICSEARCH_DSL = getattr(settings, 'ELASTICSEARCH_DSL', {})

try:
    host = ELASTICSEARCH_DSL.get('default').get('hosts')
except:
    host = 'localhost:9200'

client = Elasticsearch(host)

def get_ids_for_possible_duplicates(index=None, fields=[]):

    _script = ''
    for field in fields:
        _script += 'doc[\'{}.raw\'].value + '.format(field)

    response = client.search(
        index="releases",
        body={
            "aggs": {
                "duplicates": {
                    "terms": {
                        "script": _script.strip(' +'),
                        "size": 10000,
                        "min_doc_count": 2
                    },
                    "aggs": {
                        "duplicates": {
                            "top_hits": {
                                "_source": {
                                    "includes": [
                                        "id",
                                        "name",
                                        "artist_display"
                                    ]
                                },
                                "size": 20
                            }
                        }
                    }
                }
            }
        }
    )

    limit_ids = []

    for entry in response['aggregations']['duplicates']['buckets']:
        for hit in entry['duplicates']['hits']['hits']:
            limit_ids.append(int(hit['_id']))

    return limit_ids
