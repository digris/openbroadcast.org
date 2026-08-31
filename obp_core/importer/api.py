from django.conf.urls import url
from django.http import HttpResponse
from importer.models import Import, ImportFile
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash


class ImportFileResource(ModelResource):
    import_session = fields.ForeignKey(
        "importer.api.ImportResource", "import_session", null=True, full=False
    )

    media = fields.ForeignKey(
        "alibrary.api.MediaResource",
        "media",
        null=True,
        full=False,
        readonly=True,
        full_detail=False,
        full_list=False,
    )

    class Meta:
        queryset = ImportFile.objects.all()
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "post", "put", "delete"]
        resource_name = "importfile"
        excludes = ["type"]
        authentication = SessionAuthentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            "import_session": ALL_WITH_RELATIONS,
            "created": ["exact", "range", "gt", "gte", "lt", "lte"],
            "import_session__uuid_key": ["exact"],
        }

    def dehydrate(self, bundle):
        bundle.data["status"] = bundle.obj.get_status_display().lower()
        bundle.data["media"] = self._dehydrate_media(bundle.obj.media)
        return bundle

    def _dehydrate_media(self, media):
        if not media:
            return None

        return {
            "id": media.pk,
            "uuid": str(media.uuid),
            "resource_uri": self._safe_api_url(media),
            "absolute_url": self._safe_absolute_url(media),
            "name": media.name,
            "created": media.created,
            "artist": self._dehydrate_artist(media.artist),
            "release": self._dehydrate_release(media.release),
        }

    def _dehydrate_artist(self, artist):
        if not artist:
            return None

        return {
            "id": artist.pk,
            "uuid": str(artist.uuid),
            "absolute_url": self._safe_absolute_url(artist),
            "name": artist.name,
        }

    def _dehydrate_release(self, release):
        if not release:
            return None

        return {
            "id": release.pk,
            "uuid": str(release.uuid),
            "absolute_url": self._safe_absolute_url(release),
            "name": release.name,
            "main_image": self._safe_file_url(release.main_image),
        }

    def _safe_absolute_url(self, obj):
        try:
            return obj.get_absolute_url()
        except Exception:
            return None

    def _safe_api_url(self, obj):
        try:
            return obj.get_api_url()
        except Exception:
            return None

    def _safe_file_url(self, file_field):
        try:
            if file_field:
                return file_field.url
        except Exception:
            pass
        return None

    def deserialize(self, request, data, format=None):
        content_type = request.META.get("CONTENT_TYPE", "")
        if content_type.startswith("multipart/form-data"):
            return request.POST.copy()
        return super().deserialize(request, data, format=format)

    def obj_update(self, bundle, **kwargs):
        return super().obj_update(bundle, **kwargs)

    def obj_create(self, bundle, **kwargs):
        request = bundle.request
        """
        ugly hack to play with jquery fileupload
        """
        print(request)
        # print(request.__dict__)
        print("obj_create")
        try:
            import_id = request.GET.get("import_session", None)
            uuid_key = request.GET.get("import_session__uuid_key", None)

            if import_id:
                imp = Import.objects.get(pk=import_id)
                bundle.data["import_session"] = imp

            elif uuid_key:
                imp, created = Import.objects.get_or_create(
                    uuid_key=uuid_key, user=request.user
                )
                bundle.data["import_session"] = imp

            else:
                bundle.data["import_session"] = None

            print("---")
            # print(request.FILES)

            bundle.data["file"] = request.FILES["files[]"]

        except Exception as e:
            print(e)

        return super().obj_create(bundle, **kwargs)


class ImportResource(ModelResource):
    files = fields.ToManyField(
        "importer.api.ImportFileResource", "files", full=True, null=True
    )

    class Meta:
        queryset = Import.objects.all()
        list_allowed_methods = ["get", "post"]
        detail_allowed_methods = ["get", "post", "put", "delete"]
        resource_name = "import"
        excludes = ["updated"]
        include_absolute_url = True
        authentication = SessionAuthentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            "created": ["exact", "range", "gt", "gte", "lt", "lte"],
            "uuid_key": ["exact"],
        }

    def dehydrate(self, bundle):
        bundle.data["inserts"] = bundle.obj.get_inserts()
        return bundle

    def save_related(self, obj):
        return True

    def prepend_urls(self):

        return [
            url(
                r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/import-all%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view("import_all"),
                name="importer_api_import_all",
            ),
            url(
                r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/apply-to-all%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view("apply_to_all"),
                name="importer_api_apply_to_all",
            ),
            url(
                r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/retry-pending%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view("retry_pending"),
                name="importer_api_retry_pending",
            ),
        ]

    def import_all(self, request, **kwargs):

        self.method_check(request, allowed=["get"])
        self.is_authenticated(request)
        self.throttle_check(request)

        import_session = Import.objects.get(**self.remove_api_resource_names(kwargs))
        import_files = import_session.files.filter(
            status=2, import_session=import_session
        )

        for import_file in import_files:
            import_file.status = 6
            import_file.save()

        bundle = self.build_bundle(obj=import_session, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    """
    mass aply import tag
    """

    def apply_to_all(self, request, **kwargs):

        self.method_check(request, allowed=["post"])
        self.is_authenticated(request)
        self.throttle_check(request)

        import_session = Import.objects.get(**self.remove_api_resource_names(kwargs))

        item_id = request.POST.get("item_id", None)
        ct = request.POST.get("ct", None)

        if not (ct and item_id):
            raise ImmediateHttpResponse(response=HttpResponse(status=410))

        import_files = import_session.files.filter(
            status__in=(2, 4), import_session=import_session
        )
        source = import_files.filter(pk=item_id)
        # exclude current one
        import_files = import_files.exclude(pk=item_id)

        try:
            source = source[0]
        except BaseException:
            source = None

        if source:
            sit = source.import_tag
            for import_file in import_files:
                dit = import_file.import_tag

                if ct == "artist":
                    map = (
                        "artist",
                        "alibrary_artist_id",
                        "mb_artist_id",
                        "force_artist",
                    )

                if ct == "release":
                    map = (
                        "release",
                        "alibrary_release_id",
                        "mb_release_id",
                        "force_release",
                    )

                for key in map:
                    src = sit.get(key, None)
                    if src:
                        dit[key] = src
                    else:
                        dit.pop(key, None)

                import_file.import_tag = dit
                # TODO: investigate effect of "skip_apply_import_tag"
                import_file.save(skip_apply_import_tag=True)

        bundle = self.build_bundle(obj=import_session, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    def retry_pending(self, request, **kwargs):

        self.method_check(request, allowed=["post"])
        self.is_authenticated(request)
        self.throttle_check(request)

        import_session = Import.objects.get(**self.remove_api_resource_names(kwargs))
        import_files = import_session.files.filter(
            status=0, import_session=import_session
        )

        for import_file in import_files:
            import_file.status = 3
            import_file.save()

        bundle = {"count": import_files.count()}

        self.log_throttled_access(request)
        return self.create_response(request, bundle)
