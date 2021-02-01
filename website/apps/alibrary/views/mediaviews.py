# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import actstream
import datetime
import logging

from django.views.generic import DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from elasticsearch_dsl import TermsFacet, RangeFacet

from base.utils.form_errors import merge_form_errors
from base.views.detail import SectionDetailView
from search.views import BaseFacetedSearch, BaseSearchListView
from search.duplicate_detection import get_ids_for_possible_duplicates

from ..models import Media, Playlist, PlaylistItem
from ..forms import (
    MediaForm,
    MediaActionForm,
    MediaRelationFormSet,
    ExtraartistFormSet,
    MediaartistFormSet,
)
from ..documents import MediaDocument

log = logging.getLogger(__name__)


class MediaSearch(BaseFacetedSearch):
    doc_types = [MediaDocument]
    fields = ["tags", "name"]

    facets = [
        ("tags", TermsFacet(field="tags", size=100)),
        ("type", TermsFacet(field="type", size=20, order={"_key": "asc"})),
        ("version", TermsFacet(field="version", size=100, order={"_key": "asc"})),
        (
            "num_emissions",
            RangeFacet(
                field="num_emissions",
                ranges=[
                    ("0", (0, 1)),
                    ("1 - 10", (1, 10)),
                    ("11 - 50", (11, 50)),
                    ("More than 50", (51, None)),
                ],
            ),
        ),
        (
            "last_emission",
            RangeFacet(
                field="last_emission",
                ranges=[
                    (
                        "Last 7 days",
                        (
                            str((timezone.now() - datetime.timedelta(days=7)).date()),
                            None,
                        ),
                    ),
                    (
                        "Last month",
                        (
                            str((timezone.now() - datetime.timedelta(days=30)).date()),
                            None,
                        ),
                    ),
                    (
                        "More than a month ago",
                        (
                            None,
                            str((timezone.now() - datetime.timedelta(days=30)).date()),
                        ),
                    ),
                ],
            ),
        ),
        # (
        #     "bitrate",
        #     RangeFacet(
        #         field="bitrate",
        #         ranges=[
        #             ("Low", (0, 100)),
        #             ("Medium", (100, 200)),
        #             ("High", (200, None)),
        #         ],
        #     ),
        # ),
        # (
        #     "samplerate",
        #     RangeFacet(
        #         field="samplerate",
        #         ranges=[
        #             ("Low", (0, 44100)),
        #             ("Medium", (44100, 48000)),
        #             ("High", (48000, None)),
        #         ],
        #     ),
        # ),
        # ("encoding", TermsFacet(field="encoding", size=100)),
        # ("license", TermsFacet(field="license")),
        ("lyrics_language", TermsFacet(field="lyrics_language")),
        # ('key', __paste__),
    ]


