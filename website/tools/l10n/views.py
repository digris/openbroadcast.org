from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from l10n.models import Country, AdminArea

class CountryAreas(ListView):
    model = AdminArea
    template_name = "l10n/adminarea_list.json"
    def get_queryset(self):
        self.country = get_object_or_404(Country,
                                         id=self.request.GET['country_id'])
        return AdminArea.objects.filter(country=self.country, active=True)
