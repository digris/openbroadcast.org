import django_filters
from profiles.models import Profile

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
    




class ProfileFilter(django_filters.FilterSet):

    country__printable_name = CharListFilter(label="Country")
    expertise__name = CharListFilter(label="Expertise")
    user__groups = CharListFilter(label="Access level")
    #mentor__username = CharListFilter(label="Mentor")
    class Meta:
        model = Profile
        fields = ['country__printable_name', 'expertise__name', 'user__groups',]
    
    @property
    def filterlist(self):

        flist = []
        
        if not hasattr(self, '_filterlist'):

            for name, filter_ in self.filters.iteritems():
                
                    
                try:
                    ds = self.queryset.values_list(name, '%s__name' % name, flat=False).annotate(n=models.Count("pk", distinct=True)).distinct()
                except:
                    ds = self.queryset.values_list(name, flat=False).annotate(n=models.Count("pk", distinct=True)).distinct()
                
                if name == 'country__printable_name':
                    nd = []
                    for d in ds:
                        nd.append([d[0], d[1]])

                    nd.sort()
                    filter_.entries = nd


                elif name == 'expertise__name':
                    nd = []
                    for d in ds:
                        nd.append([d[0], d[1]])

                    nd.sort()
                    filter_.entries = nd

                else:
                    filter_.entries = ds

                
                if ds not in flist:
          
                    flist.append(filter_)

            self._filterlist = flist
        
        return self._filterlist

