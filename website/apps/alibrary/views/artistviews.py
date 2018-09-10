# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import actstream
import logging

from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db.models import Q
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from elasticsearch_dsl import TermsFacet

from base.utils.form_errors import merge_form_errors
from search.views import BaseFacetedSearch, BaseSearchListView

from ..models import Artist, Release, Media, NameVariation
from ..forms import ArtistForm, ArtistActionForm, ArtistRelationFormSet, MemberFormSet, AliasFormSet
from ..documents import ArtistDocument

log = logging.getLogger(__name__)


class ArtistSearch(BaseFacetedSearch):
    doc_types = [ArtistDocument]
    fields = ['tags', 'name', ]

    facets = {
        'tags': TermsFacet(field='tags', size=100),
        'country': TermsFacet(field='country', size=500, order={'_key': 'asc'}),
        'type': TermsFacet(field='type', order={'_key': 'asc'}),
    }


class ArtistListView(BaseSearchListView):
    model = Artist
    template_name = 'alibrary/artist_list_ng.html'
    search_class = ArtistSearch
    order_by = [
        {
            'key': 'name',
            'name': _('Name'),
            'default_direction': 'asc',
        },
        {
            'key': 'year_start',
            'name': _('Date of formation / date of birth'),
            'default_direction': 'desc',
        },
        {
            'key': 'year_end',
            'name': _('Date of breakup / date of death'),
            'default_direction': 'desc',
        },
        {
            'key': 'updated',
            'name': _('Last modified'),
            'default_direction': 'desc',
        },
        {
            'key': 'created',
            'name': _('Creation date'),
            'default_direction': 'desc',
        },
    ]

    def get_queryset(self, **kwargs):
        qs = super(ArtistListView, self).get_queryset(**kwargs)

        qs = qs.select_related(
            'country'
        ).prefetch_related(
            'creator',
            'creator__profile'
        )

        return qs


class ArtistDetailView(DetailView):
    context_object_name = "artist"
    model = Artist
    extra_context = {}

    def render_to_response(self, context):
        return super(ArtistDetailView, self).render_to_response(context, content_type="text/html")

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        obj = self.object

        extra_context = {}

        extra_context['releases'] = Release.objects.filter(Q(media_release__artist=obj) \
                                                           | Q(album_artists=obj)) \
                                        .distinct()[0:8]

        """
        top-flop
        """
        m_top = []
        media_top = Media.objects.filter(artist=obj, votes__vote__gt=0).order_by('-votes__vote').distinct()
        if media_top.exists():
            media_top = media_top[0:10]
            for media in media_top:
                m_top.append(media)

        m_flop = []
        media_flop = Media.objects.filter(artist=obj, votes__vote__lt=0).order_by('votes__vote').distinct()
        if media_flop.exists():
            media_flop = media_flop[0:10]
            for media in media_flop:
                m_flop.append(media)

        extra_context['m_top'] = m_top
        extra_context['m_flop'] = m_flop

        extra_context['m_contrib'] = Media.objects.filter(extra_artists=obj)[0:48]
        extra_context['history'] = []
        extra_context['appearances'] = {
            'media': obj.get_media(),
            'releases': obj.get_releases(),
        }

        context.update(extra_context)

        return context


class ArtistEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = "alibrary/artist_edit.html"
    permission_required = 'alibrary.change_artist'
    raise_exception = True
    success_url = '#'

    def __init__(self, *args, **kwargs):
        super(ArtistEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update({
            'user': self.request.user,
            'd_tags': ','.join(t.name for t in self.object.tags)}
        )
        return self.initial

    def get_context_data(self, **kwargs):
        context = super(ArtistEditView, self).get_context_data(**kwargs)
        obj = self.object

        extra_context = {}

        extra_context['named_formsets'] = self.get_named_formsets()
        extra_context['form_errors'] = self.get_form_errors(form=context['form'])
        extra_context['appearances'] = {
            'media': obj.get_media(),
            'releases': obj.get_releases(),
        }
        context.update(extra_context)

        return context

    def get_named_formsets(self):

        return {
            'action': ArtistActionForm(self.request.POST or None, prefix='action'),
            'relation': ArtistRelationFormSet(self.request.POST or None, instance=self.object, prefix='relation'),
            'member': MemberFormSet(self.request.POST or None, instance=self.object, prefix='member'),
            'alias': AliasFormSet(self.request.POST or None, instance=self.object, prefix='alias'),
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

        # TODO: implement in a better way
        namevariations_text = form.cleaned_data['namevariations']
        if namevariations_text:
            self.object.namevariations.all().delete()
            variations = namevariations_text.split(',')
            for v in variations:
                nv = NameVariation(name=v.strip(), artist=self.object)
                nv.save()
        else:
            self.object.namevariations.all().delete()

        d_tags = form.cleaned_data['d_tags']
        if d_tags:
            self.object.tags = d_tags

        self.object.last_editor = self.request.user
        actstream.action.send(self.request.user, verb=_('updated'), target=self.object)

        self.object = form.save()
        messages.add_message(self.request, messages.INFO, 'Object updated')

        return HttpResponseRedirect(self.object.get_edit_url())
        # return HttpResponseRedirect('')

    # TODO: investigate if this can be removed
    # def formset_relation_valid(self, formset):
    #     relations = formset.save(commit=False)
    #     for relation in relations:
    #         relation.save()

# TODO: check if still needed. should actually already be handled via api!
# def artist_autocomplete(request):
#
#     q = request.GET.get('q', None)
#
#     result = []
#
#     if q and len(q) > 1:
#
#         releases = Release.objects.filter(Q(name__istartswith=q)\
#             | Q(media_release__name__icontains=q)\
#             | Q(media_release__artist__name__icontains=q)\
#             | Q(label__name__icontains=q))\
#             .distinct()
#         for release in releases:
#             item = {}
#             item['release'] = release
#             medias = []
#             artists = []
#             labels = []
#             for media in release.media_release.filter(name__icontains=q).distinct():
#                 if not media in medias:
#                     medias.append(media)
#             for media in release.media_release.filter(artist__name__icontains=q).distinct():
#                 if not media.artist in artists:
#                     artists.append(media.artist)
#
#             if not len(artists) > 0:
#                 artists = None
#             if not len(medias) > 0:
#                 medias = None
#             if not len(labels) > 0:
#                 labels = None
#
#             item['artists'] = artists
#             item['medias'] = medias
#             item['labels'] = labels
#
#             result.append(item)
#
#     return render_to_response("alibrary/element/autocomplete.html", { 'query': q, 'result': result }, context_instance=RequestContext(request))


# class ArtistListView(PaginationMixin, ListView):
#
#     object = Artist
#     paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
#
#     model = Release
#
#     # context_object_name = "artist_list"
#     #template_name = "alibrary/release_list.html"
#     #page_template = 'alibrary/artist_list_page.html'
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
#
#
#     def get_context_data(self, **kwargs):
#
#         context = super(ArtistListView, self).get_context_data(**kwargs)
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
#
#         self.extra_context['list_style'] = self.request.GET.get('list_style', 'l')
#
#         self.extra_context['get'] = self.request.GET
#         context.update(self.extra_context)
#
#         return context
#
#
#     def get_queryset(self, **kwargs):
#
#         kwargs = {}
#         self.tagcloud = None
#         q = self.request.GET.get('q', None)
#
#         # haystack version
#         if q:
#             #sqs = SearchQuerySet().models(Artist).filter(SQ(content__contains=q) | SQ(content_auto=q))
#             #sqs = SearchQuerySet().models(Artist).filter(content=AutoQuery(q))
#             sqs = SearchQuerySet().models(Artist).filter(text_auto=AutoQuery(q))
#
#             qs = Artist.objects.filter(id__in=[result.object.pk for result in sqs]).distinct()
#         else:
#             qs = Artist.objects.all().prefetch_related('media_artist')
#
#         # if q:
#         #     # qs = Artist.objects.filter(Q(name__istartswith=q) | Q(namevariations__name__istartswith=q)).distinct()
#         #     # https://lab.hazelfire.com/issues/1477
#         #     qs = Artist.objects.filter(Q(name__icontains=q) | Q(namevariations__name__icontains=q)).distinct()
#         #     qs = qs.prefetch_related('media_artist')
#         # else:
#         #     # only display artists with tracks a.t.m.
#         #     qs = Artist.objects.all().prefetch_related('media_artist')
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
#         artist_filter = self.request.GET.get('artist', None)
#         if artist_filter:
#             qs = qs.filter(media_release__artist__slug=artist_filter).distinct()
#             fa = Artist.objects.filter(slug=artist_filter)[0]
#             f = {'item_type': 'artist' , 'item': fa, 'label': _('Artist')}
#             self.relation_filter.append(f)
#
#         label_filter = self.request.GET.get('label', None)
#         if label_filter:
#             qs = qs.filter(label__slug=label_filter).distinct()
#             fa = Label.objects.filter(slug=label_filter)[0]
#             f = {'item_type': 'label' , 'item': fa, 'label': _('Label')}
#             self.relation_filter.append(f)
#
#         date_start_filter = self.request.GET.get('date_start', None)
#         if date_start_filter:
#
#             qs = qs.filter(date_start__lte='%s-12-31' % date_start_filter, date_start__gte='%s-00-00' % date_start_filter).distinct()
#             f = {'item_type': 'label' , 'item': '%s-12-31' % date_start_filter, 'label': _('Date start')}
#             self.relation_filter.append(f)
#
#         # "extra-filters" (to provide some arbitrary searches)
#         extra_filter = self.request.GET.get('extra_filter', None)
#         if extra_filter:
#             if extra_filter == 'possible_duplicates':
#                 from django.db.models import Count
#                 duplicates = Artist.objects.values('name').annotate(Count('id')).order_by().filter(id__count__gt=1)
#                 qs = qs.filter(name__in=[item['name'] for item in duplicates])
#                 if not order_by:
#                     qs = qs.order_by('name')
#
#             if extra_filter == 'mbid_duplicates':
#                 from django.db.models import Count
#                 from django.contrib.contenttypes.models import ContentType
#                 from ..models.basemodels import Relation
#                 _ct = ContentType.objects.get_for_model(Artist)
#                 _relation_qs = Relation.objects.filter(content_type=_ct, service__in=['musicbrainz',])
#                 duplicates = _relation_qs.values('url').annotate(Count('id')).order_by().filter(id__count__gt=1)
#                 qs = qs.filter(relations__url__in=[item['url'] for item in duplicates]).distinct()
#                 if not order_by:
#                     qs = qs.order_by('name')
#
#             if extra_filter == 'type_unknown':
#                 qs = qs.filter(Q(type='') | Q(type__isnull=True)).distinct()
#
#         # filter by import session
#         import_session = self.request.GET.get('import', None)
#         if import_session:
#             from importer.models import Import
#             from django.contrib.contenttypes.models import ContentType
#             import_session = get_object_or_404(Import, pk=int(import_session))
#             ctype = ContentType.objects.get(model='artist')
#             ids = import_session.importitem_set.filter(content_type=ctype.pk).values_list('object_id',)
#             qs = qs.filter(pk__in=ids).distinct()
#
#         # apply filters
#         self.filter = ArtistFilter(self.request.GET, queryset=qs)
#         # self.filter = ReleaseFilter(self.request.GET, queryset=Release.objects.active().filter(**kwargs))
#
#         qs = self.filter.qs
#
#         stags = self.request.GET.get('tags', None)
#         tstags = []
#         if stags:
#             stags = stags.split(',')
#             for stag in stags:
#                 #print int(stag)
#                 tstags.append(int(stag))
#
#         if stags:
#             qs = Release.tagged.with_all(tstags, qs)
#
#         # rebuild filter after applying tags
#         self.filter = ArtistFilter(self.request.GET, queryset=qs)
#
#         # tagging / cloud generation
#         if qs.exists():
#             try:
#                 tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=10)
#                 self.tagcloud = calculate_cloud(tagcloud)
#             except TypeError:
#                 pass
#
#         return qs
