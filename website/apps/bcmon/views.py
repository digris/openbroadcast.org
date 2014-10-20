from django.views.generic import DetailView, ListView
from django.shortcuts import render_to_response

from django.http import HttpResponse
from django.template import RequestContext

from django.core import serializers

from wdd.models import Entry, Room


class RoomList(ListView):

    model = Room


class RoomDetail(DetailView):

    model = Room


def home(request):
    
    data = {}

    return render_to_response('wdd/home.html', data, context_instance=RequestContext(request))


def chat(request, room=None, mimetype='json'):
    
    entries = Entry.objects.all()

    if mimetype == 'json':
        
        js = serializers.get_serializer("json")()
        data = js.serialize(entries, ensure_ascii=False)

        return HttpResponse(data, mimetype="application/json")
    
    if mimetype == 'html':

        return render_to_response('wdd/chat.html', {'entries': entries})