# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from mailchimp import Mailchimp

log = logging.getLogger(__name__)

MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY', None)

class MailchimpBackend():

    def __init__(self, api_key=MAILCHIMP_API_KEY):
        if not api_key:
            raise ImproperlyConfigured('No Mailchimp API Key provided.')
        self.api = Mailchimp(api_key)

    def subscribe(self, list_id, email, name=None, language=None, channel=None):

        # split name
        names = name.split(' ')
        if len(names) == 1:
            first_name = names[0]
            last_name = None
        elif len(names) > 1:
            first_name = names[0]
            last_name = names[1]
        else:
            first_name = None
            last_name = None

        try:
            # http://kb.mailchimp.com/article/where-can-i-find-my-lists-merge-tags
            merge_vars = {}

            if first_name:
                merge_vars['FNAME'] = first_name

            if last_name:
                merge_vars['LNAME'] = last_name

            if language:
                merge_vars['MC_LANGUAGE'] = language

            if channel:
                merge_vars['CHANNEL'] = channel


            return self.api.lists.subscribe(list_id, email={'email': email}, merge_vars=merge_vars)
        except Exception, e:
            log.warning(u'unable to subscribe: %s' % e)

    def unsubscribe(self, list_id, email):
        try:
            return self.api.lists.unsubscribe(list_id, {'email': email})
        except Exception, e:
            log.warning(u'unable to unsubscribe: %s' % e)

        return
