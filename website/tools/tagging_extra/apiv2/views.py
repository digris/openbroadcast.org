# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework.decorators import api_view

from tagging.models import Tag


@api_view(['GET'])
def tag_list(request):
    q = request.GET.get('q', None)
    if q:
        qs = Tag.objects.filter(name__istartswith=q)
        results = [t.name for t in qs[0:20]]
    else:
        results = []
    return Response({"results": results})
