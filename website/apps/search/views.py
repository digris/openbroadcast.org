# views.py
import json
from django.http import HttpResponse
from django.shortcuts import render
from haystack.query import SearchQuerySet


def index(request):
    return render(request, 'search/index.html')


def autocomplete(request):

    #sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:50]
    sqs = SearchQuerySet().load_all().auto_query(request.GET.get('q', ''))
    suggestions = [result.object.name for result in sqs]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')