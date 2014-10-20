from django.views.generic import DetailView
from django.conf import settings

from pure_pagination.mixins import PaginationMixin

from alibrary.forms import *
# from alibrary.filters import ArtistFilter

from lib.util import tagging_extra


ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12,24,36,120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)


class LicenseDetailView(DetailView):

    context_object_name = "license"
    model = License