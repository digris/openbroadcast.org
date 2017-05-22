from django.conf import settings

from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine


class UnstemmedElasticsearchSearchBackend(ElasticsearchSearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(UnstemmedElasticsearchSearchBackend, self).__init__(
            connection_alias, **connection_options)

        setattr(self, 'DEFAULT_SETTINGS', settings.ELASTICSEARCH_INDEX_SETTINGS)


class UnstemmedElasticsearchSearchEngine(ElasticsearchSearchEngine):

    backend = UnstemmedElasticsearchSearchBackend
