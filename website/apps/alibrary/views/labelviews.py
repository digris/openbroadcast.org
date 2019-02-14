# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import actstream
import logging

from django.views.generic import View, DetailView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, FileResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.utils import timezone
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from elasticsearch_dsl import TermsFacet, RangeFacet

from base.utils.form_errors import merge_form_errors
from search.views import BaseFacetedSearch, BaseSearchListView
from search.duplicate_detection import get_ids_for_possible_duplicates

from ..forms import LabelForm, LabelActionForm, LabelRelationFormSet
from ..models import Label, Release
from ..documents import LabelDocument

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

log = logging.getLogger(__name__)


class LabelSearch(BaseFacetedSearch):
    doc_types = [LabelDocument]
    fields = ['tags', 'name', ]

    facets = [
        ('tags', TermsFacet(field='tags', size=100)),
        ('country', TermsFacet(field='country', size=500, order={'_key': 'asc'})),
        ('type', TermsFacet(field='type', size=20, order={'_key': 'asc'})),
        ('established', RangeFacet(field='year_start', ranges=[
            ('Before 1940\'s', (0, 1940)),
            ('40\'s', (1940, 1950)),
            ('50\'s', (1950, 1960)),
            ('60\'s', (1960, 1970)),
            ('70\'s', (1970, 1980)),
            ('80\'s', (1980, 1990)),
            ('90\'s', (1990, 2000)),
            ('2000\'s', (2000, 2010)),
            ('2010\'s', (2010, 2020)),
            ('This Year', (2018, 2019)),
        ])),
    ]

class LabelListView(BaseSearchListView):
    model = Label
    template_name = 'alibrary/label_list.html'
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

        limit_ids = None

        # TODO: special purpose filters. should be moved to generic place & add parameter validation
        duplicate_filter = self.request.GET.get('duplicate_filter', None)
        if duplicate_filter:
            fields = duplicate_filter.split(':')
            limit_ids = get_ids_for_possible_duplicates('labels', fields)

        qs = super(LabelListView, self).get_queryset(limit_ids=limit_ids, **kwargs)

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

        self.extra_context['download_statistics_for_years'] = range(timezone.now().year, obj.created.year - 1, -1)

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



class LabelStatisticsDownloadView(View):

    def get(self, request, **kwargs):

        from statistics.label_statistics import summary_for_label_as_xls

        obj = get_object_or_404(Label, pk=kwargs.get('pk'))

        filename = 'Airplay statistics - {label}.xlsx'.format(
            label=obj.name
        )

        output = StringIO.StringIO()

        summary_for_label_as_xls(
            label=obj,
            event_type_id=3,
            output=output
        )

        output.seek(0)

        response = FileResponse(output.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


        response = HttpResponse(output.read(), content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        return response
