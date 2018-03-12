from alibrary.models import Media
from alibrary.util.relations import relations_for_object
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden
from easy_thumbnails.files import get_thumbnailer
from sendfile import sendfile
from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from haystack.backends import SQ
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery


THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


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



    def build_filters(self, filters=None):
        """ Enable querying by fingerprint """
        if filters is None:
            filters = {}

        orm_filters = super(MediaResource, self).build_filters(filters)

        if "code" in filters:
            # re-implement fprint based lookups
            pass

        return orm_filters


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

            # haystack version
            #sqs = SearchQuerySet().models(Media).filter(SQ(content__contains=q) | SQ(content_auto=q))
            sqs = SearchQuerySet().models(Media).filter(content=AutoQuery(q))
            qs = Media.objects.filter(id__in=[result.object.pk for result in sqs]).distinct()

            # ORM version
            #qs = Media.objects.order_by('name').filter(name__icontains=q)

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
        format = get_format(obj, wait=True)

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
                'uuid': obj.uuid,
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
