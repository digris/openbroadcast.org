# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import datetime

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from elasticsearch_dsl import TermsFacet, RangeFacet, DateHistogramFacet

from base.views.detail import UUIDDetailView
from search.views import BaseFacetedSearch, BaseSearchListView

from ..forms import PlaylistForm, ActionForm
from ..models import Playlist
from ..documents import PlaylistDocument

log = logging.getLogger(__name__)


class PlaylistSearch(BaseFacetedSearch):
    doc_types = [PlaylistDocument]
    fields = ["tags", "name"]

    facets = [
        ("tags", TermsFacet(field="tags", size=240)),
        ("type", TermsFacet(field="type", size=100, order={"_key": "asc"})),
        # ("status", TermsFacet(field="status", size=100, order={"_key": "asc"})),
        # ("weather", TermsFacet(field="weather", size=100, order={"_key": "asc"})),
        # ("seasons", TermsFacet(field="seasons", size=100, order={"_key": "asc"})),
        (
            "daypart_days",
            TermsFacet(field="daypart_days", size=100, order={"_key": "asc"}),
        ),
        (
            "daypart_slots",
            TermsFacet(field="daypart_slots", size=100, order={"_key": "asc"}),
        ),
        ("target_duration", TermsFacet(field="target_duration", size=100)),
        (
            "num_emissions",
            RangeFacet(
                field="num_emissions",
                ranges=[
                    ("0", (0, 1)),
                    ("1 - 10", (1, 10)),
                    ("11 - 50", (11, 50)),
                    ("More than 50", (50, None)),
                ],
            ),
        ),
        (
            "last_emission",
            RangeFacet(
                field="last_emission",
                ranges=[
                    # ('old', (None, '2016-01-01')),
                    # ('2016', ('2016-01-01', '2016-12-31')),
                    # ('2018', ('2018-01-01', '2018-12-31')),
                    # ('recent', ('2019-01-01', None)),
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
                    (
                        "More than year month ago",
                        (
                            None,
                            str((timezone.now() - datetime.timedelta(days=365)).date()),
                        ),
                    ),
                    # ('Exclude 48 hours', (
                    #     None,
                    #     str((timezone.now() - datetime.timedelta(hours=48)).date())
                    # )),
                ],
            ),
        ),
        (
            "next_emission",
            RangeFacet(
                field="next_emission",
                ranges=[
                    # ('old', (None, '2016-01-01')),
                    # ('2016', ('2016-01-01', '2016-12-31')),
                    # ('2018', ('2018-01-01', '2018-12-31')),
                    # ('recent', ('2019-01-01', None)),
                    (
                        "Next 7 days",
                        (
                            None,
                            str((timezone.now() + datetime.timedelta(days=7)).date()),
                        ),
                    ),
                    # ('Exclude 48 hours', (
                    #     str((timezone.now() + datetime.timedelta(hours=48)).date()),
                    #     None
                    # )),
                ],
            ),
        ),
        # ('last_emission', DateHistogramFacet(field='last_emission', interval='month')),
        ("flags", TermsFacet(field="state_flags", order={"_key": "asc"})),
    ]


class PlaylistListView(BaseSearchListView):
    model = Playlist
    template_name = "alibrary/playlist/list.html"
    search_class = PlaylistSearch
    scope = "public"
    order_by = [
        {"key": "name", "name": _("Name"), "default_direction": "asc"},
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
            "key": "next_emission",
            "name": _("Next Emission"),
            "default_direction": "asc",
        },
        {"key": "duration", "name": _("Duration"), "default_direction": "asc"},
        {"key": "updated", "name": _("Last modified"), "default_direction": "desc"},
        {"key": "created", "name": _("Creation date"), "default_direction": "desc"},
    ]

    def get_search_query(self, **kwargs):
        serach_query = super(PlaylistListView, self).get_search_query(**kwargs)

        if self.scope == "own":
            serach_query["searches"].update({"user": [self.request.user.username]})
        else:
            serach_query["searches"].update({"type": ["-Private Playlist"]})

        return serach_query

    def get_queryset(self, **kwargs):
        qs = super(PlaylistListView, self).get_queryset(**kwargs)

        qs = qs.select_related("series", "user", "user__profile").prefetch_related(
            "items", "dayparts", "seasons", "weather", "emissions"
        )

        # TODO: refactor enumerations
        if not self.scope == "own":
            qs = qs.exclude(type="basket")

        return qs


