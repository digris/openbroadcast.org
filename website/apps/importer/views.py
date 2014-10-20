from django.views.generic import ListView, UpdateView, CreateView, DeleteView, View

from django.views.generic.detail import TemplateResponseMixin
from  django.views.generic.edit import FormMixin, ProcessFormView
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, \
    HttpResponseForbidden
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from django import http
from django.utils import simplejson as json

from importer.models import *
from importer.forms import *


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context['result'])


class ImportListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Import

    permission_required = 'importer.add_import'
    raise_exception = True

    def get_queryset(self):
        kwargs = {}
        return Import.objects.filter(user=self.request.user)


class ImportDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Import
    success_url = lazy(reverse, str)("importer-import-list")

    permission_required = 'importer.delete_import'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        obj = Import.objects.get(pk=int(kwargs['pk']))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(ImportDeleteView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        kwargs = {}
        return Import.objects.filter(user=self.request.user)


class ImportDeleteAllView(LoginRequiredMixin, PermissionRequiredMixin, View):

    url = lazy(reverse, str)("importer-import-list")

    permission_required = 'importer.delete_import'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.url)

    def post(self, request, *args, **kwargs):
        Import.objects.filter(user=self.request.user).delete()
        return HttpResponseRedirect(self.url)



"""
NOT WORKING!!
"""


class ImportModifyView(LoginRequiredMixin, PermissionRequiredMixin, JSONResponseMixin, UpdateView):
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
        if meta.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or "json" in meta.get(
                "CONTENT_TYPE") or 1 == 1:
            context['result'] = {'status': True}

            return JSONResponseMixin.render_to_response(self, context)
        else:
            return HttpResponseForbidden()


"""
Model version, adding some extra fields to the import session
"""


class ImportCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Import

    permission_required = 'importer.add_import'
    raise_exception = True

    template_name = 'importer/import_create.html'
    form_class = ImportCreateModelForm
    # success_url = lazy(reverse, str)("feedback-feedback-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_absolute_url())


class ImportUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Import
    template_name = 'importer/import_form_pushy.html'

    permission_required = 'importer.change_import'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        obj = Import.objects.get(pk=int(kwargs['pk']))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(ImportUpdateView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        kwargs = {}
        return Import.objects.filter(user=self.request.user)


@login_required
@csrf_exempt
def multiuploader(request, import_id):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    result = []

    if request.method == 'POST':
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')


        # getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        import_session = Import.objects.get(pk=import_id)

        import_file = ImportFile()
        import_file.import_session = import_session
        import_file.filename = str(filename)
        import_file.file = file
        import_file.save()

        thumb_url = ''  # does not exist, as audio only

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL + '/'
            file_url = settings.MULTI_IMAGE_URL + '/' + image.key_data + '/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/' + import_file.filename + '/'

        #generating json response array
        result.append({"name": import_file.filename,
                       "size": import_file.file.size,
                       "url": import_file.file.url,
                       "id": '%s' % import_file.pk,
                       "thumbnail_url": '',
                       "delete_url": import_file.get_delete_url(),
                       "delete_type": "POST", })

    else:

        import_files = ImportFile.objects.filter(status=0)
        for import_file in import_files:
            result.append({"name": import_file.filename,
                           "size": import_file.file.size,
                           "url": import_file.file.url,
                           "id": '%s' % import_file.pk,
                           "thumbnail_url": '',
                           "delete_url": import_file.get_delete_url(),
                           "delete_type": "POST", })

    response_data = simplejson.dumps(result)
    if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'
    return HttpResponse(response_data, mimetype=mimetype)













