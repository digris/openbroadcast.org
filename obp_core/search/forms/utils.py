import sys

from collections import namedtuple
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy


if sys.version_info[0] == 3:
    string_types = (str,)
else:
    string_types = (basestring,)


ModelData = namedtuple("ModelData", ["model_class", "url"])


def get_model_class(ctype):
    """
    `ctype` can either be in string notation "alibrary.models" or a model class
    """

    if isinstance(ctype, string_types):
        model_class = apps.get_model(*ctype.split("."))
    else:
        model_class = ctype

    return model_class


def get_model_data(ctype):

    model_class = get_model_class(ctype)
    model_ct = ContentType.objects.get_for_model(model_class)

    url = reverse_lazy(
        "api:search-by-ctype",
        kwargs={"ct": f"{model_ct.app_label}.{model_ct.model}"},
    )

    d = ModelData(model_class=model_class, url=url)

    return d
