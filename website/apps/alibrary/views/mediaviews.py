import os

from django.views.generic import DetailView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.contrib import messages

from tagging.models import Tag
import reversion
from sendfile import sendfile
import audiotranscode

from pure_pagination.mixins import PaginationMixin
from braces.views import PermissionRequiredMixin, LoginRequiredMixin

from alibrary.models import Media, Playlist, PlaylistItem, Artist, Release
from alibrary.forms import MediaForm, MediaActionForm, MediaRelationFormSet, ExtraartistFormSet
from alibrary.filters import MediaFilter

from lib.util import tagging_extra
from lib.util import change_message
from lib.util.form_errors import merge_form_errors

import logging
log = logging.getLogger(__name__)

ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12,24,36,120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)

ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'base_duration',
        'name': _('Duration')
    },
    {
        'key': 'tempo',
        'name': _('BPM')
    },
    {
        'key': 'danceability',
        'name': _('Danceability')
    },
    {
        'key': 'energy',
        'name': _('Energy')
    },
    {
        'key': 'updated',
        'name': _('Last modified')
    },
    {
        'key': 'created',
        'name': _('Creation date')
    },
]

class MediaListView(PaginationMixin, ListView):

    object = Media
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
    
    model = Media
    extra_context = {}
    
    def get_paginate_by(self, queryset):
        
        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in ALIBRARY_PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(MediaListView, self).get_context_data(**kwargs)
        
        self.extra_context['filter'] = self.filter
        self.extra_context['relation_filter'] = self.relation_filter
        self.extra_context['tagcloud'] = self.tagcloud
        # for the ordering-box
        self.extra_context['order_by'] = ORDER_BY

        # active tags
        if self.request.GET.get('tags', None):
            tag_ids = []
            for tag_id in self.request.GET['tags'].split(','):
                tag_ids.append(int(tag_id))
            self.extra_context['active_tags'] = tag_ids

        self.extra_context['list_style'] = self.request.GET.get('list_style', 's')
        self.extra_context['get'] = self.request.GET
        context.update(self.extra_context)

        return context
    

    def get_queryset(self, **kwargs):

        kwargs = {}
        self.tagcloud = None
        q = self.request.GET.get('q', None)
        
        if q:
            qs = Media.objects.filter(Q(name__icontains=q)\
            | Q(release__name__icontains=q)\
            | Q(artist__name__icontains=q))\
            .distinct()
        else:
            qs = Media.objects.all()
            
            
        order_by = self.request.GET.get('order_by', 'created')
        direction = self.request.GET.get('direction', 'descending')
        
        if order_by and direction:
            if direction == 'descending':
                qs = qs.order_by('-%s' % order_by)
            else:
                qs = qs.order_by('%s' % order_by)

            
        # special relation filters
        self.relation_filter = []
        
        artist_filter = self.request.GET.get('artist', None)
        if artist_filter:
            qs = qs.filter(artist__slug=artist_filter).distinct()
            fa = Artist.objects.filter(slug=artist_filter)[0]
            f = {'item_type': 'artist' , 'item': fa, 'label': _('Artist')}
            self.relation_filter.append(f)
            
        release_filter = self.request.GET.get('release', None)
        if release_filter:
            qs = qs.filter(release__slug=release_filter).distinct()
            fa = Release.objects.filter(slug=release_filter)[0]
            f = {'item_type': 'release' , 'item': fa, 'label': _('Release')}
            self.relation_filter.append(f)
            
        # filter by import session
        import_session = self.request.GET.get('import', None)
        if import_session:
            from importer.models import Import
            from django.contrib.contenttypes.models import ContentType
            import_session = get_object_or_404(Import, pk=int(import_session))
            ctype = ContentType.objects.get(model='media')
            ids = import_session.importitem_set.filter(content_type=ctype.pk).values_list('object_id',)
            qs = qs.filter(pk__in=ids).distinct()

        # filter by user
        creator_filter = self.request.GET.get('creator', None)
        if creator_filter:
            from django.contrib.auth.models import User
            creator = get_object_or_404(User, username='%s' % creator_filter)
            qs = qs.filter(creator=creator).distinct()
            f = {'item_type': 'release' , 'item': creator, 'label': _('Added by')}
            self.relation_filter.append(f)


        # "extra-filters" (to provide some arbitary searches)
        extra_filter = self.request.GET.get('extra_filter', None)
        if extra_filter:
            if extra_filter == 'unassigned':
                qs = qs.filter(release=None).distinct()

        
        # apply filters
        self.filter = MediaFilter(self.request.GET, queryset=qs)
        # self.filter = ReleaseFilter(self.request.GET, queryset=Release.objects.active().filter(**kwargs))
        qs = self.filter.qs
        
        
        
        
        stags = self.request.GET.get('tags', None)
        tstags = []
        if stags:
            stags = stags.split(',')
            for stag in stags:
                #print int(stag)
                tstags.append(int(stag))

        if stags:
            qs = Media.tagged.with_all(tstags, qs)
            
            
        # rebuild filter after applying tags
        self.filter = MediaFilter(self.request.GET, queryset=qs)
        

        tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=0)
        self.tagcloud = tagging_extra.calculate_cloud(tagcloud)

        return qs
    

class MediaDetailView(DetailView):

    model = Media
    extra_context = {}

    def get_context_data(self, **kwargs):
        
        context = super(MediaDetailView, self).get_context_data(**kwargs)
        obj = kwargs.get('object', None)

        self.extra_context['history'] = reversion.get_unique_for_object(obj)
        
        # foreign appearance
        ps = []
        try:
            pis = PlaylistItem.objects.filter(object_id=obj.id, content_type=ContentType.objects.get_for_model(obj))
            ps = Playlist.objects.exclude(type='basket').filter(items__in=pis)
        except:
            pass
        
        self.extra_context['appearance'] = ps
        context.update(self.extra_context)
        
        return context
    



class MediaEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Media
    form_class = MediaForm
    template_name = "alibrary/media_edit.html"
    permission_required = 'alibrary.change_media'
    raise_exception = True
    success_url = '#'

    def __init__(self, *args, **kwargs):
        super(MediaEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update({ 'user': self.request.user })
        return self.initial

    def get_context_data(self, **kwargs):
        ctx = super(MediaEditView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        # TODO: is this a good way to pass the instance main form?
        ctx['form_errors'] = self.get_form_errors(form=ctx['form'])

        return ctx

    def get_named_formsets(self):

        return {
            'action': MediaActionForm(self.request.POST or None, prefix='action'),
            'relation': MediaRelationFormSet(self.request.POST or None, instance=self.object, prefix='relation'),
            'extraartist': ExtraartistFormSet(self.request.POST or None, instance=self.object, prefix='extraartist'),
        }

    def get_form_errors(self, form=None):

        named_formsets = self.get_named_formsets()
        named_formsets.update({'form': form})
        form_errors = merge_form_errors([formset for name, formset in named_formsets.items()])

        return form_errors

    def form_valid(self, form):

        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save(commit=False)

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        msg = change_message.construct(self.request, form, [named_formsets['relation'], named_formsets['extraartist'],])

        d_tags = form.cleaned_data['d_tags']
        if d_tags:
            msg = change_message.parse_tags(obj=self.object, d_tags=d_tags, msg=msg)
            self.object.tags = d_tags

        with reversion.create_revision():
            self.object = form.save()
            reversion.set_user(self.request.user)
            reversion.set_comment(msg)

        messages.add_message(self.request, messages.INFO, msg)

        return HttpResponseRedirect('')

    def formset_relation_valid(self, formset):

        relations = formset.save(commit=False) # self.save_formset(formset, contact)
        for relation in relations:
            #relation.who = self.request.user
            #relation.contact = self.object
            relation.save()





    

@never_cache
def media_download(request, slug, format, version):
    
    media = get_object_or_404(Media, slug=slug)
    version = 'base' 


    download_permission = False
    #for product in media.mediaproduct.filter(active=True): # users who purchase hardware can download the software part as well
    #    if get_download_permissions(request, product, format, version):
    #        download_permission = True
    #    if product.unit_price == 0:
    #        download_permission = True
    
    if not download_permission:
        return HttpResponseForbidden('forbidden')
    
    if format in ['mp3', 'flac', 'wav']:
        cache_file = media.get_cache_file(format, version).path
    else:
        raise Http404
    
    
    filename = '%02d %s - %s' % (media.tracknumber, media.name.encode('ascii', 'ignore'), media.artist.name.encode('ascii', 'ignore'))
    
    filename = '%s.%s' % (filename, format)
    
    return sendfile(request, cache_file, attachment=True, attachment_filename=filename)


@never_cache
def stream_html5(request, uuid):
    
    media = get_object_or_404(Media, uuid=uuid)

    print 'requested to stream: %s' % media.pk

    stream_permission = False

    if request.user and request.user.has_perm('alibrary.play_media'):
    #if request.user.is_authenticated():
        stream_permission = True

    # check if unrestricted license
    if not stream_permission:
        if media.license and media.license.restricted == False:
            stream_permission = True

    # TODO: IMPLEMENT PERMISSION CHECK FOR PYPO!!!!!!!!!!!!!
    print request.META['HTTP_HOST']
    print request.META['HTTP_USER_AGENT']
    stream_permission = True

    if not stream_permission:
        log.warning('unauthorized attempt by "%s" to download: %s - "%s"' % (request.user.username if request.user else 'unknown', media.pk, media.name))
        raise PermissionDenied
    
    try:
        from atracker.util import create_event
        create_event(request.user, media, None, 'stream')
    except:
        pass

    media_file = media.get_cache_file('mp3', 'base')

    if not media_file:
        return HttpResponseBadRequest('unable to get cache file')

    return sendfile(request, media_file)


def __encode(path, bitrate, format):
    at = audiotranscode.AudioTranscode()
    for data in at.transcode_stream(path, format, bitrate=bitrate):
        # do something with chuck of data
        # e.g. sendDataToClient(data)
        yield data



@never_cache
def encode(request, uuid, bitrate=128, format='mp3'):

    media = get_object_or_404(Media, uuid=uuid)

    stream_permission = False

    if request.user and request.user.has_perm('alibrary.play_media'):
        stream_permission = True

    # check if unrestricted license
    if not stream_permission:
        if media.license and media.license.restricted == False:
            stream_permission = True

    if not stream_permission:
        raise PermissionDenied

    try:
        from atracker.util import create_event
        create_event(request.user, media, None, 'stream')
    except:
        pass


    return HttpResponse(__encode(media.master.path, bitrate, format), mimetype='audio/mpeg')

    #return sendfile(request, media.get_cache_file('mp3', 'base'))

@never_cache
def waveform(request, uuid):
    
    media = get_object_or_404(Media, uuid=uuid)

    if media.get_cache_file('png', 'waveform'):
        waveform_file = media.get_cache_file('png', 'waveform')
    else:
        waveform_file = os.path.join(settings.STATIC_ROOT, 'img/base/defaults/waveform.png')


    return sendfile(request, waveform_file)