# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.http import HttpResponse
from django.conf import settings
from django.core.validators import validate_email
from django import forms
from django.views.generic import View
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

#from models import Subscription
from subscription.models import Subscription, Newsletter

WEBHOOK_TOKEN = getattr(settings, 'SUBSCRIPTION_WEBHOOK_TOKEN', None)
VALID_BACKENDS = [
    'mailchimp',
]

class SubscribeView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request, *args, **kwargs):

        list_id = kwargs.get('list_id', None)
        email = request.POST.get('email', None)
        name = request.POST.get('name', None)
        action = request.POST.get('action', None)
        channel = request.POST.get('channel', 'general')

        valid = True
        message = ''

        if not (action and list_id):
            valid = False
            message = _(u'Incomplete form')

        try:
            validate_email(email)
        except forms.ValidationError as e:
            valid = False
            message = u'Invalid e-mail address'


        if valid:

            newsletter = Newsletter.objects.get(id=list_id)
            subscription = Subscription.objects.filter(newsletter=newsletter, email=email.strip())

            if action == 'subscribe':

                if subscription.exists() and not subscription[0].opted_out:
                    print 'got active subscription -> skip'
                    message = u'You are already subscribed to this newsletter'
                elif subscription.exists():
                    print 'got canceled subscription -> update'
                    subscription[0].opted_out = None
                    subscription[0].save()
                    subscription[0].subscribe()
                    message = u'Subscription updated'
                else:
                    print 'no subscription -> create'
                    subscription = Subscription(
                        newsletter=newsletter,
                        email=email,
                        name=name,
                        language=get_language()[0:2],
                        channel=channel
                    )
                    subscription.save()
                    subscription.update_subscription()
                    message = u'You\'ve successfully signed-up for the newsletter. Soon you will receive an email to confirm your subscription.'

            if action == 'unsubscribe':
                if subscription.exists():
                    subscription[0].opted_out = False
                    subscription[0].save()
                    subscription[0].unsubscribe()

        return self.render_json_response(
            {
                'success': valid,
                'message': message,
            })




class WebhookView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):

        token = kwargs.get('token', None)
        backend = kwargs.get('backend', None)

        if not backend in VALID_BACKENDS:
            return HttpResponseForbidden('Invalid webhook backend')

        if not token == WEBHOOK_TOKEN:
            return HttpResponseForbidden('Invalid webhook token')

        return super(WebhookView, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):

        return self.render_json_response(
            {u"message": u"OK!"})



    def post(self, request, *args, **kwargs):

        #print request


        """
        subscribes data:
        https://apidocs.mailchimp.com/webhooks/

        "type": "subscribe",
        "fired_at": "2009-03-26 21:35:57",
        "data[id]": "8a25ff1d98",
        "data[list_id]": "a6b5da1054",
        "data[email]": "api@mailchimp.com",
        "data[merges][EMAIL]": "api@mailchimp.com",
        "data[merges][FNAME]": "MailChimp",
        "data[merges][LNAME]": "API",
        """

        ###
        action = request.POST.get('type', None)
        email = request.POST.get('data[email]', None)
        first_name = request.POST.get('data[merges][FNAME]', None)
        last_name = request.POST.get('data[merges][LNAME]', None)

        if kwargs['backend'] == 'mailchimp':
            backend_id = request.POST.get('data[list_id]', None)
            subscription_backend_id = request.POST.get('data[id]', None)

        try:
            newsletter = Newsletter.objects.get(backend_id=backend_id)
            subscription = Subscription.objects.get(newsletter=newsletter, email=email.strip())

        except:
            return self.render_json_response({u"status": u"Unknown subscription"})

        if action == 'subscribe':
            subscription.opted_out = None
            subscription.confirmed = timezone.now()
            subscription.save()

        if action == 'unsubscribe':
            subscription.opted_out = timezone.now()
            subscription.confirmed = None
            subscription.save()

        if action == 'profile':

            if first_name and last_name:
                subscription.name = u'%s %s' % (first_name, last_name)
                subscription.save()

        return self.render_json_response({u"status": u"Updated subscription"})