import django_filters
from actstream.models import Action
from django.contrib.contenttypes.models import ContentType

ORDER_BY_FIELD = 'o'

from django.db import models

class CharListFilter(django_filters.Filter):

    def filter(self, qs, value):
        if not value:
            return qs
        if isinstance(value, (list, tuple)):
            lookup = str(value[1])
            if not lookup:
                lookup = 'exact'
            value = value[0]
        else:
            values = value.split(',')
            lookup = self.lookup_type
            
        if value and values:
            if len(values) > 1:
                lookup = 'in'
                return qs.filter(**{'%s__%s' % (self.name, lookup): values})
            else:
                return qs.filter(**{'%s__%s' % (self.name, lookup): value})
        
        return qs


class ActionFilter(django_filters.FilterSet):

    verb = CharListFilter(label="Action")
    target_content_type = CharListFilter(label="Object type")
    class Meta:
        model = Action
        fields = [
            'verb',
            'target_content_type'
        ]
    
    @property
    def filterlist(self):
        flist = []
        if not hasattr(self, '_filterlist'):
            for name, filter_ in self.filters.iteritems():
                qs = self.queryset.values_list(name, flat=False).order_by(name).annotate(n=models.Count("pk", distinct=True)).distinct()
                mapped_qs = []
                if name == 'target_content_type':
                    for item in qs:
                        ct_name = ContentType.objects.get(pk=item[0]).name
                        mapped_qs.append(
                            (ct_name, item[1])
                        )
                    mapped_qs.sort(key=lambda tup: tup[0])
                    qs = mapped_qs


                filter_.entries = qs
                if qs not in flist:
                    flist.append(filter_)

            self._filterlist = flist
        
        return self._filterlist

