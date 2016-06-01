from django.conf import settings
from django.views.generic import DetailView

from ..models import License

ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12, 24, 36, 120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)


class LicenseDetailView(DetailView):
    context_object_name = "license"
    model = License
