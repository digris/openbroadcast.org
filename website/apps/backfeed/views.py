from django.template import RequestContext

from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse

import json

from django.shortcuts import render_to_response

from django.core.urlresolvers import reverse

from backfeed.models import Backfeed
from backfeed.forms import BackfeedForm


from django.contrib.auth.decorators import login_required


@login_required
def post(request):

    form = BackfeedForm()
    
    if request.method == 'POST':
        form = BackfeedForm(request.POST)

        if form.is_valid():

            bf = Backfeed()
            bf.subject = form.cleaned_data['subject']
            bf.message = form.cleaned_data['message']
            bf.user = request.user
            #post.user_ip = request.META['REMOTE_ADDR']

            bf.save()
            return HttpResponse(json.dumps({'status': True}), mimetype="application/json")

        else:
            return HttpResponse(json.dumps({'status': False, 'errors': form.errors}), mimetype="application/json")






    return HttpResponseNotAllowed(['POST',])
