from django.db import models
from django.utils.functional import memoize
from django.contrib.contenttypes.models import ContentType

_get_content_type_for_model_cache = {}

def get_content_type_for_model(model):
    return ContentType.objects.get_for_model(model)

get_content_type_for_model = memoize(get_content_type_for_model, 
    _get_content_type_for_model_cache, 1)


class QuerysetWithContents(object):
    """
    Queryset wrapper.
    """
    def __init__(self, queryset):
        self.queryset = queryset
        
    def __getattr__(self, name):
        if name in ('get', 'create', 'get_or_create', 'count', 'in_bulk',
            'iterator', 'latest', 'aggregate', 'exists', 'update', 'delete'):
            return getattr(self.queryset, name)
        if hasattr(self.queryset, name):
            attr = getattr(self.queryset, name)
            if callable(attr):
                def _wrap(*args, **kwargs):
                    return self.__class__(attr(*args, **kwargs))
                return _wrap
            return attr
        raise AttributeError(name)
            
    def __getitem__(self, key):
        return self.__class__(self.queryset[key])
        
    def __iter__(self):
        objects = list(self.queryset)
        generics = {}
        for i in objects:
            generics.setdefault(i.content_type_id, set()).add(i.object_id)
        content_types = ContentType.objects.in_bulk(generics.keys())
        relations = {}
        for content_type_id, pk_list in generics.items():
            model = content_types[content_type_id].model_class()
            relations[content_type_id] = model.objects.in_bulk(pk_list)
        for i in objects:
            setattr(i, '_content_object_cache', 
                relations[i.content_type_id][i.object_id])
        return iter(objects)
        
    def __len__(self):
        return len(self.queryset)
                

class RatingsManager(models.Manager):
    """
    Manager used by *Score* and *Vote* models.
    """
    def get_for(self, content_object, key, **kwargs):
        """
        Return the instance related to *content_object* and matching *kwargs*. 
        Return None if a vote is not found.
        """
        content_type = get_content_type_for_model(type(content_object))
        try:
            return self.get(key=key, content_type=content_type, 
                object_id=content_object.pk, **kwargs)
        except self.model.DoesNotExist:
            return None
            
    def filter_for(self, content_object_or_model, **kwargs):
        """
        Return all the instances related to *content_object_or_model* and 
        matching *kwargs*. The argument *content_object_or_model* can be
        both a model instance or a model class.
        """
        if isinstance(content_object_or_model, models.base.ModelBase):
            lookups = {'content_type': get_content_type_for_model(
                content_object_or_model)}
        else:
            lookups = {
                'content_type': get_content_type_for_model(
                    type(content_object_or_model)),
                'object_id': content_object_or_model.pk,
            }
        lookups.update(kwargs)
        return self.filter(**lookups)
            
    def filter_with_contents(self, **kwargs):
        """
        Return all instances retreiving content objects in bulk in order
        to minimize db queries, e.g. to get all objects voted by a user::
        
            for vote in Vote.objects.filter_with_contents(user=myuser):
                vote.content_object # this does not hit the db
        """
        if 'content_object' in kwargs:
            content_object = kwargs.pop('content_object')
            queryset = self.filter_for(content_object, **kwargs)
        else:
            queryset = self.filter(**kwargs)
        return QuerysetWithContents(queryset)
