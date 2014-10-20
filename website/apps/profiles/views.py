from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import list_detail
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from actstream.models import *
from tagging.models import Tag
from django.db.models import Q

from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from profiles.models import *
from profiles.forms import *
from alibrary.models import Playlist, Release, Media
from profiles.filters import ProfileFilter
from lib.util import tagging_extra

from invitation.models import Invitation


PAGINATE_BY = getattr(settings, 'PROFILES_PAGINATE_BY', (12,24,36))
PAGINATE_BY_DEFAULT = getattr(settings, 'PROFILES_PAGINATE_BY_DEFAULT', 12)

ORDER_BY = [
    {
        'key': 'user__first_name',
        'name': _('Name')
    },
    {
        'key': 'user__last_name',
        'name': _('Surname')
    },
    {
        'key': 'user__username',
        'name': _('Username')
    },
    {
        'key': 'created',
        'name': _('Date joined')
    },
    {
        'key': 'updated',
        'name': _('Last modified')
    },
    {
        'key': 'user__last_login',
        'name': _('Last login')
    },
]





def profile_list(request):
    return list_detail.object_list(
        request,
        queryset=Profile.objects.all(),
        paginate_by=20,
    )
profile_list.__doc__ = list_detail.object_list.__doc__


class ProfileListView(PaginationMixin, ListView):
    
    # context_object_name = "artist_list"
    # template_name = "alibrary/artist_list.html"
    paginate_by = PAGINATE_BY
    extra_context = {}
    
    def get_paginate_by(self, queryset):
        
        ipp = self.request.GET.get('ipp', PAGINATE_BY_DEFAULT)
        if ipp:
            try:
                if int(ipp) in PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):
        
        context = super(ProfileListView, self).get_context_data(**kwargs)
        
        self.extra_context['filter'] = self.filter
        self.extra_context['relation_filter'] = self.relation_filter
        self.extra_context['tagcloud'] = self.tagcloud
        self.extra_context['list_style'] = self.request.GET.get('list_style', 'm')
        self.extra_context['get'] = self.request.GET

        self.extra_context['order_by'] = ORDER_BY
        
        context.update(self.extra_context)
        return context
    

    def get_queryset(self, **kwargs):

        # return render_to_response('my_app/template.html', {'filter': f})

        kwargs = {}

        self.tagcloud = None

        q = self.request.GET.get('q', None)
        
        if q:
            qs = Profile.objects.filter(Q(user__username__istartswith=q)\
            | Q(user__first_name__istartswith=q)\
            | Q(user__last_name__istartswith=q))\
            .distinct()
        else:
            qs = Profile.objects.all()
            
            
        order_by = self.request.GET.get('order_by', None)
        direction = self.request.GET.get('direction', None)
        
        if order_by and direction:
            if direction == 'descending':
                qs = qs.order_by('-%s' % order_by)
            else:
                qs = qs.order_by('%s' % order_by)

        else:
            qs = qs.order_by('user__first_name', 'user__last_name')
            
            
            
        # special relation filters
        # TODO: maybe implement for profiles
        self.relation_filter = []
        
        artist_filter = self.request.GET.get('artist', None)
        if artist_filter:
            qs = qs.filter(media_release__artist__slug=artist_filter).distinct()
            # add relation filter
            fa = Artist.objects.filter(slug=artist_filter)[0]
            f = {'item_type': 'artist' , 'item': fa, 'label': _('Artist')}
            self.relation_filter.append(f)
            
        label_filter = self.request.GET.get('label', None)
        if label_filter:
            qs = qs.filter(label__slug=label_filter).distinct()
            # add relation filter
            fa = Label.objects.filter(slug=label_filter)[0]
            f = {'item_type': 'label' , 'item': fa, 'label': _('Label')}
            self.relation_filter.append(f)

        # apply filters
        self.filter = ProfileFilter(self.request.GET, queryset=qs)

        qs = self.filter.qs

        stags = self.request.GET.get('tags', None)
        tstags = []
        if stags:
            stags = stags.split(',')
            for stag in stags:
                tstags.append(int(stag))

        if stags:
            qs = Profile.tagged.with_all(tstags, qs)
            
        # rebuild filter after applying tags
        self.filter = ProfileFilter(self.request.GET, queryset=qs)
        
        # tagging / cloud generation
        tagcloud = Tag.objects.usage_for_queryset(qs, counts=True, min_count=0)
        self.tagcloud = tagging_extra.calculate_cloud(tagcloud)

        return qs






