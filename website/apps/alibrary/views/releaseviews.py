# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import actstream
import logging

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, UpdateView
from elasticsearch_dsl import TermsFacet, RangeFacet
from navutils import MenuMixin

from base.utils.form_errors import merge_form_errors
from base.models.utils.merge import merge_objects
from base.views.detail import SectionDetailView
from search.views import BaseFacetedSearch, BaseSearchListView
from search.duplicate_detection import get_ids_for_possible_duplicates

from ..forms import (
    ReleaseForm,
    ReleaseActionForm,
    ReleaseBulkeditForm,
    ReleaseRelationFormSet,
    AlbumartistFormSet,
    ReleaseMediaFormSet,
)
from ..models import Release, Artist, ReleaseAlbumartists
from ..documents import ReleaseDocument


log = logging.getLogger(__name__)


class ReleaseSearch(BaseFacetedSearch):
    doc_types = [ReleaseDocument]
    fields = ["tags", "name"]

    facets = [
        ("tags", TermsFacet(field="tags", size=200)),
        (
            "releasedate",
            RangeFacet(
                field="releasedate_year",
                ranges=[
                    ("Before 1940's", (0, 1940)),
                    ("40's", (1940, 1950)),
                    ("50's", (1950, 1960)),
                    ("60's", (1960, 1970)),
                    ("70's", (1970, 1980)),
                    ("80's", (1980, 1990)),
                    ("90's", (1990, 2000)),
                    ("2000's", (2000, 2010)),
                    ("2010's", (2010, 2019)),
                    ("2020's", (2020, 2029)),
                    ("This Year", (2021, 2022)),
                ],
            ),
        ),
        ("type", TermsFacet(field="type", size=20, order={"_key": "asc"})),
        ("country", TermsFacet(field="country", size=500, order={"_key": "asc"})),
        ("label_type", TermsFacet(field="label_type", size=100)),
    ]


