import logging

from django.contrib.contenttypes.models import ContentType

from alibrary.models.basemodels import *
from alibrary.models.artistmodels import *
log = logging.getLogger(__name__)


def object_by_mb_id(mb_id, type):
    
    log = logging.getLogger('alibrary.util.lookup.object_by_mb_id')
    log.debug('Looking for %s with mb_id: %s' % (type, mb_id))
    
    rel_type = ContentType.objects.get(app_label="alibrary", model=type)
    
    return Relation.objects.filter(content_type=rel_type, url__contains=mb_id)


def media_by_mb_id(mb_id):
    
    rels = object_by_mb_id(mb_id, 'media')
    rel_ids = []
    for rel in rels:
        rel_ids.append(rel.content_object.pk)

    return Media.objects.filter(pk__in=rel_ids)

def release_by_mb_id(mb_id):
    
    rels = object_by_mb_id(mb_id, 'release')
    rel_ids = []
    for rel in rels:
        rel_ids.append(rel.content_object.pk)

    return Release.objects.filter(pk__in=rel_ids)

def artist_by_mb_id(mb_id):
    
    rels = object_by_mb_id(mb_id, 'artist')
    rel_ids = []
    for rel in rels:
        rel_ids.append(rel.content_object.pk)

    return Artist.objects.filter(pk__in=rel_ids)

def label_by_mb_id(mb_id):

    rels = object_by_mb_id(mb_id, 'label')
    rel_ids = []
    for rel in rels:
        rel_ids.append(rel.content_object.pk)

    return Label.objects.filter(pk__in=rel_ids)





def object_by_relation_url(relation_url, type):
    
    log = logging.getLogger('alibrary.util.lookup.object_by_relation_url')
    log.debug('Looking for %s with relation_url: %s' % (type, relation_url))
    
    rel_type = ContentType.objects.get(app_label="alibrary", model=type)
    
    return Relation.objects.filter(content_type=rel_type, url=relation_url)

def artist_by_relation_url(relation_url):

    rels = object_by_relation_url(relation_url, 'artist')
    rel_ids = []
    for rel in rels:
        rel_ids.append(rel.content_object.pk)

    return Artist.objects.filter(pk__in=rel_ids)

