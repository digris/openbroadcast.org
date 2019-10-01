import logging

from django.views.generic import ListView, UpdateView, CreateView, DeleteView, View
from django.views.generic.detail import TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django import http
import json
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from sendfile import sendfile

from exporter.models import Export

log = logging.getLogger(__name__)


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


class ExportListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):

    model = Export

    permission_required = "exporter.add_export"
    raise_exception = True

    def get_queryset(self):
        kwargs = {}
        return Export.objects.filter(user=self.request.user)


class ExportDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):

    model = Export
    success_url = lazy(reverse, str)("exporter-export-list")

    permission_required = "exporter.delete_export"
    raise_exception = True

    def get_queryset(self):
        kwargs = {}
        return Export.objects.filter(user=self.request.user)


class ExportDeleteAllView(PermissionRequiredMixin, LoginRequiredMixin, View):

    model = Export
    success_url = lazy(reverse, str)("exporter-export-list")

    permission_required = "exporter.delete_export"
    raise_exception = True

    def get_queryset(self):
        kwargs = {}
        return Export.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        Export.objects.filter(user=self.request.user).delete()
        return HttpResponseRedirect(reverse("exporter-export-list"))


@login_required
def export_download(request, uuid, token):

    log = logging.getLogger("exporter.views.export_download")
    log.info("Download Request by: %s" % (request.user.username))

    export = get_object_or_404(Export, uuid=uuid)

    download_permission = False

    if request.user == export.user and token == export.token:
        download_permission = True

    if not download_permission:
        return HttpResponseForbidden("forbidden")

    filename = "%s.%s" % (export.filename, "zip")

    export.set_downloaded()

    return sendfile(
        request, export.file.path, attachment=True, attachment_filename=filename
    )