class ReleaseListView(MenuMixin, BaseSearchListView):
    model = Release
    template_name = "alibrary/release/list.html"
    current_menu_item = "catalog:releases"
    search_class = ReleaseSearch
    order_by = [
        {"key": "name.raw", "name": _("Name"), "default_direction": "asc"},
        {
            "key": "releasedate",
            "name": _("Releasedate"),
            "default_direction": "asc",
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
            limit_ids = get_ids_for_possible_duplicates("releases", fields)

        # just testing rating
        # from django.contrib.contenttypes.models import ContentType
        # from arating.models import Vote
        # limit_ids = Vote.objects.filter(
        #     vote__gte=1,
        #     user=self.request.user,
        #     content_type=ContentType.objects.get_for_model(self.model),
        # ).values_list('object_id', flat=True)

        qs = super(ReleaseListView, self).get_queryset(limit_ids=limit_ids, **kwargs)

        qs = qs.select_related(
            "label",
            "release_country",
            "creator",
            "creator__profile",
        ).prefetch_related(
            "media",
            "media__artist",
            "media__license",
            "extra_artists",
            "album_artists",
        )

        return qs


class ReleaseDetailViewLegacy(DetailView):
    model = Release

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return redirect(obj.get_absolute_url())


class ReleaseDetailView(MenuMixin, SectionDetailView):
    model = Release
    template_name = "alibrary/release/detail.html"
    section_template_pattern = "alibrary/release/detail/_{key}.html"
    context_object_name = "release"
    url_name = "alibrary-release-detail"

    sections = [
        {
            "key": "tracklist",
            "url": None,
            "title": _("Tracks"),
        },
        {
            "key": "description",
            "url": "description",
            "title": _("Description"),
        },
        {
            "key": "statistics",
            "url": "statistics",
            "title": _("Statistics"),
        },
        # {
        #     "key": "license",
        #     "url": "license",
        #     "title": _("License / Legal"),
        # },
    ]

    def get_sections(self, *args, **kwargs):
        sections = self.sections
        obj = self.get_object()
        if not obj.description:
            sections = [s for s in sections if not s["key"] == "description"]
        # if not obj.get_license():
        #     sections = [s for s in sections if not s["key"] == "license"]
        return sections

    def get_queryset(self):
        return self.model.objects.select_related(
            "release_country",
            "label",
            "creator",
            "last_editor",
        ).prefetch_related(
            "extra_artists",
            "album_artists",
            "media_release",
            "media_release__artist",
            "media_release__preflight_check",
        )


class ReleaseEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Release
    form_class = ReleaseForm
    template_name = "alibrary/release/edit.html"
    permission_required = "alibrary.change_release"
    raise_exception = True
    success_url = "#"

    def __init__(self, *args, **kwargs):
        self.created_artists = {}
        super(ReleaseEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update(
            {
                "user": self.request.user,
                "d_tags": ",".join(t.name for t in self.object.tags),
            }
        )
        return self.initial

    def get_context_data(self, **kwargs):
        ctx = super(ReleaseEditView, self).get_context_data(**kwargs)
        ctx["named_formsets"] = self.get_named_formsets()
        # TODO: is this a good way to pass the instance main form?
        ctx["form_errors"] = self.get_form_errors(form=ctx["form"])

        return ctx

    def get_named_formsets(self):

        return {
            "action": ReleaseActionForm(
                self.request.POST or None, instance=self.object, prefix="action"
            ),
            "bulkedit": ReleaseBulkeditForm(
                self.request.POST or None, instance=self.object, prefix="bulkedit"
            ),
            "relation": ReleaseRelationFormSet(
                self.request.POST or None, instance=self.object, prefix="relation"
            ),
            "albumartist": AlbumartistFormSet(
                self.request.POST or None, instance=self.object, prefix="albumartist"
            ),
            "media": ReleaseMediaFormSet(
                self.request.POST or None, instance=self.object, prefix="media"
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

        # moved to revision transaction
        # for name, formset in named_formsets.items():
        #     formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
        #     if formset_save_func is not None:
        #         formset_save_func(formset)
        #     else:
        #         formset.save()

        # publish = self.do_publish

        """
        # publishing is depreciated
        if publish:
            from datetime import datetime
            self.object.publish_date = datetime.now()
            self.object.publisher = self.request.user
            self.object.save()
        """

        actstream.action.send(self.request.user, verb=_("updated"), target=self.object)

        # self.object.last_editor = self.request.user
        # we pass last editor as attribut (not to field directly) and handle information in save()
        self.object._last_editor = self.request.user

        self.object = form.save()

        self.formset_media_valid(named_formsets["media"])

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, "formset_{0}_valid".format(name), None)
            if name != "media":
                if formset_save_func is not None:
                    formset_save_func(formset)
                else:
                    formset.save()

        d_tags = form.cleaned_data["d_tags"]
        if d_tags:
            self.object.tags = d_tags

        messages.add_message(self.request, messages.INFO, "Object updated")

        return HttpResponseRedirect(self.object.get_edit_url())

    def formset_media_valid(self, formset):
        media = formset.save(commit=False)

        # TODO: this is extremely ugly!! refactor!
        import hashlib

        for m in media:
            if m.artist and not m.artist.pk:
                key = hashlib.md5(m.artist.name.encode("ascii", "ignore")).hexdigest()
                try:
                    artist = self.created_artists[key]
                except KeyError as e:
                    m.artist.save()
                    artist = m.artist
                    self.created_artists[key] = artist

                m.artist = artist

            # pass last editor
            m.last_editor = self.request.user

            # hackish way to handle 'ghost tags'
            m.d_tags = ",".join(t.name for t in m.tags)

            m.save()

            if formset.has_changed():
                # set actstream (e.v. atracker?)
                actstream.action.send(self.request.user, verb=_("updated"), target=m)

    def formset_albumartist_valid(self, formset):

        import hashlib

        # TODO: this is extremely ugly!! refactor!
        albumartists = formset.save(commit=False)

        delete_qs = ReleaseAlbumartists.objects.filter(release__pk=self.object.pk)
        delete_qs = delete_qs.exclude(
            artist__pk__in=[a.artist.pk for a in albumartists]
        )
        delete_qs.delete()

        for albumartist in albumartists:
            key = hashlib.md5(
                albumartist.artist.name.encode("ascii", "ignore")
            ).hexdigest()
            try:
                artist = self.created_artists[key]
            except KeyError as e:
                pass
            else:
                delete_pk = albumartist.artist.pk
                albumartist.artist = artist
                albumartist.save()
                merge_objects(albumartist.artist, [Artist.objects.get(pk=delete_pk)])

            albumartist.save()

    def formset_action_valid(self, formset):
        self.do_publish = formset.cleaned_data.get("publish", False)
