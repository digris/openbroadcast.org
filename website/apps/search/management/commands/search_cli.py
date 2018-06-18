#-*- coding: utf-8 -*-

import os
import djclick as click
from django.contrib.auth.models import User
from django.conf import settings

from massimporter.models import Massimport, MassimportFile

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search



@click.group()
def cli():
    """Massimporter CLI"""
    pass



@cli.command()
@click.option('--query', '-q', type=unicode, required=False)
def query(query):

    click.echo(u'query: {}'.format(query))


    from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet, Search

    from alibrary.documents import ArtistDocument, LabelDocument

    # class BlogSearch(Search):
    #     doc_types = [ArtistDocument, LabelDocument]
    #     #doc_types = '_all'
    #     # fields that should be searched
    #     fields = ['name', 'description']

    s = Search()

    bs = BlogSearch(query)

    response = bs.execute()
    print(response.hits.total, 'hits total')
    for hit in response:
        print(hit.meta.__dict__)
        print(hit.meta.score, hit.name)
        print(hit.meta.highlight)
        print('*' * 72)




@cli.command()
@click.option('--query', '-q', type=unicode, required=False)
def label(query):

    click.echo(u'query: {}'.format(query))

    from datetime import date

    from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet

    from alibrary.documents import LabelDocument

    class LabelSearch(FacetedSearch):
        doc_types = [LabelDocument]
        # fields that should be searched
        fields = ['tags', 'name',]

        facets = {
            # use bucket aggregations to define facets
            #'tags': TermsFacet(field='tags', size=5),
            'country': TermsFacet(field='country'),
            #'publishing_frequency': DateHistogramFacet(field='published_from', interval='month')
        }

        # def search(self, *args, **kwargs):
        #     # override methods to add custom pieces
        #     # s = super().search()
        #     s = super(BlogSearch, self).search(*args, **kwargs)
        #     return s.filter('range', publish_from={'lte': 'now/h'})



        def query(self, search, query):
            """
            Add query part to ``search``.

            Override this if you wish to customize the query used.
            """
            if query:
                return search.update_from_dict(query)
            return search



    #bs = BlogSearch('python web', {'publishing_frequency': date(2015, 6)})


    _query = {
        "query": {
            "match" : {
                "autocomplete" : {
                    "query": query,
                    "fuzziness": "AUTO",
                    "operator" : "and"
                }
            }
        },
        # "highlight" : {
        #     "fields" : {
        #         "name" : {}
        #     }
        # }
    }

    s = LabelSearch(query=_query, filters={'country': ['CH', 'JP']})


    # s.to_queryset()

    #s = s.from_dict(_query)
    #s.update_from_dict(_query)
    #bs = bs.filter({'country': ['CH']})

    response = s.execute()

    # access hits and other attributes as usual
    print(response.hits.total, 'hits total')
    for hit in response:
        print(hit.meta.score, hit.name)

    # for (tag, count, selected) in response.facets.tags:
    #     print(tag, ' (SELECTED):' if selected else ':', count)

    for c in response.facets.country:
        print(c)

    # for (month, count, selected) in response.facets.publishing_frequency:
    #     print(month.strftime('%B %Y'), ' (SELECTED):' if selected else ':', count)




@cli.command()
@click.option('--query', '-q', type=unicode, required=False)
def facet(query):

    click.echo(u'query: {}'.format(query))

    from datetime import date

    from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet

    from alibrary.documents import ArtistDocument, LabelDocument

    class BlogSearch(FacetedSearch):
        doc_types = [ArtistDocument, LabelDocument]
        # fields that should be searched
        fields = ['tags', 'name',]

        facets = {
            # use bucket aggregations to define facets
            'tags': TermsFacet(field='tags', size=5),
            'country': TermsFacet(field='country'),
            #'publishing_frequency': DateHistogramFacet(field='published_from', interval='month')
        }

        # def search(self, *args, **kwargs):
        #     # override methods to add custom pieces
        #     # s = super().search()
        #     s = super(BlogSearch, self).search(*args, **kwargs)
        #     return s.filter('range', publish_from={'lte': 'now/h'})

    #bs = BlogSearch('python web', {'publishing_frequency': date(2015, 6)})
    bs = BlogSearch(query, {'country': ['AL'], 'tags': ['Tech Funk']})

    #bs = bs.filter({'country': ['CH']})

    response = bs.execute()

    # access hits and other attributes as usual
    print(response.hits.total, 'hits total')
    for hit in response:
        print(hit.meta.score, hit.name)

    for (tag, count, selected) in response.facets.tags:
        print(tag, ' (SELECTED):' if selected else ':', count)

    for c in response.facets.country:
        print(c)

    # for (month, count, selected) in response.facets.publishing_frequency:
    #     print(month.strftime('%B %Y'), ' (SELECTED):' if selected else ':', count)

