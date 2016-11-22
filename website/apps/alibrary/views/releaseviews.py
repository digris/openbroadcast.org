# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
from datetime import timedelta

import actstream
import reversion
from alibrary.filters import ReleaseFilter
from haystack.backends import SQ
from haystack.query import SearchQuerySet

from ..forms import ReleaseForm, ReleaseActionForm, ReleaseBulkeditForm, ReleaseRelationFormSet, AlbumartistFormSet, ReleaseMediaFormSet
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from django import http
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, UpdateView
from tagging_extra.utils import calculate_cloud
from lib.util.form_errors import merge_form_errors
from base.models.utils.merge import merge_objects
from pure_pagination.mixins import PaginationMixin
from tagging.models import Tag
from ..models import Release, Artist, Label, ReleaseAlbumartists

ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12,24,36,120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)


ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'releasedate',
        'name': _('Releasedate')
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


class ReleaseListView(PaginationMixin, ListView):

    object = Release
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
    model = Release

    extra_context = {}
    
    def get_paginate_by(self, queryset):
        
        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in ALIBRARY_PAGINATE_BY:
                    return int(ipp)
            except Exception as e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super(ReleaseListView, self).get_context_data(**kwargs)

        self.extra_context['filter'] = self.filter
        self.extra_context['special_filters'] = ['releasedate',]
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

        self.extra_context['list_style'] = self.request.GET.get('list_style', 'l')
        self.extra_context['get'] = self.request.GET
        context.update(self.extra_context)

        return context
    

    def get_queryset(self, **kwargs):

        kwargs = {}

        self.tagcloud = None

        q = self.request.GET.get('q', None)





        # haystack version
        if q:
            sqs = SearchQuerySet().models(Release).filter(SQ(content__contains=q) | SQ(name__contains=q))
            qs = Release.objects.filter(id__in=[result.object.pk for result in sqs]).distinct()
        else:
            qs = Release.objects.select_related('license').prefetch_related('media_release').all()



        # if q:
        #     #qs = Release.objects.filter(Q(name__istartswith=q)\
        #     #| Q(media_release__name__icontains=q)\
        #     #| Q(media_release__artist__name__icontains=q)\
        #     #| Q(label__name__icontains=q))\
        #     #.distinct()
        #     qs = Release.objects.filter(name__icontains=q).distinct()
        # else:
        #     qs = Release.objects.select_related('license').prefetch_related('media_release').all()
            
            
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
            #qs = qs.filter(Q(media_release__artist__slug=artist_filter) | Q(media_release__media_artists__slug=artist_filter) | Q(album_artists__slug=artist_filter)).distinct()

            a = get_object_or_404(Artist, slug=artist_filter)
            qs = qs.filter(pk__in=(r.id for r in a.get_releases())).distinct()

            f = {'item_type': 'artist' , 'item': a, 'label': _('Artist')}
            self.relation_filter.append(f)
            
        label_filter = self.request.GET.get('label', None)
        if label_filter:
            l = get_object_or_404(Label, slug=label_filter)
            qs = qs.filter(label__pk=l.pk).distinct()

            f = {'item_type': 'label' , 'item': l, 'label': _('Label')}
            self.relation_filter.append(f)


        # filter by import session
        import_session = self.request.GET.get('import', None)
        if import_session:
            from importer.models import Import
            from django.contrib.contenttypes.models import ContentType
            import_session = get_object_or_404(Import, pk=int(import_session))
            ctype = ContentType.objects.get(model='release')
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

        # filter by user
        creator_exclude_filter = self.request.GET.get('creator_exclude', None)
        if creator_exclude_filter:
            from django.contrib.auth.models import User
            creator = get_object_or_404(User, username='%s' % creator_exclude_filter)
            qs = qs.exclude(creator__id=creator.id).distinct()
            f = {'item_type': 'release' , 'item': creator, 'label': _('Not added by')}
            self.relation_filter.append(f)

        # filter by promo flag
        # TODO: refactor query, publish_date is depreciated
        promo_filter = self.request.GET.get('promo', None)
        if promo_filter and promo_filter.isnumeric() and int(promo_filter) == 1:
            #qs = qs.filter(releasedate__gte=F('publish_date')).distinct()
            qs = qs.filter(releasedate__gt=datetime.datetime.now().date()).distinct()
            f = {'item_type': 'release' , 'item': _('Promotional Releases'), 'label': 'Filter'}
            self.relation_filter.append(f)

        # filter by new flag
        # TODO: refactor query, publish_date is depreciated
        new_filter = self.request.GET.get('new', None)
        if new_filter and new_filter.isnumeric() and int(new_filter) == 1:
            #qs = qs.filter(releasedate__gte=F('publish_date')).distinct()
            qs = qs.filter(releasedate__range=(datetime.datetime.now() - timedelta(days=14), datetime.datetime.now().date())).distinct()
            f = {'item_type': 'release' , 'item': _('New Releases'), 'label': 'Filter'}
            self.relation_filter.append(f)


        # "extra-filters" (to provide some arbitary searches)
        extra_filter = self.request.GET.get('extra_filter', None)
        if extra_filter:
            if extra_filter == 'no_cover':
                qs = qs.filter(main_image='').distinct()
            if extra_filter == 'has_cover':
                qs = qs.exclude(main_image='').distinct()

            if extra_filter == 'possible_duplicates':
                from django.db.models import Count
                dupes = Release.objects.values('name').annotate(Count('id')).order_by().filter(id__count__gt=1)
                qs = qs.filter(name__in=[item['name'] for item in dupes])
                if not order_by:
                    qs = qs.order_by('name')



        
        # apply filters
        self.filter = ReleaseFilter(self.request.GET, queryset=qs)
        qs = self.filter.qs

        stags = self.request.GET.get('tags', None)
        tstags = []
        if stags:
            stags = stags.split(',')
            for stag in stags:
                tstags.append(int(stag))

        if stags:
            qs = Release.tagged.with_all(tstags, qs)

        # rebuild filter after applying tags
        self.filter = ReleaseFilter(self.request.GET, queryset=qs)
        
        # tagging / cloud generation
        if qs.exists():
            tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=5)
            self.tagcloud = calculate_cloud(tagcloud)

        return qs



