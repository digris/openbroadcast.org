
from django.template import RequestContext
from django.shortcuts import render_to_response

def popup(request, username=None):

    data = {}

    return render_to_response('aplayer/popup.html', data, context_instance=RequestContext(request))
