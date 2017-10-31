# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import ntpath
import os

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django import http
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, HttpResponseForbidden)
from django.utils.functional import lazy
from django.views.generic import ListView, DetailView
from .models import Massimport
from alibrary.models import Media
from importer.models import ImportFile
from pure_pagination.mixins import PaginationMixin


class MassimportListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    model = Massimport
    paginate_by = 12
    permission_required = 'massimporter.massimport_manage'
    raise_exception = True

    def get_queryset(self):
        kwargs = {}
        #return Massimport.objects.filter(user=self.request.user)
        return Massimport.objects.all()


class MassimportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Massimport
    permission_required = 'massimporter.massimport_manage'
    raise_exception = True

    def get_object(self):
        return Massimport.objects.get(uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):

        context = super(MassimportDetailView, self).get_context_data(**kwargs)

        ###############################################################
        # gather summary of import
        ###############################################################

        obj = self.object

        # summary querysets
        qs_all = obj.import_session.files.all().nocache()
        qs_duplicate = qs_all.filter(status=ImportFile.STATUS_DUPLICATE)
        qs_done = qs_all.filter(status=ImportFile.STATUS_DONE)


        # plausibility check - compare if we can find the title in original filename
        possible_name_mismatch = []
        for item in qs_duplicate:
            m_name = clean_filename(item.media.name)
            m_orig = clean_filename(ntpath.basename(item.filename))
            if not (m_name.lower() in m_orig.lower()):
                possible_name_mismatch.append({
                    'item': item,
                    'media': item.media,
                    'filename': m_orig,
                })


        # check for possible unrecognized duplicates
        possible_duplicates = []
        for item in qs_done:

            if not (hasattr(item, 'media') and item.media and item.media.master and item.media.master_duration):
                continue

            # search for exact duplicates by name (title & artist)
            dupe_qs = Media.objects.exclude(pk=item.media.pk).filter(
                name=item.media.name, artist__name=item.media.artist.name
            )

            # withon a small window of same duration
            d_range = (item.media.master_duration - 1.0, item.media.master_duration + 1.0)

            duplicates_qs = dupe_qs.filter(master_duration__range=d_range)

            if duplicates_qs.exists():
                possible_duplicates.append({
                    'item': item,
                    'media': item.media,
                    'duplicates_qs': duplicates_qs,
                })

        context.update({
            'qs_all': qs_all,
            'qs_duplicate': qs_duplicate,
            'qs_done': qs_done,

            'possible_name_mismatch': possible_name_mismatch,
            'possible_duplicates': possible_duplicates,
        })

        return context


def clean_filename(filename):

    filename = filename.replace(u"’", u"'")
    filename = filename.replace(u"-", u" ")
    filename = filename.replace(u"_", u" ")
    filename = filename.lstrip('0123456789.- ')
    filename = os.path.splitext(filename)[0]

    return filename
