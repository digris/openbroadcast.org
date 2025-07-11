from django.views.generic import ListView


from ..models import Release


class ReleaseListView(ListView):
    model = Release
    template_name = "alibrary/release/list.html"