class ProfileDetailView(DetailView):

    context_object_name = "profile"
    model = Profile
    slug_field = 'user__username'
    

    
    def render_to_response(self, context):
        return super(ProfileDetailView, self).render_to_response(context, mimetype="text/html")
        
    def get_context_data(self, **kwargs):
        context = kwargs
        context_object_name = self.get_context_object_name(self.object)
        # get contributions
        # TODO: this is kind of a hack...
        if self.request.user == self.object.user:
            context['broadcasts'] = Playlist.objects.filter(user=self.object.user).order_by('-updated')
        else:
            context['broadcasts'] = Playlist.objects.filter(user=self.object.user).exclude(type='basket').order_by('-updated')



        context['uploaded_releases'] = Release.objects.filter(creator=self.object.user).order_by('-created')
        context['uploaded_media'] = Media.objects.filter(creator=self.object.user).order_by('-created')

        context['user_stream'] = actor_stream(self.object.user)[0:20]

        context['following'] = Follow.objects.following(self.object.user)
        context['followers'] = Follow.objects.followers(self.object.user)

        if context_object_name:
            context[context_object_name] = self.object

        return context





def profile_detail(request, username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404
    profile = Profile.objects.get(user=user)
    context = { 'object':profile }
    return render_to_response('profiles/profile_detail.html', context, context_instance=RequestContext(request))


@login_required
def profile_edit(request, template_name='profiles/profile_form.html'):
    """Edit profile."""

    if request.POST:
        profile = Profile.objects.get(user=request.user)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        service_formset = ServiceFormSet(request.POST, instance=profile)
        link_formset = LinkFormSet(request.POST, instance=profile)

        if profile_form.is_valid() and user_form.is_valid() and service_formset.is_valid() and link_formset.is_valid():
            profile_form.save()
            user_form.save()
            link_formset.save()
            service_formset.save()
            #return HttpResponseRedirect(reverse('profile_detail', kwargs={'username': request.user.username}))
            return HttpResponseRedirect(reverse('profiles-profile-edit'))
        else:

            from lib.util.form_errors import merge_form_errors
            form_errors = merge_form_errors([
                user_form,
                profile_form,
                service_formset,
                link_formset,
            ])

            context = {
                'object': profile,
                'action_form': ActionForm(),
                'profile_form': profile_form,
                'user_form': user_form,
                'service_formset': service_formset,
                'link_formset': link_formset,
                'form_errors': form_errors,
            }

    else:
        profile = Profile.objects.get(user=request.user)
        link_formset = LinkFormSet(instance=profile)
        service_formset = ServiceFormSet(instance=profile)
        
        context = {
            'object': profile,
            'action_form': ActionForm(),
            'profile_form': ProfileForm(instance=profile),
            'user_form': UserForm(instance=request.user),
            'service_formset': service_formset,
            'link_formset': link_formset
        }
    return render_to_response(template_name, context, context_instance=RequestContext(request))






# TODO: Implement!
def profile_force_login(request, username):
    raise NotImplementedError("Not implemented yet.")










"""
mentoring views
"""

@login_required
def profile_mentor(request, pk, cancel = False):

    profile = get_object_or_404(Profile, pk=pk)

    if cancel and profile.mentor == request.user:
        profile.mentor = None
        profile.save()
    elif not profile.mentor:
        profile.mentor = request.user
        profile.save()

    return respond(request, 201)


@login_required
def profile_approve(request, pk, level):

    profile = get_object_or_404(Profile, pk=pk)
    
    if not profile.mentor == request.user:
        return respond(request, 403)
    
    # assign groups
    profile.approve(mentor=request.user, level=level)

    return respond(request, 201)


def respond(request, code):
    """
    Responds to the request with the given response code.
    If ``next`` is in the form, it will redirect instead.
    """
    if 'next' in request.REQUEST:
        return HttpResponseRedirect(request.REQUEST['next'])
    return type('Response%d' % code, (HttpResponse, ), {'status_code': code})()






"""
invitation based views / hackish here but still better than in invitation module...
"""

class InvitationListView(PaginationMixin, ListView):

    # context_object_name = "artist_list"
    template_name = "profiles/invitation_list.html"
    paginate_by = PAGINATE_BY
    extra_context = {}

    def get_paginate_by(self, queryset):

        ipp = self.request.GET.get('ipp', PAGINATE_BY_DEFAULT)
        if ipp:
            try:
                if int(ipp) in PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by

    def get_context_data(self, **kwargs):

        context = super(InvitationListView, self).get_context_data(**kwargs)
        #context.update(self.extra_context)
        return context


    def get_queryset(self, **kwargs):

        kwargs = {}
        from invitation.models import Invitation
        qs = Invitation.objects.filter(user=self.request.user)

        return qs


class InvitationDeleteView(View):

    model = Invitation

    def get(self, *args, **kwargs):

        i = get_object_or_404(Invitation, pk=kwargs['pk'])

        if not i.user == self.request.user:
            return HttpResponseForbidden('permission denied')

        if i.delete():
            messages.add_message(self.request, messages.INFO, _('Deleted invitation for %s' % i.email))


        return HttpResponseRedirect(reverse('profiles-invitations'))