class MediaListView(BaseSearchListView):
    model = Media
    template_name = "alibrary/media/list.html"
    search_class = MediaSearch
    order_by = [
        {
            "key": "name.raw",
            "name": _("Name"),
            "default_direction": "asc",
        },
        {
            "key": "artist_display.raw",
            "name": _("Artist name"),
            "default_direction": "asc",
        },
        {
            "key": "duration",
            "name": _("Duration"),
            "default_direction": "asc",
        },
        # {
        #     'key': 'tempo',
        #     'name': _('BPM'),
        #     'default_direction': 'asc',
        # },
        {
            "key": "num_emissions",
            "name": _("Num Emissions"),
            "default_direction": "desc",
        },
        {
            "key": "last_emission",
            "name": _("Last Emission"),
            "default_direction": "desc",
        },
        {
            "key": "updated",
            "name": _("Last modified"),
            "default_direction": "desc",
        },
        {
            "key": "created",
            "name": _("Creation date"),
            "default_direction": "desc",
        },
    ]

    def get_queryset(self, **kwargs):

        limit_ids = None

        # TODO: special purpose filters. should be moved to generic place & add parameter validation
        duplicate_filter = self.request.GET.get("duplicate_filter", None)
        if duplicate_filter:
            fields = duplicate_filter.split(":")
            limit_ids = get_ids_for_possible_duplicates("media", fields)

        qs = super(MediaListView, self).get_queryset(limit_ids=limit_ids, **kwargs)

        # qs = qs.select_related("release", "artist", "license", 'release__label', 'preflight_check').prefetch_related(
        #     "media_artists", "extra_artists"
        # )

        qs = qs.select_related(
            "release",
            "artist",
            "release__label",
            "release__release_country",
            "preflight_check",
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        return context


class MediaDetailViewLegacy(DetailView):
    model = Media

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return redirect(obj.get_absolute_url())


    # extra_context = {}
    #
    # def get_context_data(self, **kwargs):
    #
    #     context = super(MediaDetailViewLegacy, self).get_context_data(**kwargs)
    #     obj = kwargs.get("object", None)
    #
    #     self.extra_context["history"] = []
    #
    #     # foreign appearance
    #     ps = []
    #     try:
    #         pis = PlaylistItem.objects.filter(
    #             object_id=obj.id, content_type=ContentType.objects.get_for_model(obj)
    #         )
    #         ps = Playlist.objects.exclude(type="basket").filter(items__in=pis)
    #     except:
    #         pass
    #
    #     self.extra_context["appearance"] = ps
    #     context.update(self.extra_context)
    #
    #     return context


class MediaDetailView(SectionDetailView):
    model = Media
    template_name = "alibrary/media/detail.html"
    section_template_pattern = "alibrary/media/detail/_{key}.html"
    context_object_name = "media"
    url_name = "alibrary-media-detail"

    sections = [
        {
            "key": "overview",
            "url": None,
            "title": _("Overview"),
        },
        {
            "key": "credits",
            "url": "credits",
            "title": _("Credits"),
        },
        {
            "key": "description",
            "url": "description",
            "title": _("Description"),
        },
        {
            "key": "videoclips",
            "url": "videoclips",
            "title": _("Video clips"),
        },
        {
            "key": "lyrics",
            "url": "lyrics",
            "title": _("Lyrics"),
        },
        {
            "key": "statistics",
            "url": "statistics",
            "title": _("Statistics"),
        },
    ]

    def get_sections(self, *args, **kwargs):
        sections = self.sections
        obj = self.get_object()
        if not obj.description:
            sections = [s for s in sections if not s['key'] == 'description']
        if not obj.lyrics:
            sections = [s for s in sections if not s['key'] == 'lyrics']
        if not obj.extraartist_media.exists():
            sections = [s for s in sections if not s['key'] == 'credits']
        if not obj.get_videoclips().exists():
            sections = [s for s in sections if not s['key'] == 'videoclips']
        return sections

    def get_context_data(self, *args, **kwargs):
        context = super(MediaDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()

        playlist_qs = PlaylistItem.objects.filter(
            object_id=obj.id, content_type=ContentType.objects.get_for_model(obj)
        )
        broadcasts = Playlist.objects.filter(type=Playlist.TYPE_BROADCAST, items__in=playlist_qs)
        playlists = Playlist.objects.filter(type=Playlist.TYPE_PLAYLIST, items__in=playlist_qs)

        context.update({
            "broadcasts": broadcasts,
            "playlists": playlists,
        })

        return context



class MediaEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Media
    form_class = MediaForm
    template_name = "alibrary/media/edit.html"
    permission_required = "alibrary.change_media"
    raise_exception = True
    success_url = "#"

    def __init__(self, *args, **kwargs):
        self.created_artists = {}
        super(MediaEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update(
            {
                "user": self.request.user,
                "d_tags": ",".join(t.name for t in self.object.tags),
            }
        )
        return self.initial

    def get_context_data(self, **kwargs):
        ctx = super(MediaEditView, self).get_context_data(**kwargs)
        ctx["named_formsets"] = self.get_named_formsets()
        # TODO: is this a good way to pass the instance main form?
        ctx["form_errors"] = self.get_form_errors(form=ctx["form"])

        return ctx

    def get_named_formsets(self):

        return {
            "action": MediaActionForm(self.request.POST or None, prefix="action"),
            "relation": MediaRelationFormSet(
                self.request.POST or None, instance=self.object, prefix="relation"
            ),
            "extraartist": ExtraartistFormSet(
                self.request.POST or None, instance=self.object, prefix="extraartist"
            ),
            "mediaartists": MediaartistFormSet(
                self.request.POST or None, instance=self.object, prefix="mediaartists"
            ),
        }

    def get_form_errors(self, form=None):

        named_formsets = self.get_named_formsets()
        named_formsets.update({"form": form})
        form_errors = merge_form_errors(
            [formset for name, formset in named_formsets.items()]
        )

        return form_errors

    def form_valid(self, form):

        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save(commit=False)

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, "formset_{0}_valid".format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        d_tags = form.cleaned_data["d_tags"]
        if d_tags:
            self.object.tags = d_tags

        self.object.last_editor = self.request.user
        actstream.action.send(self.request.user, verb=_("updated"), target=self.object)

        # revisions disabled -> needs refactoring
        self.object = form.save()
        messages.add_message(self.request, messages.INFO, "Object updated")

        return HttpResponseRedirect(self.object.get_edit_url())
