# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from celery import shared_task
from django_elasticsearch_dsl.registries import registry

log = logging.getLogger(__name__)

@shared_task
def update_index():

    models = registry.get_models()
    for doc in registry.get_documents(models):
        qs = doc().get_queryset()
        log.info('indexing {} "{}" objects'.format(
            qs.count(), doc._doc_type.model.__name__)
        )
        doc().update(qs)
