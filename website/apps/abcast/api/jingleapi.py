from abcast.models import Jingle, JingleSet
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class JingleResource(ModelResource):
    set = fields.ForeignKey('abcast.api.JingleSetResource', 'set', null=True, full=True, max_depth=2)

    class Meta:
        queryset = Jingle.objects.order_by('name').all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'abcast/jingle'
        excludes = ['updated', ]
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def dehydrate(self, bundle):

        obj = bundle.obj

        if obj.master:
            stream = {
                'rtmp_app': '%s' % settings.RTMP_APP,
                'rtmp_host': 'rtmp://%s:%s/' % (settings.RTMP_HOST, settings.RTMP_PORT),
                'file': obj.master,
                'uuid': obj.uuid,
                'uri': obj.master.url,
            }
        else:
            stream = None

        bundle.data['stream'] = stream
        bundle.data['waveform_image'] = None
        try:
            waveform_image = bundle.obj.get_waveform_image()
            if waveform_image:
                bundle.data['waveform_image'] = bundle.obj.get_waveform_url()

        except Exception as e:
            pass

        return bundle


class JingleSetResource(ModelResource):
    jingles = fields.ToManyField('abcast.api.JingleResource', 'jingle_set', null=True, full=True, max_depth=2)

    class Meta:
        queryset = JingleSet.objects.order_by('name').all()
        list_allowed_methods = ['get', ]
        detail_allowed_methods = ['get', ]
        resource_name = 'abcast/jingleset'
        excludes = ['updated', ]
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def dehydrate(self, bundle):

        bundle.data['main_image'] = None

        if bundle.obj.main_image:
            opt = dict(size=(70, 70), crop=True, bw=False, quality=80)
            try:
                main_image = get_thumbnailer(bundle.obj.main_image).get_thumbnail(opt)
                bundle.data['main_image'] = main_image.url
            except:
                pass

        return bundle
