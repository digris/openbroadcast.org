import django_filters
from abcast.models import Station

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


class StationFilter(django_filters.FilterSet):

    type = CharListFilter(label="Station type")
    country = CharListFilter(label="Country")

    class Meta:
        model = Station
        fields = ['type', 'country', 'city',]

    @property
    def filterlist(self):

        flist = []

        if not hasattr(self, '_filterlist'):

            for name, filter_ in self.filters.iteritems():

                ds = self.queryset.values_list(name, flat=False).annotate(
                    n=models.Count("pk", distinct=True)).distinct()

                filter_.entries = ds

                if ds not in flist:
                    flist.append(filter_)

            self._filterlist = flist

        return self._filterlist