class PlaylistDetailView(UUIDDetailView, DetailView):
    context_object_name = "playlist"
    model = Playlist
    template_name = "alibrary/playlist/detail.html"


class PlaylistCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Playlist

    template_name = "alibrary/playlist_create.html"
    form_class = PlaylistForm

    permission_required = "alibrary.add_playlist"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(PlaylistCreateView, self).get_context_data(**kwargs)
        context["action_form"] = ActionForm()
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_edit_url())


class PlaylistDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Playlist
    template_name = "alibrary/playlist_delete.html"
    permission_required = "alibrary.delete_playlist"
    raise_exception = True

    # TODO: this is a hack/bug/issue
    # http://stackoverflow.com/questions/7039839/how-do-i-use-reverse-or-an-equivalent-to-refer-to-urls-that-are-hooked-into-dj
    success_url = reverse_lazy("alibrary-playlist-list")

    def dispatch(self, request, *args, **kwargs):

        # TODO: here we could implement permission check for 'shared-editing' playlists
        obj = Playlist.objects.get(pk=int(kwargs["pk"]))
        if not obj.user == request.user:
            raise PermissionDenied

        # check if possible to delete
        can_delete, reason = obj.can_be_deleted()
        if not can_delete:
            messages.add_message(request, messages.ERROR, reason)
            return HttpResponseRedirect(obj.get_edit_url())

        return super(PlaylistDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaylistDeleteView, self).get_context_data(**kwargs)

        return context


class PlaylistEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Playlist
    template_name = "alibrary/playlist_edit.html"
    success_url = "#"
    form_class = PlaylistForm

    permission_required = "alibrary.change_playlist"
    raise_exception = True

    def __init__(self, *args, **kwargs):
        super(PlaylistEditView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):

        # TODO: here we could implement permission check for 'shared-editing' playlists
        obj = Playlist.objects.get(pk=int(kwargs["pk"]))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(PlaylistEditView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update(
            {
                "user": self.request.user,
                "d_tags": ",".join(t.name for t in self.object.tags),
            }
        )
        return self.initial

    def get_context_data(self, **kwargs):

        context = super(PlaylistEditView, self).get_context_data(**kwargs)

        context["action_form"] = ActionForm()
        context["user"] = self.request.user
        context["request"] = self.request

        if (
            self.request.user.has_perm("importer.add_import")
            and not self.object.type == "broadcast"
        ):
            context["can_upload_media"] = True
        else:
            context["can_upload_media"] = False

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # validation
        if form.is_valid():
            self.object.tags = form.cleaned_data["d_tags"]

            # temporary instance to validate inline forms against
            tmp = form.save(commit=False)

            form.save()
            form.save_m2m()

            return HttpResponseRedirect("#")
        else:

            from base.utils.form_errors import merge_form_errors

            form_errors = merge_form_errors([form])

            return self.render_to_response(
                self.get_context_data(form=form, form_errors=form_errors)
            )


@login_required
def playlist_convert(request, pk, playlist_type):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)

    playlist, status = playlist.convert_to(playlist_type)
    if status:
        messages.add_message(
            request,
            messages.INFO,
            _(
                'Successfully converted "%s" to "%s"'
                % (playlist.name, playlist.get_type_display())
            ),
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            _('There occured an error while converting "%s"' % (playlist.name)),
        )

    return HttpResponseRedirect(playlist.get_edit_url())
