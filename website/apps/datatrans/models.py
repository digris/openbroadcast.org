import datetime
from hashlib import sha1

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import signals
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


def make_digest(key):
    """Get the SHA1 hexdigest of the given key"""
    return sha1(key.encode('utf-8')).hexdigest()


def _get_cache_keys(self):
    """Get all the cache keys for the given object"""
    kv_id_fields = ('language', 'digest', 'content_type_id', 'object_id', 'field')
    values = tuple(getattr(self, attr) for attr in kv_id_fields)
    return ('datatrans_%s_%s_%s_%s_%s' % values,
            'datatrans_%s' % self.id)

# cache for an hour
CACHE_DURATION = getattr(settings, 'DATATRANS_CACHE_DURATION', 60 * 60)


class KeyValueManager(models.Manager):
    def get_query_set(self):
        return KeyValueQuerySet(self.model)

    def get_keyvalue(self, key, language, obj, field):
        key = key or ''
        digest = make_digest(key)
        content_type = ContentType.objects.get_for_model(obj.__class__)
        object_id = obj.id
        keyvalue, created = self.get_or_create(digest=digest,
                                               language=language,
                                               content_type_id=content_type.id,
                                               object_id=obj.id,
                                               field=field,
                                               defaults={'value': key})
        return keyvalue

    def lookup(self, key, language, obj, field):
        kv = self.get_keyvalue(key, language, obj, field)
        if kv.edited:
            return kv.value
        else:
            return key

    def for_model(self, model, fields, modelfield=None):
        """
        Get KeyValues for a model. The fields argument is a list of model
        fields.
        If modelfield is specified, only KeyValue entries for that field will
        be returned.
        """
        field_names = [f.name for f in fields] if modelfield is None else [modelfield]
        ct = ContentType.objects.get_for_model(model)
        return self.filter(field__in=field_names, content_type__id=ct.id)

    def contribute_to_class(self, model, name):
        signals.post_save.connect(self._post_save, sender=model)
        signals.post_delete.connect(self._post_delete, sender=model)
        setattr(model, '_get_cache_keys', _get_cache_keys)
        setattr(model, 'cache_keys', property(_get_cache_keys))
        return super(KeyValueManager, self).contribute_to_class(model, name)

    def _invalidate_cache(self, instance):
        """
        Explicitly set a None value instead of just deleting so we don't have
        any race conditions where.
        """
        for key in instance.cache_keys:
            cache.set(key, None, 5)

    def _post_save(self, instance, **kwargs):
        """
        Refresh the cache when saving
        """
        for key in instance.cache_keys:
            cache.set(key, instance, CACHE_DURATION)

    def _post_delete(self, instance, **kwargs):
        self._invalidate_cache(instance)


class KeyValueQuerySet(QuerySet):
    def iterator(self):
        superiter = super(KeyValueQuerySet, self).iterator()
        while True:
            obj = superiter.next()
            # Use cache.add instead of cache.set to prevent race conditions
            for key in obj.cache_keys:
                cache.add(key, obj, CACHE_DURATION)
            yield obj

    def get(self, *args, **kwargs):
        """
        Checks the cache to see if there's a cached entry for this pk. If not,
        fetches using super then stores the result in cache.

        Most of the logic here was gathered from a careful reading of
        ``django.db.models.sql.query.add_filter``
        """
        if self.query.where:
            # If there is any other ``where`` filter on this QuerySet just call
            # super. There will be a where clause if this QuerySet has already
            # been filtered/cloned.
            return super(KeyValueQuerySet, self).get(*args, **kwargs)

        kv_id_fields = ('language', 'digest', 'content_type', 'object_id', 'field')

        # Punt on anything more complicated than get by pk/id only...
        if len(kwargs) == 1:
            k = kwargs.keys()[0]
            if k in ('pk', 'pk__exact', 'id', 'id__exact'):
                obj = cache.get('datatrans_%s' % kwargs.values()[0])
                if obj is not None:
                    return obj
        elif set(kv_id_fields) <= set(kwargs.keys()):
            values = tuple(kwargs[attr] for attr in kv_id_fields)
            obj = cache.get('datatrans_%s_%s_%s_%s_%s' % values)

            if obj is not None:
                return obj

        # Calls self.iterator to fetch objects, storing object in cache.
        return super(KeyValueQuerySet, self).get(*args, **kwargs)


class KeyValue(models.Model):
    """
    The datatrans magic is stored in this model. It stores the localized fields of models.
    """
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True, default=None)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=255)
    language = models.CharField(max_length=5, db_index=True, choices=settings.LANGUAGES)

    value = models.TextField(blank=True)
    edited = models.BooleanField(blank=True, default=False)
    fuzzy = models.BooleanField(blank=True, default=False)

    digest = models.CharField(max_length=40, db_index=True)
    updated = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    objects = KeyValueManager()

    def __unicode__(self):
        return u'%s: %s' % (self.language, self.value)

    class Meta:
        #unique_together = ('digest', 'language')
        unique_together = ('language', 'content_type', 'field', 'object_id', 'digest')


class WordCount(models.Model):
    """
    It all happens here
    """
    class Meta:
        abstract = True

    total_words = models.IntegerField(default=0)
    valid = models.BooleanField()


class ModelWordCount(WordCount):
    """
    Caches the total number of localized words for a model
    """
    content_type = models.ForeignKey(ContentType, db_index=True, unique=True)


class FieldWordCount(WordCount):
    """
    Caches the total number of localized words for a model field.
    """
    class Meta:
        unique_together = ('content_type', 'field')

    content_type = models.ForeignKey(ContentType, db_index=True)
    field = models.CharField(max_length=64, db_index=True)


