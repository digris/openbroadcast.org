from sendfile import sendfile
from django.conf import settings
from django.conf.urls import *
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from tastypie import fields
from tastypie.authentication import *
from tastypie.authorization import *
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.cache import SimpleCache

from easy_thumbnails.files import get_thumbnailer

from alibrary.models import Media
from alibrary.util.relations import relations_for_object

from ep.API import fp

THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


#from tastypie.contrib.specifiedfields import SpecifiedFields


class MediaResource(ModelResource):

    release = fields.ForeignKey('alibrary.api.ReleaseResource', 'release', null=True, full=True, max_depth=2)
    artist = fields.ForeignKey('alibrary.api.ArtistResource', 'artist', null=True, full=True, max_depth=2)
    message = fields.CharField(attribute='message', null=True)

    class Meta:
        queryset = Media.objects.order_by('tracknumber').all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'library/track'
        detail_uri_name = 'uuid'
        excludes = ['updated', 'release__media']
        include_absolute_url = True
        authentication = MultiAuthentication(ApiKeyAuthentication(), SessionAuthentication(), Authentication())
        authorization = Authorization()
        limit = 50
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'id': ['exact', 'in'],
        }
        #cache = SimpleCache(timeout=600)


    def apply_sorting(self, obj_list, options=None):

        sorting = options.get('id__in', None)
        if not sorting:
            return obj_list

        obj_list_sorted = list()
        for pk in sorting.split(','):
            obj_list_sorted.append(obj_list.get(pk=int(pk)))

        return obj_list_sorted


    def dehydrate(self, bundle):

        obj = bundle.obj


        if obj.master:
            stream = {
                'uri': reverse_lazy('mediaasset-format', kwargs={
                    'media_uuid': bundle.obj.uuid,
                    'quality': 'default',
                    'encoding': 'mp3',
                }),
            }
        else:
            stream = None

        bundle.data['stream'] = stream
        bundle.data['duration'] = bundle.obj.get_duration()
        bundle.data['waveform_image'] = reverse_lazy('mediaasset-waveform', kwargs={'media_uuid': bundle.obj.uuid, 'type': 'w'})
        bundle.data['spectrogram_image'] = reverse_lazy('mediaasset-waveform', kwargs={'media_uuid': bundle.obj.uuid, 'type': 's'})

        bundle.data['relations'] = relations_for_object(bundle.obj)

        # TODO: find a nicer way - disable ops-cache
        obj = Media.objects.filter(pk=obj.pk).nocache()[0]

        # votes
        try:
            user_vote = obj.votes.filter(user=bundle.request.user)[0].vote
        except (TypeError, IndexError) as e:
            user_vote = None

        try:
            votes = {
                'up': obj.total_upvotes,
                'down': obj.total_downvotes,
                'total': obj.vote_total,
                'user': user_vote,
            }
        except AttributeError as e:
            votes = None
        bundle.data['votes'] = votes


        """
        count playlist usage - #914
        """
        bundle.data['playlist_usage'] = len(bundle.obj.get_appearances())

        bundle.data['bitrate'] = bundle.obj.bitrate

        bundle.data['tags'] = [tag.name for tag in bundle.obj.tags]


        """
        TODO: verry hackish and incomplete imnplementation.
        label includes are needed for on-air app. should be built more flexible in the future!
        """
        if bundle.request.GET.get('includes', None):
            includes = bundle.request.GET['includes'].split(',')
            if 'label' in includes:
                try:
                    from alibrary.api.labelapi import LabelResource
                    label = bundle.obj.release.label
                    label_bundle = LabelResource().build_bundle(obj=label, request=bundle.request)
                    label_resource = LabelResource().full_dehydrate(label_bundle)
                except:
                    label_resource = None


                bundle.data['label'] = label_resource




        return bundle


    """
    Filters
    Enable querying by fingerprint
    """

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(MediaResource, self).build_filters(filters)

        if "code" in filters:

            print 'CODE FILTER!!!'

            ids = []
            code = filters['code']

            # code = "eJyFmGFyLSkIhbckoALLUYH9L2GO99XUncpUfH--JNptIxxA0xqdag9ke4CZXujxgu4XvL2w1gNC_QU-D_QmL_B4Ye4XfDxAoS9UPMCaL6zzQvID0uoFni_IfqBfgfyOYS_seuEa_iso7AHmfGH0F_S8sNoL214ofUCavSD-Qt8vlD3QmV849gCd8ULNB7jTCyYvvKNw1gPSxgtXtr9D9IFu-4WjD9DOF2K9kPUAd3nhL_XZX_iE8TdIOy9wvVDjgX4f-RUU-ULJA-zrhd1e-Dj7N_yll8kLnfwBinih2gOs9oI_ceYLtR4Q5NLv6GwvvPPomSm3uz_wF2_UC29vZD4g17Rf0Ru_cPP0F6w0tTTeOYee3dbuNRivma44vdZANtGa3HW5dRP3WTOqxprSSFDDbXuWkRl5p2nQ6mSUJCXp6TL3PNY9SudY2_dE58Zq5bK8K9fAUkzV5-hk-Mhw47mTd-fwtVkHw0rxSsfXko-c4IlHs3mklLriS21iOZwYpm5mPue4s_Q1HY0xdK1xJg3CGhHCF3b6aDGJl9FaanBFjo7V-qJhI1rvB9tvsnLHOjhq8vaavWQuZnxybCEO3nBS3zyIczTG7s2xnXl4c_bzRWLB-DH2BWxGTYNI4ELv3Sdcx7OndZKhe-vUglsHJYni7FojuOkyCMOP3jc8kzZ6Juxny8yRH7lPDPpkWjvaUZ258T0Sn7FWzX10NARm-qHTjBGKPWil11BpiwIHUh1zLzupQ4YX49Vuqej7EYgmnut6ihGBLXEmks_ERFW7cd8YLhjtkm2mbCneelSSGRJRM-ypsimsX2NjDG_OLpCW3-1xO_ibJnYMFS_fuUkJUoVooCOeAnES9LS_yOr_G_sCAT8axW3uW54Szl7ITKWoNeHPI4kNQufjtCVTMszZDEYfHgtn994p4YzDMuC14ataGp4k-AJaObmRrNdyDxf4VO9dgrmoSM-oQ4p4YHG43eAIpO5CreszHZJejBXbZnJl8xastAo-wzHKGAkB_Qy4TpCie1ENOIdtnW1YvKoRkoeWhpKTsjSsCcPWhrkN2q9CuBKKEBg00RU6fJEwmkWxQyVaYtERByyGXDDInqt3rHxu1FscKAJRNdiKiIXrmWOU8lCLsF1feLZsP8a-2Lqa_FFh94QX4OKY4lCIITu7b4e_8zZUFCFGf-O8t5uYyDT8WYRD2ph9hAfurXMgo3E3CuiTGiw7tSng0rZa0NzaG3yfeZwmp9hop_o-AR3KHGbTEzmYV8VwK-4zhA1EIAr-qXrRBt7TPhBr6ljl-nIICc0mWgiSIqS-GNcZ7OemRKjBKycnrx51rGBvxm7IzKDdkHy4JVZ2LKG3KrlVEYzZfdayWV-45V4_xr5AiBB7GOqI4RlIuOFqK9HVlZ1zK3JIy5ajbM8VeyHtAw6E-AIu6ltHDyNq1BcK2YEIba5EGR8lfmxsQy2KvkX3iGrbUYTQKRjqpp6wtoseum-jTmIaphRSvbvObR2z5megKkBCLScux-h0CcWNg0rmKBlIah0buYGGEVl5DlwDWYegiBI6C6ScTNlMkdeCM9ZE8ToOC1C0BmqOKmoRkqR91rtyGLFLdJ1z773_gg7C_mPsizaX5kLwUZ_ufQlVbG2Z7Mh37w1dYC_R7oTSgM5gyDD86pCmioTdGAR6SHUKRrF1C-y3rXXrjlhCj3MJ8u9mOT6zXQoK1PvfAmQzRGsbXff-M4Qp9qibA734dLRphEJrGqNn3YYPGfVczuNOoSPshC2EPSNm-UXd5vdj7D9wtFHDTlhR_NEiES38RPnL0zWQDkh4BMFVjDLxdb_9Db1yMpIyIJGO2ml7dB4nJuo81pqQ12dx3GZC0EB5QlUQtxREtftATZ2mECbK-XJsP-jUGeZ-fIwhFTglIKXRB7EEMmkGB3adiqdQAxJveuIYEg3dQw0JdO0hOFxT5JbRBfOhcNQKmV_4zPVz7AtEkJGSt9vJGijfiW8W4o4aMRwyO7AD7bM6zhqaSBRG6_nz2o_ZQLvVmyOMMMGOO4uQJyVO4vGdrcV1GubGZ9YQcP7MKpIoP7Mbxwt0vo3I31l4uPTe1wINAZ-6K0OIKGHor__5xucNnKJw4rzLozIe5Bf62Befvf0Y--Ify8EFSw=="
            res = fp.best_match_for_query(code_string=code, elbow=10)
            #res = fp.query_fp(code_string=code)

            print 'RREESS!!!'

            try:
                if res.match():
                    print res.match()
                    ids = [int(res.TRID), ]

                    orm_filters["pk__in"] = ids

                else:
                    orm_filters["pk__in"] = ()
            except Exception, e:
                print '****************'
                print e
                print '****************'
                pass

        return orm_filters


    # additional methods
    def prepend_urls(self):

        return [
              url(r"^(?P<resource_name>%s)/autocomplete%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('autocomplete'), name="alibrary-media_api-autocomplete"),
              url(r"^(?P<resource_name>%s)/(?P<uuid>\w[\w/-]*)/vote%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('vote'), name="alibrary-media_api-vote"),
              url(r"^(?P<resource_name>%s)/(?P<uuid>\w[\w/-]*)/stats%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('stats'), name="alibrary-media_api-stats"),
              url(r"^(?P<resource_name>%s)/(?P<uuid>\w[\w/-]*)/stream.mp3$" % self._meta.resource_name, self.wrap_view('stream_file'), name="alibrary-media_api-stream"),
        ]

    def autocomplete(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.throttle_check(request)

        q = request.GET.get('q', None)
        result = []
        object_list = []
        objects = []
        object_count = 0

        qs = None

        if q and len(q) > 1:
            qs = Media.objects.order_by('name').filter(name__icontains=q)
            #qs = Media.objects.order_by('name').filter(Q(name__istartswith=q)\
            #    | Q(artist__name__icontains=q)\
            #    | Q(release__name__icontains=q))



            object_list = qs.distinct()[0:50]
            object_count = qs.distinct().count()

            for result in object_list:
                bundle = self.build_bundle(obj=result, request=request)
                bundle = self.autocomplete_dehydrate(bundle, q)
                objects.append(bundle)


        data = {
            'meta': {
                     'query': q,
                     'total_count': object_count
                     },
            'objects': objects,
        }



        self.log_throttled_access(request)
        return self.create_response(request, data)



    def autocomplete_dehydrate(self, bundle, q):

        bundle.data['name'] = bundle.obj.name
        bundle.data['id'] = bundle.obj.pk
        bundle.data['ct'] = 'media'
        bundle.data['get_absolute_url'] = bundle.obj.get_absolute_url()
        bundle.data['resource_uri'] = bundle.obj.get_api_url()
        bundle.data['main_image'] = None
        bundle.data['duration'] = bundle.obj.get_duration()
        try:
            bundle.data['artist'] = bundle.obj.artist.name
        except:
            bundle.data['artist'] = None
        try:
            bundle.data['release'] = bundle.obj.release.name
        except:
            bundle.data['release'] = None
        try:
            opt = THUMBNAIL_OPT
            main_image = get_thumbnailer(bundle.obj.release.main_image).get_thumbnail(opt)
            bundle.data['main_image'] = main_image.url
        except:
            pass

        return bundle


    def vote(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        obj = Media.objects.get(**self.remove_api_resource_names(kwargs))

        # votes
        try:
            user_vote = obj.votes.filter(user=request.user)[0].vote
        except (TypeError, IndexError) as e:
            user_vote = None

        votes = {
            'up': obj.total_upvotes,
            'down': obj.total_downvotes,
            'total': obj.vote_total,
            'user': user_vote,
        }

        self.log_throttled_access(request)
        return self.create_response(request, votes)


    def stats(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        #self.is_authenticated(request)
        self.throttle_check(request)

        obj = Media.objects.get(**self.remove_api_resource_names(kwargs))

        from statistics.util import ObjectStatistics
        ostats = ObjectStatistics(obj=obj)
        stats = ostats.generate()

        self.log_throttled_access(request)
        return self.create_response(request, stats)


    def stream_file(self, request, **kwargs):
        """
        provides the default stream file as download.
        method is only used by API clients (radio website) at the moment
        """

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if not(request.user.has_perm('alibrary.play_media')):
            return HttpResponseForbidden('sorry. no permissions here!')

        obj = Media.objects.get(**self.remove_api_resource_names(kwargs))


        from media_asset.util import get_format


        #file = obj.get_cache_file('mp3', 'base')

        format = get_format(obj, wait=True)
        # format_file = open(format.path, "rb").read()
        #
        # if not format_file:
        #     return HttpResponseBadRequest('unable to get file')

        return sendfile(request, format.path)



class SimpleMediaResource(ModelResource):

    class Meta:
        queryset = Media.objects.order_by('tracknumber').all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        # not so nice - force resource to full version
        resource_name = 'library/simpletrack'
        detail_uri_name = 'uuid'
        excludes = ['updated', 'release__media']
        include_absolute_url = True
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'id': ['exact', 'in'],
        }

    def apply_sorting(self, obj_list, options=None):

        sorting = options.get('id__in', None)
        if not sorting:
            return obj_list

        obj_list_sorted = list()
        for pk in sorting.split(','):
            obj_list_sorted.append(obj_list.get(pk=int(pk)))

        return obj_list_sorted

    def dehydrate(self, bundle):

        obj = bundle.obj

        if obj.master:
            stream = {
                #'rtmp_app': '%s' % settings.RTMP_APP,
                #'rtmp_host': 'rtmp://%s:%s/' % (settings.RTMP_HOST, settings.RTMP_PORT),
                #'file': obj.master,
                'uuid': obj.uuid,
                #'uri': obj.get_stream_url(),
                'uri': reverse_lazy('mediaasset-format', kwargs={
                    'media_uuid': bundle.obj.uuid,
                    'quality': 'default',
                    'encoding': 'mp3',
                }),
            }
        else:
            stream = None

        bundle.data['stream'] = stream
        bundle.data['duration'] = bundle.obj.get_duration()
        bundle.data['waveform_image'] = reverse_lazy('mediaasset-waveform', kwargs={'media_uuid': bundle.obj.uuid, 'type': 'w'})
        bundle.data['spectrogram_image'] = reverse_lazy('mediaasset-waveform', kwargs={'media_uuid': bundle.obj.uuid, 'type': 's'})


        return bundle