class ReleaseDetailView(DetailView):

    model = Release
    context_object_name = "release"
    extra_context = {}
    
    def render_to_response(self, context):
        return super(ReleaseDetailView, self).render_to_response(context, content_type="text/html")
        
    def get_context_data(self, **kwargs):
        
        context = super(ReleaseDetailView, self).get_context_data(**kwargs)
        obj = kwargs.get('object', None)

        self.extra_context['history'] = reversion.get_unique_for_object(obj)

        context.update(self.extra_context)
        
        return context







class ReleaseEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Release
    form_class = ReleaseForm
    template_name = 'alibrary/release_edit.html'
    permission_required = 'alibrary.change_release'
    raise_exception = True
    success_url = '#'

    def __init__(self, *args, **kwargs):
        self.created_artists = {}
        super(ReleaseEditView, self).__init__(*args, **kwargs)

    def get_initial(self):
        self.initial.update({
            'user': self.request.user,
            'd_tags': ','.join(t.name for t in self.object.tags)
        })
        return self.initial

    def get_context_data(self, **kwargs):
        ctx = super(ReleaseEditView, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        # TODO: is this a good way to pass the instance main form?
        ctx['form_errors'] = self.get_form_errors(form=ctx['form'])

        return ctx

    def get_named_formsets(self):

        return {
            'action': ReleaseActionForm(self.request.POST or None, instance=self.object, prefix='action'),
            'bulkedit': ReleaseBulkeditForm(self.request.POST or None, instance=self.object, prefix='bulkedit'),
            'relation': ReleaseRelationFormSet(self.request.POST or None, instance=self.object, prefix='relation'),
            'albumartist': AlbumartistFormSet(self.request.POST or None, instance=self.object, prefix='albumartist'),
            'media': ReleaseMediaFormSet(self.request.POST or None, instance=self.object, prefix='media'),
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


        # moved to revision transaction
        # for name, formset in named_formsets.items():
        #     formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
        #     if formset_save_func is not None:
        #         formset_save_func(formset)
        #     else:
        #         formset.save()

        #publish = self.do_publish

        """
        # publishing is depreciated
        if publish:
            from datetime import datetime
            self.object.publish_date = datetime.now()
            self.object.publisher = self.request.user
            self.object.save()
        """


        # hm - not so nice. separate revision for media formset:
        # separate revision needed for media object, as it should only display
        # changes made to the object itself (and not the release object)
        # with reversion.create_revision():
        #
        #     # hm..
        #     self.object = form.save()
        #
        #     self.formset_media_valid(named_formsets['media'])
        #     msg = change_message.construct(self.request, None, [named_formsets['media'],])
        #     reversion.set_user(self.request.user)
        #     reversion.set_comment(msg)
        #
        #     for name, formset in named_formsets.items():
        #         formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
        #         if name != 'media':
        #             if formset_save_func is not None:
        #                 formset_save_func(formset)
        #             else:
        #                 formset.save()
        #
        #     # we still need the media formset here to get revision for the whole form
        #     msg = change_message.construct(self.request, form, [named_formsets['relation'],
        #                                                         named_formsets['albumartist'],
        #                                                         named_formsets['media'],])
        #
        #     d_tags = form.cleaned_data['d_tags']
        #     if d_tags:
        #         msg = change_message.parse_tags(obj=self.object, d_tags=d_tags, msg=msg)
        #         self.object.tags = d_tags
        #
        #     reversion.set_user(self.request.user)
        #     reversion.set_comment(msg)
        #
        #     # set actstream (e.v. atracker?)
        #     if msg != 'Nothing changed':
        #         actstream.action.send(self.request.user, verb=_('updated'), target=self.object)
        #
        # messages.add_message(self.request, messages.INFO, msg)



        # revisions disabled -> needs refactoring


        self.object.last_editor = self.request.user
        actstream.action.send(self.request.user, verb=_('updated'), target=self.object)


        self.object = form.save()

        self.formset_media_valid(named_formsets['media'])

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if name != 'media':
                if formset_save_func is not None:
                    formset_save_func(formset)
                else:
                    formset.save()

        d_tags = form.cleaned_data['d_tags']
        if d_tags:
            self.object.tags = d_tags

        messages.add_message(self.request, messages.INFO, 'Object updated')

        return HttpResponseRedirect('')



    def formset_media_valid(self, formset):
        media = formset.save(commit=False)

        # TODO: this is extremely ugly!! refactor!

        import hashlib
        for m in media:

            if m.artist and not m.artist.pk:
                key = hashlib.md5(m.artist.name.encode('ascii', 'ignore')).hexdigest()
                try:
                    artist = self.created_artists[key]
                except Exception as e:
                    m.artist.save()
                    artist = m.artist
                    self.created_artists[key] = artist

                m.artist = artist
                m.save()
            else:
                m.save()

            if formset.has_changed():
                # set actstream (e.v. atracker?)
                actstream.action.send(self.request.user, verb=_('updated'), target=m)


    def formset_albumartist_valid(self, formset):

        import hashlib

        # TODO: this is extremely ugly!! refactor!
        albumartists = formset.save(commit=False)

        delete_qs = ReleaseAlbumartists.objects.filter(release__pk=self.object.pk)
        delete_qs = delete_qs.exclude(artist__pk__in=[a.artist.pk for a in albumartists])
        delete_qs.delete()

        for albumartist in albumartists:
            key = hashlib.md5(albumartist.artist.name.encode('ascii', 'ignore')).hexdigest()
            try:
                artist = self.created_artists[key]
            except Exception as e:
                pass
            else:
                delete_pk = albumartist.artist.pk
                albumartist.artist = artist
                albumartist.save()
                merge_objects(albumartist.artist, [Artist.objects.get(pk=delete_pk),])

            albumartist.save()


    def formset_action_valid(self, formset):
        self.do_publish = formset.cleaned_data.get('publish', False)

    


    
# autocompleter views
def release_autocomplete(request):

    q = request.GET.get('q', None)
    
    result = []
    
    if q and len(q) > 1:
        
        releases = Release.objects.filter(Q(name__istartswith=q)\
            | Q(media_release__name__icontains=q)\
            | Q(media_release__artist__name__icontains=q)\
            | Q(label__name__icontains=q))\
            .distinct()
        for release in releases:
            item = {}
            item['release'] = release
            medias = []
            artists = []
            labels = []
            for media in release.media_release.filter(name__icontains=q).distinct():
                if not media in medias:
                    medias.append(media)
            for media in release.media_release.filter(artist__name__icontains=q).distinct():
                if not media.artist in artists:
                    artists.append(media.artist)
                
            if not len(artists) > 0:
                artists = None
            if not len(medias) > 0:
                medias = None
            if not len(labels) > 0:
                labels = None

            item['artists'] = artists
            item['medias'] = medias
            item['labels'] = labels
            
            result.append(item)

    return render_to_response("alibrary/element/autocomplete.html", { 'query': q, 'result': result }, context_instance=RequestContext(request))
    



class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        
        ret = {}
        
        release = context['release']
        
        ret['name'] = release.name
        ret['status'] = True
        
        ret['media'] = {};
        
        for media in release.get_media():
            ret['media'][media.id] = {
                                      'name': media.name,
                                      'tracknumber': media.tracknumber,
                                      'url': media.master.url
                                      }
        
        
        
        return json.dumps(ret)
    
class JSONReleaseDetailView(JSONResponseMixin, ReleaseDetailView):
    pass

