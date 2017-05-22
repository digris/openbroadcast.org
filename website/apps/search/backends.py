# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine

#######################################################################
# https://wellfire.co/learn/custom-haystack-elasticsearch-backend/
# http://stackoverflow.com/questions/18201147/django-haystack-how-to-\
# force-exact-attribute-match-without-stemming
#######################################################################

class UnstemmedElasticsearchSearchBackend(ElasticsearchSearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(UnstemmedElasticsearchSearchBackend, self).__init__(
            connection_alias, **connection_options)

        setattr(self, 'DEFAULT_SETTINGS', settings.ELASTICSEARCH_INDEX_SETTINGS)


class UnstemmedElasticsearchSearchEngine(ElasticsearchSearchEngine):

    backend = UnstemmedElasticsearchSearchBackend
