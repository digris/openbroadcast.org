from django.conf.urls.defaults import *
from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.exceptions import ImmediateHttpResponse
from django.http import HttpResponse


from importer.models import Import, ImportFile


# file = request.FILES[u'files[]']



class ImportFileResource(ModelResource):
    
    import_session = fields.ForeignKey('importer.api.ImportResource', 'import_session', null=True, full=False)
    
    media = fields.ForeignKey('alibrary.api.MediaResource', 'media', null=True, full=True)

    class Meta:
        queryset = ImportFile.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete',]
        resource_name = 'importfile'
        # excludes = ['type','results_musicbrainz']
        excludes = ['type',]
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'import_session': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'import_session__uuid_key': ['exact',],
        }
        

    def dehydrate(self, bundle):
        bundle.data['status'] = bundle.obj.get_status_display().lower();
        # offload json parsing to the backend
        # TODO: remove in js, enable here
        """
        bundle.data['import_tag'] = json.loads(bundle.data['import_tag'])
        bundle.data['results_acoustid'] = json.loads(bundle.data['results_acoustid'])
        bundle.data['results_musicbrainz'] = json.loads(bundle.data['results_musicbrainz'])
        bundle.data['results_discogs'] = json.loads(bundle.data['results_discogs'])
        bundle.data['results_tag'] = json.loads(bundle.data['results_tag'])
        """
        return bundle
        
        
    def obj_update(self, bundle, request, **kwargs):
        #import time
        #time.sleep(3)
        return super(ImportFileResource, self).obj_update(bundle, request, **kwargs)
        

    def obj_create(self, bundle, request, **kwargs):
        """
        Little switch to play with jquery fileupload
        """
        try:

            #import_id = request.GET['import_session']
            import_id = request.GET.get('import_session', None)
            #uuid_key = request.GET.get('uuid_key', None)
            uuid_key = request.GET.get('import_session__uuid_key', None)


            print "####################################"
            print request.FILES[u'files[]']

            if import_id:
                imp = Import.objects.get(pk=import_id)
                bundle.data['import_session'] = imp

            elif uuid_key:
                imp, created = Import.objects.get_or_create(uuid_key=uuid_key, user=request.user)
                bundle.data['import_session'] = imp

            else:
                bundle.data['import_session'] = None



            bundle.data['file'] = request.FILES[u'files[]']
            
            
        except Exception, e:
            print e
            
        return super(ImportFileResource, self).obj_create(bundle, request, **kwargs)


class ImportResource(ModelResource):
    
    files = fields.ToManyField('importer.api.ImportFileResource', 'files', full=True, null=True)

    class Meta:
        queryset = Import.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        #list_allowed_methods = ['get',]
        #detail_allowed_methods = ['get',]
        resource_name = 'import'
        excludes = ['updated',]
        include_absolute_url = True
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            #'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'uuid_key': ['exact',],
        }




    def dehydrate(self, bundle):
        bundle.data['inserts'] = bundle.obj.get_inserts();
        return bundle



    def save_related(self, obj):
        return True
    
    
    # additional methods
    def prepend_urls(self):
        
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/import-all%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('import_all'), name="importer_api_import_all"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/apply-to-all%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('apply_to_all'), name="importer_api_apply_to_all"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/retry-pending%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('retry_pending'), name="importer_api_retry_pending"),
        ]

    def import_all(self, request, **kwargs):
        
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        import_session = Import.objects.get(**self.remove_api_resource_names(kwargs))
        import_files = import_session.files.filter(status=2, import_session=import_session)
        
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
        
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        import_session = Import.objects.get(**self.remove_api_resource_names(kwargs))

        item_id = request.POST.get('item_id', None)
        ct = request.POST.get('ct', None)
        
        print 'item_id: %s' % item_id
        print 'ct: %s' % ct
        
        if not (ct and item_id):
            raise ImmediateHttpResponse(response=HttpResponse(status=410))
        
        import_files = import_session.files.filter(status__in=(2,4), import_session=import_session)
        source = import_files.filter(pk=item_id)
        # exclude current one
        import_files = import_files.exclude(pk=item_id)
        
        try:
            source = source[0]
            print 'The source:'
            print source
            # print source.import_tag
        except:
            source = None
        
        
        if source:
            sit = source.import_tag   
            for import_file in import_files:
                dit = import_file.import_tag
                
                if ct == 'artist':
                    map = ('artist', 'alibrary_artist_id', 'mb_artist_id', 'force_artist')
                    
                if ct == 'release':
                    map = ('release', 'alibrary_release_id', 'mb_release_id', 'force_release')
                
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

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        import_session = Import.objects.get(**self.remove_api_resource_names(kwargs))
        import_files = import_session.files.filter(status=0, import_session=import_session)

        for import_file in import_files:
            import_file.status = 3
            import_file.save()


        bundle = {'count': import_files.count()}


        self.log_throttled_access(request)
        return self.create_response(request, bundle)
        

    
    
    

    