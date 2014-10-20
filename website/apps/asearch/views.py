# views.py
import json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


def autocomplete(request):

    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:50]
    suggestions = [result.object.name for result in sqs]
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')