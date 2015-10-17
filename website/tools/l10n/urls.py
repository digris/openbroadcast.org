from django.conf.urls import *
from l10n.views import CountryAreas

urlpatterns = patterns(
    '',
    url(r'country/areas/', CountryAreas.as_view(),
        name='l10n_country_areas'),
    )
