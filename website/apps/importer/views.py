# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django import http
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.functional import lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, View, RedirectView
from importer.forms import ImportCreateModelForm
from importer.models import Import
from pure_pagination.mixins import PaginationMixin


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(
            content, content_type="application/json", **httpresponse_kwargs
        )

    def convert_context_to_json(self, context):
        return json.dumps(context["result"])


class ImportListView(
    LoginRequiredMixin, PermissionRequiredMixin, PaginationMixin, ListView
):
    model = Import
    paginate_by = 12
    permission_required = "importer.add_import"
    raise_exception = True

    def get_queryset(self):
        kwargs = {}

        qs = self.model.objects.filter(user=self.request.user)

        qs = qs.select_related("user").prefetch_related("files", "importitem_set")

        return qs


class ImportDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Import
    success_url = lazy(reverse, str)("importer-import-list")

    permission_required = "importer.delete_import"
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        obj = Import.objects.get(pk=int(kwargs["pk"]))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(ImportDeleteView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        kwargs = {}
        return Import.objects.filter(user=self.request.user)


class ImportDeleteAllView(LoginRequiredMixin, PermissionRequiredMixin, View):
    url = lazy(reverse, str)("importer-import-list")

    permission_required = "importer.delete_import"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.url)

    def post(self, request, *args, **kwargs):
        Import.objects.filter(user=self.request.user).delete()
        return HttpResponseRedirect(self.url)


class ImportModifyView(
    LoginRequiredMixin, PermissionRequiredMixin, JSONResponseMixin, UpdateView
):
    model = Import

    def get_queryset(self):
        kwargs = {}
        return Import.objects.filter(user=self.request.user)

    def get(self, cls, **kwargs):
        cls.object = cls.get_object()
        kwargs.update({"object": cls.object})
        return cls, kwargs

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        meta = self.request.META
        if (
            meta.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
            or "json" in meta.get("CONTENT_TYPE")
            or 1 == 1
        ):
            context["result"] = {"status": True}

            return JSONResponseMixin.render_to_response(self, context)
        else:
            return HttpResponseForbidden()


# class ImportCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Import
#
#     permission_required = "importer.add_import"
#     raise_exception = True
#
#     template_name = "importer/import_create.html"
#     form_class = ImportCreateModelForm
#
#     # success_url = lazy(reverse, str)("feedback-feedback-list")
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.user = self.request.user
#         obj.save()
#         return HttpResponseRedirect(obj.get_absolute_url())


class ImportCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Import
    permission_required = "importer.add_import"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        obj = self.model()
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class ImportUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Import
    # template_name = 'importer/import_form.html'

    fields = "__all__"

    permission_required = "importer.change_import"
    raise_exception = True

    def get_template_names(self):

        if self.object.type == Import.TYPE_WEB:
            template_name = "importer/import_form.html"
        else:
            template_name = "importer/import_readonly_form.html"

        return [template_name]

    def dispatch(self, request, *args, **kwargs):
        obj = Import.objects.get(pk=int(kwargs["pk"]))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(ImportUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        kwargs = {}
        return Import.objects.filter(user=self.request.user).prefetch_related(
            "files", "files__media"
        )
