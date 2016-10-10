# -*- coding: utf-8 -*-
import logging
import json
import urllib
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .signals import webhook_signal

log = logging.getLogger(__name__)

SECURITY_TOKEN = getattr(settings, 'WEBHOOK_SECURITY_TOKEN', None)
SECURITY_TOKEN_KEY = 'challenge'
PAYLOAD_KEYS = getattr(settings, 'WEBHOOK_PAYLOAD_KEYS', ['payload',])

"""
inspired by:
https://raw.githubusercontent.com/sheppard/django-github-hook/master/github_hook/views.py
"""

class WebookView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(WebookView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        name = kwargs.get('name', None)
        token = request.GET.get(SECURITY_TOKEN_KEY, None)

        return HttpResponse(token)

    def post(self, request, *args, **kwargs):

        name = kwargs.get('name', None)
        token = request.GET.get(SECURITY_TOKEN_KEY, None)

        if request.META.get('CONTENT_TYPE') == "application/json":
            payload = json.loads(request.body)
        else:
            payload = {}
            for key in PAYLOAD_KEYS:
                if key in request.POST:
                    payload = json.loads(request.POST['payload'])[0]
                    log.debug('payload by key "{}"'.format(key))
                    break

        if not payload:
            raise Exception(
                'Unable to extract payload'
            )

        print payload

        webhook_signal.send(WebookView, request=request, name=name, token=token, payload=payload)
        log.debug('Signal {} sent'.format(webhook_signal))



        return HttpResponse(token)