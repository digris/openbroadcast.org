from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tagging.models import Tag
from django.contrib.auth.models import User
from guardian.forms import UserObjectPermissionsForm

from pure_pagination.mixins import PaginationMixin
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from alibrary.models import Playlist
from alibrary.forms import *
from alibrary.filters import PlaylistFilter
from lib.util import tagging_extra


ALIBRARY_PAGINATE_BY = getattr(settings, 'ALIBRARY_PAGINATE_BY', (12,24,36,120))
ALIBRARY_PAGINATE_BY_DEFAULT = getattr(settings, 'ALIBRARY_PAGINATE_BY_DEFAULT', 12)

ORDER_BY = [
    {
        'key': 'name',
        'name': _('Name')
    },
    {
        'key': 'duration',
        'name': _('Duration')
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

class PlaylistListView(PaginationMixin, ListView):
    
    context_object_name = "playlist_list"
    template_name = "alibrary/playlist_list.html"
    
    paginate_by = ALIBRARY_PAGINATE_BY_DEFAULT
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
        
        
        context = super(PlaylistListView, self).get_context_data(**kwargs)
        
        
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
        
        self.extra_context['list_style'] = self.request.GET.get('list_style', 'l')
        self.extra_context['get'] = self.request.GET
        
        context.update(self.extra_context)
        
        return context
    

    def get_queryset(self, **kwargs):
        
        
        self.tagcloud = None
        q = self.request.GET.get('q', None)

        #qs = Playlist.objects.all()
        if self.request.user.is_authenticated():
            qs = Playlist.objects.filter(~Q(type='basket') | Q(user__pk=self.request.user.pk))
            #qs = Playlist.objects.filter(~Q(type='basket'))
        else:
            qs = Playlist.objects.exclude(type='basket')


        
        if q:
            qs = qs.filter(Q(name__istartswith=q)\
            | Q(description__icontains=q)\
            | Q(user__username__istartswith=q))\
            .distinct()


            

            
            
        order_by = self.request.GET.get('order_by', None)
        direction = self.request.GET.get('direction', None)
        
        if order_by and direction:
            if direction == 'descending':
                qs = qs.order_by('-%s' % order_by)
            else:
                qs = qs.order_by('%s' % order_by)
            
            
            
        if 'type' in self.kwargs:
            qs = qs.filter(type=self.kwargs['type'])
            
        if 'user' in self.kwargs:
            user = get_object_or_404(User, username=self.kwargs['user'])
            if 'type' in self.kwargs:
                qs = qs.filter(type=self.kwargs['type'], user=user)
            else:
                 qs = qs.filter(type__in=['playlist', 'broadcast', 'basket'],user=user)
            
        # special relation filters
        self.relation_filter = []

        user_filter = self.request.GET.get('user', None)
        if user_filter:
            user = get_object_or_404(User, username=user_filter)
            #qs = qs.filter(media_release__artist__slug=artist_filter).distinct()
            # incl album_artists
            qs = qs.filter(user=user).distinct()

            # add relation filter
            fa = user # for consistency
            f = {'item_type': 'user' , 'item': fa, 'label': _('User')}
            self.relation_filter.append(f)






        
        # apply filters
        self.filter = PlaylistFilter(self.request.GET, queryset=qs)
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
        self.filter = PlaylistFilter(self.request.GET, queryset=qs)
        
        # tagging / cloud generation
        tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=0)

        self.tagcloud = tagging_extra.calculate_cloud(tagcloud)
        return qs
    
    """
    def get_queryset(self):
        kwargs = {}
        return Playlist.objects.filter(**kwargs)
    """

class PlaylistDetailView(DetailView):

    context_object_name = "playlist"
    model = Playlist
    
    def render_to_response(self, context):
        return super(PlaylistDetailView, self).render_to_response(context, mimetype="text/html")
        
    def get_context_data(self, **kwargs):

        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        return context
    

class PlaylistCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    
    model = Playlist
    
    template_name = 'alibrary/playlist_create.html'
    form_class = PlaylistForm

    permission_required = 'alibrary.add_playlist'
    raise_exception = True

    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    return super(PlaylistCreateView, self).dispatch(*args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super(PlaylistCreateView, self).get_context_data(**kwargs)
        context['action_form'] = ActionForm()        
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(obj.get_edit_url())


class PlaylistDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Playlist
    template_name = 'alibrary/playlist_delete.html'
    permission_required = 'alibrary.delete_playlist'
    raise_exception = True

    # TODO: this is a hack/bug/issue
    # http://stackoverflow.com/questions/7039839/how-do-i-use-reverse-or-an-equivalent-to-refer-to-urls-that-are-hooked-into-dj
    success_url = reverse_lazy('en:alibrary-playlist-list')


    def dispatch(self, request, *args, **kwargs):

        # TODO: here we could implement permission check for 'shared-editing' playlists
        obj = Playlist.objects.get(pk=int(kwargs['pk']))
        if not obj.user == request.user:
            raise PermissionDenied

        # check if possible to delete
        can_delete, reason = obj.can_be_deleted()
        if not can_delete:
            messages.add_message(request, messages.ERROR, reason)
            return HttpResponseRedirect(obj.get_edit_url())

        return super(PlaylistDeleteView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(PlaylistDeleteView, self).get_context_data(**kwargs)
        return context

    
    
class PlaylistEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    
    model = Playlist
    template_name = "alibrary/playlist_edit.html"
    success_url = '#'
    form_class = PlaylistForm

    permission_required = 'alibrary.change_playlist'
    raise_exception = True

    def __init__(self, *args, **kwargs):
        super(PlaylistEditView, self).__init__(*args, **kwargs)


    def dispatch(self, request, *args, **kwargs):

        # TODO: here we could implement permission check for 'shared-editing' playlists
        obj = Playlist.objects.get(pk=int(kwargs['pk']))
        if not obj.user == request.user:
            raise PermissionDenied

        return super(PlaylistEditView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({ 'user': self.request.user })
        return self.initial


    def get_context_data(self, **kwargs):

        context = super(PlaylistEditView, self).get_context_data(**kwargs)

        context['action_form'] = ActionForm()
        context['releasemedia_form'] = ReleaseMediaFormSet(instance=self.object)
        context['user'] = self.request.user
        context['request'] = self.request
        context['permission_form'] =  UserObjectPermissionsForm(self.request.user, self.object, self.request.POST or None)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        print 'PlaylistEditView - form_valid'

        # validation
        if form.is_valid():
            self.object.tags = form.cleaned_data['d_tags']

            # temporary instance to validate inline forms against
            tmp = form.save(commit=False)

            form.save()
            form.save_m2m()

            return HttpResponseRedirect('#')
        else:

            from lib.util.form_errors import merge_form_errors
            form_errors = merge_form_errors([form,])

            print form_errors


            return self.render_to_response(self.get_context_data(form=form, form_errors=form_errors))
        


@login_required
def playlist_convert(request, pk, type):
    
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)

    playlist, status = playlist.convert_to(type)
    if status:
        messages.add_message(request, messages.INFO, _('Successfully converted "%s" to "%s"' % (playlist.name, playlist.get_type_display())))
    else:
        messages.add_message(request, messages.ERROR,_('There occured an error while converting "%s"' % (playlist.name)))

    return HttpResponseRedirect(playlist.get_edit_url())

