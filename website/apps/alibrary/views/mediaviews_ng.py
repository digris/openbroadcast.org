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

from elasticsearch_dsl import FacetedSearch, TermsFacet, RangeFacet
from elasticsearch_dsl import Q as ESQ

from tagging_extra.utils import calculate_cloud
from base.utils.form_errors import merge_form_errors
from search.queries import format_search_results
from search.utils import parse_search_query, parse_pagination_query, get_pagination_data, get_tagcloud_data, get_filter_data

from alibrary.models import Media, Release
from alibrary.forms import MediaForm, MediaActionForm, MediaRelationFormSet
from alibrary.filters import MediaFilter
from alibrary.documents import MediaDocument



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


class MediaSearch(FacetedSearch):
    doc_types = [MediaDocument]
    fields = ['tags', 'name', ]

    facets = {
        'tags': TermsFacet(field='tags', size=100),
        'type': TermsFacet(field='type', size=100),
        'version': TermsFacet(field='version', size=100),
        'bitrate': RangeFacet(field='bitrate', ranges=[
            ('Low', (0, 100)),
            ('Medium', (100, 200)),
            ('High', (200, None))
        ]),
        'samplerate': RangeFacet(field='samplerate', ranges=[
            ('Low', (0, 44100)),
            ('Medium', (44100, 48000)),
            ('High', (48000, None))
        ]),
        'encoding': TermsFacet(field='encoding', size=100),
        'license': TermsFacet(field='license'),
        'lyrics_language': TermsFacet(field='lyrics_language'),

        # 'releasedate': RangeFacet(field='bitrate', ranges=[
        #     ('Low', (0, 100)),
        #     ('Medium', (100, 200)),
        #     ('High', (200, None))
        # ]),

        # 'duplicates': TermsFacet(field='name', size=100, min_doc_count=2),
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
            # not particularly nice - maybe there is a better way to build queries here
            # 'q' - the main search query
            if key == 'q':
                if _options.get('fuzzy', True):
                    _q = ESQ('match', autocomplete={'query': ' '.join(value), 'operator': 'and', 'fuzziness': 'AUTO'})
                else:
                    _q = ESQ('match', autocomplete={'query': ' '.join(value), 'operator': 'and'})
                _musts.append(
                    _q,
                )

            # 'tags' - for 'intersection-style' tagcloud
            elif key == 'tags':
                for tag in value:
                    _musts.append(
                        ESQ('term', tags=tag)
                    )
            else:
                for v in value:
                    _musts.append(
                        ESQ('term', **{key: v})
                    )
                #s = s.highlight(key)

        if _musts:
            s.query = ESQ('bool', must=_musts)

        return s



class MediaListView(ListView):

    model = Media
    template_name = 'alibrary/media_list_ng.html'
    search_class = MediaSearch
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

        qs = qs.select_related('release', 'artist', 'license').prefetch_related('media_artists', 'extra_artists')

        return qs


    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)

        search_result = self._search_result
        pagination_query = parse_pagination_query(request=self.request)
        pagination = get_pagination_data(search_result, pagination_query)
        tagcloud = get_tagcloud_data(tags=search_result.facets.tags, request=self.request)

        context.update({
            'facets': search_result.facets,
            'num_results': search_result.hits.total,
            'pagination': pagination,
            'tagcloud': tagcloud,
            'filters': get_filter_data(search_result.facets),
        })

        return context
