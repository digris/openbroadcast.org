from tagging.models import Tag
from django.http import HttpResponse
import json
from django.utils.datastructures import MultiValueDictKeyError


def list_tags(request):
    try:
        tags = Tag.objects.filter(name__istartswith=request.GET["term"]).values_list(
            "name", flat=True
        )
    except MultiValueDictKeyError:
        tags = []

    return JsonResponse([x for x in tags])


class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json`` mimetype.
    """

    def __init__(self, data):

        print("data", data)

        super().__init__(
            content=json.dumps(data), content_type="application/json"
        )
