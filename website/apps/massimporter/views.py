# Create your views here.
from __future__ import unicode_literals

import json

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django import http
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, HttpResponseForbidden)
from django.utils.functional import lazy
from django.views.generic import ListView, DetailView
from .models import Massimport
from pure_pagination.mixins import PaginationMixin


class MassimportListView(LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView):
    model = Massimport
    paginate_by = 12
    permission_required = 'importer.add_import'
    raise_exception = True

    def get_queryset(self):
        kwargs = {}
        #return Massimport.objects.filter(user=self.request.user)
        return Massimport.objects.all()


class MassimportDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Massimport
    permission_required = 'importer.add_import'
    raise_exception = True

    def get_object(self):
        return Massimport.objects.get(uuid=self.kwargs['uuid'])


