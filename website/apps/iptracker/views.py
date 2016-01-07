# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from .models import Host

log = logging.getLogger(__name__)


class IPTrackerView(View):

    def get(self, *args, **kwargs):

        hostname = self.request.GET.get('hostname', None)

        if hostname:

            x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = self.request.META.get('REMOTE_ADDR')

            log.debug('update values for %s with ip %s' % (hostname, ip))

            host, created = Host.objects.get_or_create(hostname=hostname)
            host.ip = ip
            host.save()

            return HttpResponse(ip)


        else:

            return render(self.request, 'iptracker/index.html', {'hosts': Host.objects.all()}, content_type="text/html")

