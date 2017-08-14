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


        print('****************************')
        print(request.POST)
        print(request.body)
        print('----------------------------')


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

        for account in payload['list_folder']['accounts']:
            process_user(account)




        webhook_signal.send(WebookView, request=request, name=name, token=token, payload=payload)
        log.debug('Signal {} sent'.format(webhook_signal))



        return HttpResponse(token)



def process_user(account):



    print('process_user')
    print(account)

    # # OAuth token for the user
    # token = redis_client.hget('tokens', account)
    #
    # # cursor for the user (None the first time)
    # cursor = redis_client.hget('cursors', account)
    #
    # dbx = Dropbox(token)
    # has_more = True
    #
    # while has_more:
    #     if cursor is None:
    #         result = dbx.files_list_folder(path='')
    #     else:
    #         result = dbx.files_list_folder_continue(cursor)
    #
    #     for entry in result.entries:
    #         # Ignore deleted files, folders, and non-markdown files
    #         if (isinstance(entry, DeletedMetadata) or
    #             isinstance(entry, FolderMetadata) or
    #             not entry.path_lower.endswith('.md')):
    #             continue
    #
    #         # Convert to Markdown and store as <basename>.html
    #         _, resp = dbx.files_download(entry.path_lower)
    #         html = markdown(resp.content)
    #         dbx.files_upload(html, entry.path_lower[:-3] + '.html', mode=WriteMode('overwrite'))
    #
    #     # Update cursor
    #     cursor = result.cursor
    #     redis_client.hset('cursors', account, cursor)
    #
    #     # Repeat only if there's more to do
    #     has_more = result.has_more
