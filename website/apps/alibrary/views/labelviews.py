# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import actstream
import logging

from django.views.generic import DetailView, ListView, UpdateView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q, Case, When
from django.utils.translation import ugettext as _
from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from elasticsearch_dsl import FacetedSearch, TermsFacet
from elasticsearch_dsl import Q as ESQ

from tagging_extra.utils import calculate_cloud
from base.utils.form_errors import merge_form_errors
from search.queries import format_search_results
from search.utils import parse_search_query, parse_pagination_query, get_pagination_data, get_tagcloud_data, get_filter_data

from alibrary.models import Label, Release
from alibrary.forms import LabelForm, LabelActionForm, LabelRelationFormSet
from alibrary.filters import LabelFilter
from alibrary.documents import LabelDocument



ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12,24,36,120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)


PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)


log = logging.getLogger(__name__)

ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'updated',
        'name': _('Last modified')
    },
    {
        'key': 'created',
        'name': _('Creation date')
    },
]


class LabelSearch(FacetedSearch):
    doc_types = [LabelDocument]
    fields = ['tags', 'name', ]

    facets = {
        'tags': TermsFacet(field='tags', size=100),
        'country': TermsFacet(field='country', size=500),
        'type': TermsFacet(field='type'),

        #'duplicates': TermsFacet(field='exact_name', size=100, min_doc_count=2),
    }

    def query(self, search, query):

        s = search

        _searches = query.get('searches', None)
        _options = query.get('options', None)

        if not _searches:
            return s

        # elasticsearch 'must' queries
        _musts = []

        for key, value in _searches.iteritems():
            # not particularly nice
            # 'q' - the main search query
            if key == 'q':

                if _options.get('fuzzy', True):
                    _q = ESQ('match', autocomplete={'query': ' '.join(value), 'operator': 'and', 'fuzziness': 'AUTO'})
                    print('FUZZY')
                else:
                    _q = ESQ('match', autocomplete={'query': ' '.join(value), 'operator': 'and'})
                    print('EXACT')

                _musts.append(
                    _q,
                )

            # 'tags' - for 'intersection-style' tagcloud
            if key == 'tags':
                print(value)
                for tag in value:
                    _musts.append(
                        ESQ('term', tags=tag)
                    )

        if _musts:
            s.query = ESQ('bool', must=_musts)

        return s



class LabelListView(ListView):

    model = Label
    template_name = 'alibrary/label_list_ng.html'
    search_class = LabelSearch
    _search_result = None

    def get_queryset(self, **kwargs):

        search_query = parse_search_query(request=self.request)

        # initialize search class
        s = self.search_class(
            query=search_query,
            filters=search_query['filters'],
            sort=search_query['order_by']
        )


        # handle pagination
        pagination_query = parse_pagination_query(request=self.request)
        s = s[pagination_query['start']:pagination_query['end']]


        # execute elasticsearch query
        result = s.execute()
        formatted_result = format_search_results(result)


        # get object pks and create corresponding queryset
        pks = [r['id'] for r in formatted_result['results'] if r['ct']]
        qs = self.model.objects.filter(pk__in=pks)
        qs = qs.order_by(Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)]))


        # add search result as reference
        self._search_result = result

        qs = qs.select_related('country').prefetch_related('release_label', 'creator', 'creator__profile')

        return qs


    def get_context_data(self, **kwargs):
        context = super(LabelListView, self).get_context_data(**kwargs)

        search_result = self._search_result
        pagination_query = parse_pagination_query(request=self.request)
        pagination = get_pagination_data(search_result, pagination_query)
        tagcloud = get_tagcloud_data(search_result.facets.tags)

        context.update({
            'facets': search_result.facets,
            'num_results': search_result.hits.total,
            'pagination': pagination,
            'tagcloud': tagcloud,
            #'filters': get_filter_data([f for f in search_result.facets if not f == 'tags']),
            'filters': get_filter_data(search_result.facets),
        })

        return context


class LabelDetailView(DetailView):

    context_object_name = "label"
    model = Label
    extra_context = {}


    def get_context_data(self, **kwargs):

        context = super(LabelDetailView, self).get_context_data(**kwargs)
        obj = kwargs.get('object', None)

        releases = Release.objects.filter(label=obj).order_by('-releasedate').distinct()[:8]
        self.extra_context['releases'] = releases
        self.extra_context['history'] = []

        context.update(self.extra_context)

        return context








class LabelEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Label
    form_class = LabelForm
    template_name = "alibrary/label_edit.html"
    permission_required = 'alibrary.change_label'
    raise_exception = True
    success_url = '#'

    def __init__(self, *args, **kwargs):
        super(LabelEditView, self).__init__(*args, **kwargs)


    def get_initial(self):
        self.initial.update({
            'user': self.request.user,
            'd_tags': ','.join(t.name for t in self.object.tags)
        })
        return self.initial

    def get_context_data(self, **kwargs):

        # TODO: this is the wrong place for this!
        if self.object.disable_editing:
            raise Exception('Editing is locked on that object!')


        ctx = super(LabelEditView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        # TODO: is this a good way to pass the instance main form?
        ctx['form_errors'] = self.get_form_errors(form=ctx['form'])

        return ctx

    def get_named_formsets(self):

        return {
            'action': LabelActionForm(self.request.POST or None, prefix='action'),
            'relation': LabelRelationFormSet(self.request.POST or None, instance=self.object, prefix='relation'),
        }

    def get_form_errors(self, form=None):

        named_formsets = self.get_named_formsets()
        named_formsets.update({'form': form})
        form_errors = merge_form_errors([formset for name, formset in named_formsets.items()])

        return form_errors

    def form_valid(self, form):

        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save(commit=False)

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        d_tags = form.cleaned_data['d_tags']
        if d_tags:
            self.object.tags = d_tags

        self.object.last_editor = self.request.user
        actstream.action.send(self.request.user, verb=_('updated'), target=self.object)

        self.object = form.save()
        messages.add_message(self.request, messages.INFO, 'Object updated')

        return HttpResponseRedirect(self.object.get_edit_url())
        # return HttpResponseRedirect('')


# autocompleter views
# TODO: remove
# def label_autocomplete(request):
#
#     q = request.GET.get('q', None)
#
#     result = []
#
#     if q and len(q) > 1:
#
#         releases = Release.objects.filter(Q(name__istartswith=q)\
#             | Q(media_release__name__icontains=q)\
#             | Q(media_release__label__name__icontains=q)\
#             | Q(label__name__icontains=q))\
#             .distinct()
#         for release in releases:
#             item = {}
#             item['release'] = release
#             medias = []
#             labels = []
#             labels = []
#             for media in release.media_release.filter(name__icontains=q).distinct():
#                 if not media in medias:
#                     medias.append(media)
#             for media in release.media_release.filter(label__name__icontains=q).distinct():
#                 if not media.label in labels:
#                     labels.append(media.label)
#
#             if not len(labels) > 0:
#                 labels = None
#             if not len(medias) > 0:
#                 medias = None
#             if not len(labels) > 0:
#                 labels = None
#
#             item['labels'] = labels
#             item['medias'] = medias
#             item['labels'] = labels
#
#             result.append(item)
#
#
#     #return HttpResponse(json.dumps(list(result)))
#     return render_to_response("alibrary/element/autocomplete.html", { 'query': q, 'result': result }, context_instance=RequestContext(request))








# class LabelListView(PaginationMixin, ListView):
#
#     # context_object_name = "label_list"
#     #template_name = "alibrary/release_list.html"
#
#     object = Label
#     paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
#
#     model = Release
#     extra_context = {}
#
#     def get_paginate_by(self, queryset):
#
#         ipp = self.request.GET.get('ipp', None)
#         if ipp:
#             try:
#                 if int(ipp) in ALIBRARY_PAGINATE_BY:
#                     return int(ipp)
#             except Exception as e:
#                 pass
#
#         return self.paginate_by
#
#     def get_context_data(self, **kwargs):
#         context = super(LabelListView, self).get_context_data(**kwargs)
#
#         self.extra_context['filter'] = self.filter
#         self.extra_context['relation_filter'] = self.relation_filter
#         self.extra_context['tagcloud'] = self.tagcloud
#         # for the ordering-box
#         self.extra_context['order_by'] = ORDER_BY
#
#         # active tags
#         if self.request.GET.get('tags', None):
#             tag_ids = []
#             for tag_id in self.request.GET['tags'].split(','):
#                 tag_ids.append(int(tag_id))
#             self.extra_context['active_tags'] = tag_ids
#         #self.extra_context['release_list'] = self.filter
#
#         # hard-coded for the moment
#
#         self.extra_context['list_style'] = self.request.GET.get('list_style', 'l')
#         #self.extra_context['list_style'] = 's'
#
#         self.extra_context['get'] = self.request.GET
#
#         context.update(self.extra_context)
#
#         return context
#
#
#     def get_queryset(self, **kwargs):
#
#         # return render_to_response('my_app/template.html', {'filter': f})
#
#         kwargs = {}
#
#         self.tagcloud = None
#
#         q = self.request.GET.get('q', None)
#
#         if q:
#             # haystack version
#             #sqs = SearchQuerySet().models(Label).filter(SQ(content__contains=q) | SQ(content_auto=q))
#             #sqs = SearchQuerySet().models(Label).filter(content=AutoQuery(q))
#             sqs = SearchQuerySet().models(Label).filter(text_auto=AutoQuery(q))
#             qs = Label.objects.filter(id__in=[result.object.pk for result in sqs]).distinct()
#
#             # ORM
#             # qs = qs.filter(name__icontains=q).distinct()
#
#         else:
#             qs = Label.objects.all()
#
#
#
#
#         order_by = self.request.GET.get('order_by', 'created')
#         direction = self.request.GET.get('direction', 'descending')
#
#         if order_by and direction:
#             if direction == 'descending':
#                 qs = qs.order_by('-%s' % order_by)
#             else:
#                 qs = qs.order_by('%s' % order_by)
#
#
#
#         # special relation filters
#         self.relation_filter = []
#
#         label_filter = self.request.GET.get('label', None)
#         if label_filter:
#             qs = qs.filter(media_release__label__slug=label_filter).distinct()
#             # add relation filter
#             fa = Label.objects.filter(slug=label_filter)[0]
#             f = {'item_type': 'label' , 'item': fa, 'label': _('Label')}
#             self.relation_filter.append(f)
#
#         label_filter = self.request.GET.get('label', None)
#         if label_filter:
#             qs = qs.filter(label__slug=label_filter).distinct()
#             # add relation filter
#             fa = Label.objects.filter(slug=label_filter)[0]
#             f = {'item_type': 'label' , 'item': fa, 'label': _('Label')}
#             self.relation_filter.append(f)
#
#
#
#         # filter by import session
#         import_session = self.request.GET.get('import', None)
#         if import_session:
#             from importer.models import Import
#             from django.contrib.contenttypes.models import ContentType
#             import_session = get_object_or_404(Import, pk=int(import_session))
#             ctype = ContentType.objects.get(model='label')
#             ids = import_session.importitem_set.filter(content_type=ctype.pk).values_list('object_id',)
#             qs = qs.filter(pk__in=ids).distinct()
#
#
#         # "extra-filters" (to provide some arbitary searches)
#         extra_filter = self.request.GET.get('extra_filter', None)
#         if extra_filter:
#             if extra_filter == 'possible_duplicates':
#                 from django.db.models import Count
#                 dupes = Label.objects.values('name').annotate(Count('id')).order_by().filter(id__count__gt=1)
#                 qs = qs.filter(name__in=[item['name'] for item in dupes])
#                 if not order_by:
#                     qs = qs.order_by('name')
#
#
#         # apply filters
#         self.filter = LabelFilter(self.request.GET, queryset=qs)
#
#         qs = self.filter.qs
#
#
#
#
#         stags = self.request.GET.get('tags', None)
#         #print "** STAGS:"
#         #print stags
#         tstags = []
#         if stags:
#             stags = stags.split(',')
#             for stag in stags:
#                 #print int(stag)
#                 tstags.append(int(stag))
#
#         #print "** TSTAGS:"
#         #print tstags
#
#         #stags = ('Techno', 'Electronic')
#         #stags = (4,)
#         if stags:
#             qs = Label.tagged.with_all(tstags, qs)
#
#
#         # rebuild filter after applying tags
#         self.filter = LabelFilter(self.request.GET, queryset=qs)
#
#         # tagging / cloud generation
#         if qs.exists():
#             tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=2)
#             self.tagcloud = calculate_cloud(tagcloud)
#
#
#         return qs


