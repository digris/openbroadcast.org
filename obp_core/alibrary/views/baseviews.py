from django.views.generic import DetailView

from ..models import License


class LicenseDetailView(DetailView):
    context_object_name = "license"
    model = License
