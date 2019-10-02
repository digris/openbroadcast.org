import django_filters
from actstream.models import Action
from django.contrib.contenttypes.models import ContentType

ORDER_BY_FIELD = "o"

from django.db import models


class ActionFilter(django_filters.FilterSet):
    class Meta:
        model = Action
        fields = {"verb": ["exact"], "target_content_type": ["exact"]}

    @property
    def filterlist(self):
        flist = []
        if not hasattr(self, "_filterlist"):
            for name, filter_ in self.filters.items():
                qs = (
                    self.queryset.values_list(name, flat=False)
                    .order_by(name)
                    .annotate(n=models.Count("pk", distinct=True))
                    .distinct()
                )
                mapped_qs = []

                if name == "target_content_type":
                    for item in qs:
                        ct_name = ContentType.objects.get(pk=item[0]).name
                        mapped_qs.append((item[0], ct_name, item[1]))
                    mapped_qs.sort(key=lambda tup: tup[0])
                    qs = mapped_qs

                filter_.entries = qs
                if qs not in flist:
                    flist.append(filter_)

            self._filterlist = flist

        return self._filterlist
