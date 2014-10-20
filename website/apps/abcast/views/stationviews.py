from django.views.generic import DetailView, ListView
from django.conf import settings
from tagging.models import Tag
from django.db.models import Q

from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from abcast.models import Station
from abcast.filters import StationFilter
from lib.util import tagging_extra


PAGINATE_BY = getattr(settings, 'PAGINATE_BY', (12,24,36,120))
PAGINATE_BY_DEFAULT = getattr(settings, 'AGINATE_BY_DEFAULT', 12)


class StationListView(PaginationMixin, ListView):
    
    object = Station
    paginate_by = PAGINATE_BY_DEFAULT
    
    model = Station
    extra_context = {}
    
    def get_paginate_by(self, queryset):
        
        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(StationListView, self).get_context_data(**kwargs)
        
        self.extra_context['filter'] = self.filter
        self.extra_context['relation_filter'] = self.relation_filter
        self.extra_context['tagcloud'] = self.tagcloud
        self.extra_context['list_style'] = self.request.GET.get('list_style', 's')
        self.extra_context['get'] = self.request.GET
        context.update(self.extra_context)

        return context
    

    def get_queryset(self, **kwargs):

        kwargs = {}

        self.tagcloud = None

        q = self.request.GET.get('q', None)
        
        if q:
            qs = Station.objects.filter(Q(name__istartswith=q))\
            .distinct()
        else:
            qs = Station.objects.all()
            
            
        order_by = self.request.GET.get('order_by', None)
        direction = self.request.GET.get('direction', None)
        
        if order_by and direction:
            if direction == 'descending':
                qs = qs.order_by('-%s' % order_by)
            else:
                qs = qs.order_by('%s' % order_by)
            
            
            
        # special relation filters
        self.relation_filter = []

            
            
            

        # base queryset        
        #qs = Release.objects.all()
        
        # apply filters
        self.filter = StationFilter(self.request.GET, queryset=qs)
        # self.filter = ReleaseFilter(self.request.GET, queryset=Release.objects.active().filter(**kwargs))
        
        qs = self.filter.qs
        
        
        
        
        stags = self.request.GET.get('tags', None)
        tstags = []
        if stags:
            stags = stags.split(',')
            for stag in stags:
                tstags.append(int(stag))

            
            
        # rebuild filter after applying tags
        self.filter = StationFilter(self.request.GET, queryset=qs)
        
        # tagging / cloud generation
        tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=0)

        self.tagcloud = tagging_extra.calculate_cloud(tagcloud)
        
        return qs



class StationDetailView(DetailView):

    context_object_name = "station"
    model = Station
    extra_context = {}

    def render_to_response(self, context):
        return super(StationDetailView, self).render_to_response(context, mimetype="text/html")
    

        
    def get_context_data(self, **kwargs):
        
        obj = kwargs.get('object', None)
        context = super(StationDetailView, self).get_context_data(**kwargs)

        members = obj.members.all()
        self.extra_context['members'] = members

        context.update(self.extra_context)

        return context

    