# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import actstream
import logging

from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from elasticsearch_dsl import TermsFacet

from base.utils.form_errors import merge_form_errors
from search.views import BaseFacetedSearch, BaseSearchListView

from ..forms import LabelForm, LabelActionForm, LabelRelationFormSet
from ..models import Label, Release
from ..documents import LabelDocument

log = logging.getLogger(__name__)


class LabelSearch(BaseFacetedSearch):
    doc_types = [LabelDocument]
    fields = ['tags', 'name', ]

    facets = {
        'tags': TermsFacet(field='tags', size=100),
        'country': TermsFacet(field='country', size=500, order={'_key': 'asc'}),
        'type': TermsFacet(field='type', order={'_key': 'asc'}),
        # 'duplicates': TermsFacet(field='exact_name', size=100, min_doc_count=2),
    }


class LabelListView(BaseSearchListView):
    model = Label
    template_name = 'alibrary/label_list_ng.html'
    search_class = LabelSearch
    order_by = [
        {
            'key': 'created',
            'name': _('Creation date'),
            'default_direction': 'desc',
        },
        {
            'key': 'updated',
            'name': _('Modification date'),
            'default_direction': 'asc',
        },
        {
            'key': 'name',
            'name': _('Name'),
            'default_direction': 'asc',
        },
    ]

    def get_queryset(self, **kwargs):
        qs = super(LabelListView, self).get_queryset(**kwargs)

        qs = qs.select_related(
            'country'
        ).prefetch_related(
            'release_label',
            'creator',
            'creator__profile'
        )

        return qs


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
