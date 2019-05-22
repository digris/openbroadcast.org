#-*- coding: utf-8 -*-

import djclick as click

@click.group()
def cli():
    """Search CLI"""
    pass


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

