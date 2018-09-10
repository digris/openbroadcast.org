# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.views.generic import DetailView, ListView

from ..models import License

class LicenseDetailView(DetailView):
    context_object_name = "license"
    model = License


