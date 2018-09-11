# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from actstream.models import Follow, actor_stream
from alibrary.models import Playlist, Release, Media
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, View, UpdateView
from braces.views import LoginRequiredMixin
from invitation.models import Invitation
from profiles.forms import UserForm, ProfileForm, ServiceFormSet, LinkFormSet, ActionForm, UserCredentialsForm
from profiles.models import Profile, User
from pure_pagination.mixins import PaginationMixin

from elasticsearch_dsl import TermsFacet
from search.views import BaseFacetedSearch, BaseSearchListView

from .documents import ProfileDocument


class ProfileSearch(BaseFacetedSearch):
    doc_types = [ProfileDocument]
    fields = ['tags', 'name', ]

    facets = [
        ('tags', TermsFacet(field='tags', size=100)),
        ('country', TermsFacet(field='country', size=500, order={'_key': 'asc'})),
        ('expertise', TermsFacet(field='expertise')),
        ('access_level', TermsFacet(field='groups')),
    ]


class ProfileListView(BaseSearchListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    search_class = ProfileSearch
    order_by = [
        {
            'key': 'created',
            'name': _('Creation date'),
            'default_direction': 'desc',
        },
        {
            'key': 'updated',
            'name': _('Modification date'),
            'default_direction': 'asc',
        },
        {
            'key': 'date_joined',
            'name': _('Date joined'),
            'default_direction': 'desc',
        },
        {
            'key': 'last_login',
            'name': _('Last Login'),
            'default_direction': 'desc',
        },
        {
            'key': 'name',
            'name': _('Name'),
            'default_direction': 'asc',
        },
    ]

    def get_queryset(self, **kwargs):
        qs = super(ProfileListView, self).get_queryset(**kwargs)

        qs = qs.select_related(
            'user',
            'country',
            'mentor',
        ).prefetch_related(
            'user',
            'user__groups',
        )

        return qs



class ProfileDetailView(DetailView):

    model = Profile
    template_name = 'profiles/profile_detail_ng.html'
    #context_object_name = "profile"

    # queryset = Profile.objects.select_related(
    #     'mentor',
    #     'country',
    # ).prefetch_related(
    #     'link_set',
    #     'user__votes',
    # )

    def get_object(self, queryset=None):

        profile = get_object_or_404(
            self.model,
            user__username=self.kwargs['username']
        )

        return profile



    def get_context_data(self, **kwargs):
        context = kwargs
        context_object_name = self.get_context_object_name(self.object)

        # get contributions
        # TODO: this is kind of a hack...
        if self.request.user == self.object.user:
            context['broadcasts'] = Playlist.objects.filter(user=self.object.user).order_by('-updated')
        else:
            context['broadcasts'] = Playlist.objects.filter(user=self.object.user).exclude(type='basket').order_by(
                '-updated')


        release_qs = Release.objects.filter(
            creator=self.object.user
        ).select_related(
            'label',
            'release_country',
            'creator',
            'creator__profile',
        ).prefetch_related(
            'media',
            'media__artist',
            'media__license',
            'extra_artists',
            'album_artists',
        ).order_by('-created')


        media_qs = Media.objects.filter(
            creator=self.object.user
        ).select_related(
            'release',
            'artist',
        ).prefetch_related(
            'media_artists',
            'extra_artists',
        ).order_by('-created')

        context['uploaded_releases'] = release_qs
        context['uploaded_media'] = media_qs

        # context['uploaded_releases'] = Release.objects.filter(creator=self.object.user).order_by('-created')
        # context['uploaded_media'] = Media.objects.filter(creator=self.object.user).order_by('-created')

        context['user_stream'] = actor_stream(self.object.user)[0:20]

        context['following'] = Follow.objects.following(self.object.user)
        context['followers'] = Follow.objects.followers(self.object.user)

        # votes
        # vs = Vote.objects.filter(user=u).order_by('-vote', '-created')
        # TODO: rewrite queryset. this generates a tremendous amount of db-hits!
        context['upvotes'] = self.object.user.votes.filter(vote__gt=0).order_by('content_type__model', '-created')
        context['downvotes'] = self.object.user.votes.filter(vote__lt=0).order_by('content_type__model', '-created')

        if context_object_name:
            context[context_object_name] = self.object

        return context


# TODO: refactor to CBV
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
            return HttpResponseRedirect(reverse('profiles-profile-edit'))
        else:

            from base.utils.form_errors import merge_form_errors
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



class UserCredentialsView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = UserCredentialsForm
    template_name = 'profiles/credentials_form.html'
    success_url = '/network/users/edit/'

    def get_object(self):
        return self.request.user

    def get_initial(self):
        self.initial.update({
            'user': self.request.user,
        })
        return self.initial


    def form_valid(self, form):

        self.object = form.save(commit=False)

        if form.cleaned_data['new_password2']:
            self.object.set_password(form.cleaned_data['new_password2'])

        self.object = form.save()

        messages.add_message(self.request, messages.INFO, 'Credentials updated')

        return HttpResponseRedirect(self.success_url)





# TODO: Implement!
def profile_force_login(request, username):
    raise NotImplementedError("Not implemented yet.")


"""
mentoring views
"""


@login_required
def profile_mentor(request, pk, cancel=False):
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
    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    return type('Response%d' % code, (HttpResponse,), {'status_code': code})()


#######################################################################
# invitation based views / hackish here but still better than in
# invitation module..
#######################################################################
class InvitationListView(PaginationMixin, ListView):

    template_name = "profiles/invitation_list.html"
    paginate_by = 36
    extra_context = {}

    def get_context_data(self, **kwargs):

        context = super(InvitationListView, self).get_context_data(**kwargs)
        # context.update(self.extra_context)
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
