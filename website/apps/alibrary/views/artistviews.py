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
from search.duplicate_detection import get_ids_for_possible_duplicates

from ..models import Artist, Release, Media, NameVariation
from ..forms import (
    ArtistForm,
    ArtistActionForm,
    ArtistRelationFormSet,
    MemberFormSet,
    AliasFormSet,
)
from ..documents import ArtistDocument

log = logging.getLogger(__name__)


class ArtistSearch(BaseFacetedSearch):
    doc_types = [ArtistDocument]
    fields = ["tags", "name"]

    facets = [
        ("tags", TermsFacet(field="tags", size=100)),
        ("country", TermsFacet(field="country", size=500, order={"_key": "asc"})),
        ("type", TermsFacet(field="type", size=20, order={"_key": "asc"})),
    ]


class ArtistListView(BaseSearchListView):
    model = Artist
    template_name = "alibrary/artist_list.html"
    search_class = ArtistSearch
    order_by = [
        {"key": "name.raw", "name": _("Name"), "default_direction": "asc"},
        {
            "key": "year_start",
            "name": _("Date of formation / date of birth"),
            "default_direction": "desc",
        },
        {
            "key": "year_end",
            "name": _("Date of breakup / date of death"),
            "default_direction": "desc",
        },
        {"key": "updated", "name": _("Last modified"), "default_direction": "desc"},
        {"key": "created", "name": _("Creation date"), "default_direction": "desc"},
    ]

    def get_queryset(self, **kwargs):

        limit_ids = None

        # TODO: special purpose filters. should be moved to generic place & add parameter validation
        duplicate_filter = self.request.GET.get("duplicate_filter", None)
        if duplicate_filter:
            fields = duplicate_filter.split(":")
            limit_ids = get_ids_for_possible_duplicates("artists", fields)

        qs = super(ArtistListView, self).get_queryset(limit_ids=limit_ids, **kwargs)

        qs = qs.select_related("country").prefetch_related(
            "creator", "creator__profile"
        )

        return qs


class ArtistDetailView(DetailView):
    context_object_name = "artist"
    model = Artist
    extra_context = {}

    def render_to_response(self, context):
        return super(ArtistDetailView, self).render_to_response(
            context, content_type="text/html"
        )

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        obj = self.object

        extra_context = {}

        extra_context["releases"] = Release.objects.filter(
            Q(media_release__artist=obj) | Q(album_artists=obj)
        ).distinct()[0:8]

        """
        top-flop
        """
        m_top = []
        media_top = (
            Media.objects.filter(artist=obj, votes__vote__gt=0)
            .order_by("-votes__vote")
            .distinct()
        )
        if media_top.exists():
            media_top = media_top[0:10]
            for media in media_top:
                m_top.append(media)

        m_flop = []
        media_flop = (
            Media.objects.filter(artist=obj, votes__vote__lt=0)
            .order_by("votes__vote")
            .distinct()
        )
        if media_flop.exists():
            media_flop = media_flop[0:10]
            for media in media_flop:
                m_flop.append(media)

        extra_context["m_top"] = m_top
        extra_context["m_flop"] = m_flop

        extra_context["m_contrib"] = Media.objects.filter(extra_artists=obj)[0:48]
        extra_context["history"] = []
        extra_context["appearances"] = {
            "media": obj.get_media(),
            "releases": obj.get_releases(),
        }

        context.update(extra_context)

        return context


class ArtistEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = "alibrary/artist_edit.html"
    permission_required = "alibrary.change_artist"
    raise_exception = True
    success_url = "#"

    def __init__(self, *args, **kwargs):
        super(ArtistEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update(
            {
                "user": self.request.user,
                "d_tags": ",".join(t.name for t in self.object.tags),
            }
        )
        return self.initial

    def get_context_data(self, **kwargs):
        context = super(ArtistEditView, self).get_context_data(**kwargs)
        obj = self.object

        extra_context = {}

        extra_context["named_formsets"] = self.get_named_formsets()
        extra_context["form_errors"] = self.get_form_errors(form=context["form"])
        extra_context["appearances"] = {
            "media": obj.get_media(),
            "releases": obj.get_releases(),
        }
        context.update(extra_context)

        return context

    def get_named_formsets(self):

        return {
            "action": ArtistActionForm(self.request.POST or None, prefix="action"),
            "relation": ArtistRelationFormSet(
                self.request.POST or None, instance=self.object, prefix="relation"
            ),
            "member": MemberFormSet(
                self.request.POST or None, instance=self.object, prefix="member"
            ),
            "alias": AliasFormSet(
                self.request.POST or None, instance=self.object, prefix="alias"
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

        # TODO: implement in a better way
        namevariations_text = form.cleaned_data["namevariations"]
        if namevariations_text:
            self.object.namevariations.all().delete()
            variations = namevariations_text.split(",")
            for v in variations:
                nv = NameVariation(name=v.strip(), artist=self.object)
                nv.save()
        else:
            self.object.namevariations.all().delete()

        d_tags = form.cleaned_data["d_tags"]
        if d_tags:
            self.object.tags = d_tags

        self.object.last_editor = self.request.user
        actstream.action.send(self.request.user, verb=_("updated"), target=self.object)

        self.object = form.save()
        messages.add_message(self.request, messages.INFO, "Object updated")

        return HttpResponseRedirect(self.object.get_edit_url())
