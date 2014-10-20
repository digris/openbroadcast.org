from django.utils.html import mark_safe
from easy_thumbnails.files import get_thumbnailer

from selectable.base import ModelLookup
from selectable.registry import registry
from alibrary.models import *

THUMBNAIL_OPT = dict(size=(70, 70), crop=True, bw=False, quality=80)


class ReleaseNameLookup(ModelLookup):
    model = Release
    search_fields = ['name__icontains',]
    
    def get_item_label(self, item):

        name = (item.name[:22] + '..') if len(item.name) > 22 else item.name

        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html += '<span>%s' % name

        if item.catalognumber:
            html += '<small>%s</small>' % item.catalognumber

        html += '</span>'



        return mark_safe(html)
    
registry.register(ReleaseNameLookup)

""""""
class PlaylistSeriesLookup(ModelLookup):
    model = Series
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html = ''
        html += '<span>%s</span>' % item.name

        return mark_safe(html)
    
    
    
registry.register(PlaylistSeriesLookup)



class ReleaseLabelLookup(ModelLookup):
    model = Label
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html += '<span>%s</span>' % item.name

        return mark_safe(html)



registry.register(ReleaseLabelLookup)


class ParentLabelLookup(ReleaseLabelLookup):
    pass

registry.register(ParentLabelLookup)

""""""
class ArtistLookup(ModelLookup):
    model = Artist
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html += '<span>%s</span>' % item.name

        return mark_safe(html)

    
    
    
registry.register(ArtistLookup)


class LabelLookup(ModelLookup):
    model = Label
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        try:
            opt = THUMBNAIL_OPT
            image = image = get_thumbnailer(item.main_image).get_thumbnail(opt).url
        except:
            image = "/static/img/base/spacer.png"
            pass

        html = '<img src="%s">' % image
        html += '<span>%s</span>' % item.name

        return mark_safe(html)
    
registry.register(LabelLookup)


class LicenseLookup(ModelLookup):
    model = License
    search_fields = ['name__icontains',]

    def get_item_label(self, item):
        return mark_safe(u'%s (%s) <span class="%s">%s</span>' % (item.name, item.restricted, item.key, item.key))
    
    
registry.register(LicenseLookup)
