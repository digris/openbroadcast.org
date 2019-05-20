import json

from abcast.api import JingleResource
from abcast.models import Jingle
from alibrary.api import ReleaseResource, MediaResource, SimpleMediaResource
from alibrary.models import Playlist, Media, PlaylistItemPlaylist, PlaylistItem, Daypart
from alibrary.models import Release
from django.conf.urls import url
from django.db.models import Q
from easy_thumbnails.files import get_thumbnailer
from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


class PlaylistItemResource(ModelResource):
    co_to = {
        Release: ReleaseResource,
        Media: SimpleMediaResource,
        Jingle: JingleResource,
    }

    content_object = GenericForeignKeyField(to=co_to, attribute='content_object', null=False, full=True)

    class Meta:
        queryset = PlaylistItem.objects.all()
        excludes = ['id', ]

    def dehydrate(self, bundle):
        bundle.data['content_type'] = '%s' % bundle.obj.content_object.__class__.__name__.lower()
        bundle.data['resource_uri'] = '%s' % bundle.obj.content_object.get_api_url()
        return bundle


class PlaylistItemPlaylistResource(ModelResource):
    item = fields.ToOneField('alibrary.api.PlaylistItemResource', 'item', null=True, full=True)

    class Meta:
        queryset = PlaylistItemPlaylist.objects.all()
        resource_name = 'library/playlistitem'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['put', 'post', 'patch', 'get', 'delete']
        always_return_data = True
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()


class DaypartResource(ModelResource):
    class Meta:
        queryset = Daypart.objects.all()
        excludes = ['id', ]


