from alibrary.models import Label
from django.conf.urls import url
from easy_thumbnails.files import get_thumbnailer
from tastypie.authentication import (
    MultiAuthentication,
    SessionAuthentication,
    ApiKeyAuthentication,
)
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


class LabelResource(ModelResource):
    class Meta:
        queryset = Label.objects.all()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        resource_name = "library/label"
        excludes = ["updated"]
        include_absolute_url = True
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication()
        )
        authorization = Authorization()
        filtering = {
            "created": ["exact", "range", "gt", "gte", "lt", "lte"],
            "id": ["exact", "in"],
        }
        cache = SimpleCache(timeout=120)

    def dehydrate(self, bundle):

        if bundle.obj.main_image:
            bundle.data["main_image"] = None
            try:
                opt = THUMBNAIL_OPT
                main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
                bundle.data["main_image"] = main_image.url
            except:
                pass

        bundle.data["release_count"] = bundle.obj.release_label.count()
        bundle.data["type_display"] = bundle.obj.get_type_display()

        bundle.data["tags"] = [tag.name for tag in bundle.obj.tags]

        return bundle