class PlaylistResource(ModelResource):
    items = fields.ToManyField('alibrary.api.PlaylistItemPlaylistResource',
                               attribute=lambda bundle: bundle.obj.items.through.objects.filter(
                                   playlist=bundle.obj).order_by('position') or bundle.obj.items, null=True, full=True,
                               max_depth=5)

    dayparts = fields.ToManyField('alibrary.api.DaypartResource', 'dayparts', null=True, full=True, max_depth=3)

    class Meta:
        queryset = Playlist.objects.order_by('-created').all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'delete', 'put', 'post', 'patch']
        resource_name = 'library/playlist'
        include_absolute_url = True
        always_return_data = True
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        limit = 50
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'status': ['exact', 'range', ],
            'is_current': ['exact', ],
            'type': ['exact', ],
        }

    def apply_authorization_limits(self, request, object_list):
        if request.GET.get('all', False):
            return object_list
        else:
            return object_list.filter(user=request.user)

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(PlaylistResource, self).obj_create(bundle, request, user=request.user)

        Playlist.objects.filter(user=request.user).update(is_current=False)
        bundle.obj.is_current = True
        bundle.obj.save()
        return bundle

    def obj_delete(self, request=None, **kwargs):
        ret = super(PlaylistResource, self).obj_delete(request, **kwargs)

        try:
            p = Playlist.objects.filter(user=request.user)[0]
            p.is_current = True
            p.save()
        except:
            pass

        return ret

    def dehydrate(self, bundle):
        bundle.data['edit_url'] = bundle.obj.get_edit_url()

        bundle.data['item_count'] = bundle.obj.items.count()

        # somehow needed to get data as json...
        bundle.data['broadcast_status_messages'] = bundle.obj.broadcast_status_messages

        # a bit hackish maybe, provide uuids of all items in playlist
        items = bundle.obj.get_items()
        item_uuids = []
        for item in items:
            item_uuids.append(item.content_object.uuid)
        bundle.data['item_uuids'] = item_uuids

        bundle.data['main_image'] = None
        try:
            opt = THUMBNAIL_OPT
            main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
            bundle.data['main_image'] = main_image.url
        except:
            pass

        bundle.data['series'] = None
        if bundle.obj.series:
            bundle.data['series'] = bundle.obj.series.name

        bundle.data['tags'] = [tag.name for tag in bundle.obj.tags]

        # bundle.data['reorder_url'] = bundle.obj.get_reorder_url();
        return bundle

    """
    def hydrate_m2m(self, bundle):
        print "hydrate m2m"


        #curl --dump-header - -H "Content-Type: application/json" -X PUT --data '{"media": [{"media": "/api/v1/library/track/16587/"}]}' "http://localhost:8080/de/api/v1/library/playlist/58/?username=root&api_key=APIKEY"

        try:
            for item in bundle.data['media']:
                #item[u'media'] = self.get_resource_uri(bundle.obj)
                print item
        except:
            pass

    """

    def save_m2m(self, bundle):
        return bundle

    # additional methods
    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/set-current%s$" % (
            self._meta.resource_name, trailing_slash()), self.wrap_view('set_current'),
                name="playlist_api_set_current"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/reorder%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reorder'), name="playlist_api_reorder"),
            # collecting
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/collect%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('collect_specific'), name="playlist_api_collect_specific"),
            url(r"^(?P<resource_name>%s)/collect%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('collect'), name="playlist_api_collect"),
            # services & hooks
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/mixdown-complete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('mixdown_complete'), name="alibrary-playlist_api-mixdown_complete"),
            # # autocomplete
            # url(r"^(?P<resource_name>%s)/autocomplete%s$" % (self._meta.resource_name, trailing_slash()),
            #     self.wrap_view('autocomplete'), name="alibrary-playlist_api-autocomplete"),
            #
            # # legacy
            # url(r"^(?P<resource_name>%s)/autocomplete-name%s$" % (self._meta.resource_name, trailing_slash()),
            #     self.wrap_view('autocomplete'), name="alibrary-playlist_api-autocomplete"),

        ]

    def set_current(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        Playlist.objects.filter(user=request.user).exclude(**self.remove_api_resource_names(kwargs)).update(
            is_current=False)
        cp = Playlist.objects.get(**self.remove_api_resource_names(kwargs))
        cp.is_current = True
        cp.save()

        bundle = self.build_bundle(obj=cp, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    """
    collect with knowing the target playlist
    """

    def collect_specific(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        p = Playlist.objects.get(**self.remove_api_resource_names(kwargs))

        data = json.loads(request.body)

        ids = data.get('ids', None)
        ct = data.get('ct', None)

        if ids:
            ids = ids.split(',')
            p.add_items_by_ids(ids, ct)

        bundle = self.build_bundle(obj=p, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    """
    collect _without_ knowing the target playlist
    """

    def collect(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            p = Playlist.objects.filter(user=request.user, is_current=True)[0]
        except:
            p = Playlist(user=request.user, is_current=True, name="New Playlist")
            p.save()

        data = json.loads(request.body)

        ids = data.get('ids', None)
        ct = data.get('ct', None)

        if ids:
            ids = ids.split(',')
            p.add_items_by_ids(ids, ct)

        bundle = self.build_bundle(obj=p, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    def reorder(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        p = Playlist.objects.get(**self.remove_api_resource_names(kwargs))

        order = request.POST.get('order', None)

        if order:
            order = order.split(',')
            p.reorder_items_by_uuids(order)

        bundle = self.build_bundle(obj=p, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)



    # services & hooks
    def mixdown_complete(self, request, **kwargs):
        """
        callback from mixdown service.
        triggers download of processed mixdown file
        """

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        p = Playlist.objects.get(**self.remove_api_resource_names(kwargs))

        try:
            p.download_mixdown()
            bundle = {
                'status': True,
            }
        except Exception as e:
            bundle = {
                'status': False,
                'error': '{}'.format(e)
            }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)



class SimplePlaylistResource(ModelResource):
    class Meta:
        # queryset = Playlist.objects.order_by('-created').all()
        queryset = Playlist.objects.order_by('-updated').all().nocache()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'library/simpleplaylist'
        # excludes = ['updated',]
        include_absolute_url = True

        always_return_data = True

        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        limit = 50
        filtering = {
            # 'channel': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'status': ['exact', 'range', ],
            'is_current': ['exact', ],
            'type': ['exact', 'in'],
            'id': ['in', ],
        }

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def dehydrate(self, bundle):
        bundle.data['item_count'] = bundle.obj.items.count();

        # a bit hackish maybe, return uuids of all items in playlist
        items = bundle.obj.get_items()
        item_uuids = []
        for item in items:
            item_uuids.append(item.content_object.uuid)
        bundle.data['item_uuids'] = item_uuids

        return bundle

    # additional methods
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/set-current%s$" % (
            self._meta.resource_name, trailing_slash()), self.wrap_view('set_current'),
                name="playlist_api_set_current"),
        ]

    def set_current(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        Playlist.objects.filter(user=request.user).exclude(**self.remove_api_resource_names(kwargs)).update(
            is_current=False)
        cp = Playlist.objects.get(**self.remove_api_resource_names(kwargs))
        cp.is_current = True
        cp.save()

        bundle = self.build_bundle(obj=cp, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)
