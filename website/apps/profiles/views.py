# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from actstream.models import Action, Follow, actor_stream
from alibrary.models import Playlist, Release, Media
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView, View, UpdateView
from braces.views import LoginRequiredMixin
from invitation.models import Invitation
from profiles.forms import UserForm, ProfileForm, ServiceFormSet, LinkFormSet, ActionForm, UserCredentialsForm
from profiles.models import Profile
from django.contrib.auth import get_user_model
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
    section_template_base = 'profiles/profile/_detail'
    section = None
    sections = [
        ('playlists', _('Playlists')),
        ('profile', _('Profile')),
        ('votes', _('Up- & Downvotes')),
        ('uploads', _('Uploads')),
        ('activities', _('Activities')),
    ]

    def dispatch(self, request, *args, **kwargs):

        # get default section if none provided
        if not kwargs.get('section'):
            obj = self.get_object()
            section = self.get_default_section(obj)
            redirect_to = reverse_lazy('profiles-profile-detail', kwargs={'uuid': obj.uuid, 'section': section})
            return redirect(redirect_to)

        self.section = kwargs.get('section')
        if not self.section in [s[0] for s in self.sections]:
            return HttpResponseBadRequest('invalid section "{}"'.format(self.section))

        return super(ProfileDetailView, self).dispatch(request, *args, **kwargs)


    def get_object(self, queryset=None):
        obj = get_object_or_404(
            self.model,
            uuid=self.kwargs['uuid']
        )
        return obj


    def get_default_section(self, obj):
        if obj.user.playlists.exclude(type='basket').exists():
            return 'playlists'
        else:
            return 'profile'


    def get_section_menu(self, object, section):
        menu = []
        for key, title in self.sections:
            # TODO: find a better way
            if key == 'playlists' and not self.object.user.playlists.exclude(type='basket').exists():
                continue

            if key == 'uploads' and not self.object.user.created_media.exists():
                continue

            menu.append({
                'active': key == section,
                'title': title,
                'url': reverse('profiles-profile-detail', kwargs={'uuid': object.uuid, 'section': key})
            })

        return menu


    def get_section_template(self):
        template = '{base}_{section}.html'.format(
            base=self.section_template_base,
            section=self.section
        )
        return template


    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)

        section_menu = self.get_section_menu(object=self.object, section=self.section)

        ###############################################################
        # generic context, needed for all sections
        ###############################################################
        context.update({
            'section': self.section,
            'section_menu': section_menu,
            'section_template': self.get_section_template(),
        })

        ###############################################################
        # section specific context
        ###############################################################
        if self.section == 'playlists':
            playlist_qs = self.object.user.playlists.exclude(type='basket').order_by('-created')
            playlist_qs = playlist_qs.select_related(
                'user',
            ).prefetch_related(
                'items',
                'emissions',
            )
            context.update({
                'playlists': playlist_qs,
            })

        if self.section == 'uploads':
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

            context.update({
                'uploads': {
                    'releases': release_qs,
                    'media': media_qs,
                },
            })

        if self.section == 'votes':
            vote_qs = self.object.user.votes.order_by('-created').prefetch_related('content_object')

            upvotes = [v for v in vote_qs if v.vote > 0]
            downvotes = [v for v in vote_qs if v.vote < 0]

            context.update({
                'upvotes': upvotes,
                'downvotes': downvotes,
            })

        if self.section == 'activities':
            activity_qs = actor_stream(self.object.user).select_related(
                # 'actor_content_type',
                # 'target_content_type',
                # 'action_object_content_type',
            ).prefetch_related(
                'actor',
                'target',
                'action_object',
            ).order_by('-pk')

            # activity_qs = Action.objects.filter(
            #     actor_content_type__id=3,
            #     actor_object_id=self.object.user.pk
            # ).order_by('-pk')

            context.update({
                'activities': activity_qs,
            })


        return context


    def get(self, request, *args, **kwargs):
        return super(ProfileDetailView, self).get(request, *args, **kwargs)





#######################################################################
# TODO: views below here need to be reviewed / refacored
#######################################################################
class LegacyProfileDetailView(DetailView):

    model = Profile
    template_name = 'profiles/profile_detail.html'

    def get_object(self, queryset=None):

        profile = get_object_or_404(
            self.model,
            user__username=self.kwargs['username']
        )

        return profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        url = reverse_lazy('profiles-profile-detail', kwargs={'uuid': str(profile.uuid)})
        return redirect(url)

    #
    # def get_context_data(self, **kwargs):
    #     context = kwargs
    #     context_object_name = self.get_context_object_name(self.object)
    #
    #     # get contributions
    #     # TODO: this is kind of a hack...
    #     if self.request.user == self.object.user:
    #         context['broadcasts'] = Playlist.objects.filter(user=self.object.user).order_by('-updated')
    #     else:
    #         context['broadcasts'] = Playlist.objects.filter(user=self.object.user).exclude(type='basket').order_by(
    #             '-updated')
    #
    #
    #     release_qs = Release.objects.filter(
    #         creator=self.object.user
    #     ).select_related(
    #         'label',
    #         'release_country',
    #         'creator',
    #         'creator__profile',
    #     ).prefetch_related(
    #         'media',
    #         'media__artist',
    #         'media__license',
    #         'extra_artists',
    #         'album_artists',
    #     ).order_by('-created')
    #
    #
    #     media_qs = Media.objects.filter(
    #         creator=self.object.user
    #     ).select_related(
    #         'release',
    #         'artist',
    #     ).prefetch_related(
    #         'media_artists',
    #         'extra_artists',
    #     ).order_by('-created')
    #
    #     context['uploaded_releases'] = release_qs
    #     context['uploaded_media'] = media_qs
    #
    #     # context['uploaded_releases'] = Release.objects.filter(creator=self.object.user).order_by('-created')
    #     # context['uploaded_media'] = Media.objects.filter(creator=self.object.user).order_by('-created')
    #
    #     context['user_stream'] = actor_stream(self.object.user)[0:20]
    #
    #     context['following'] = Follow.objects.following(self.object.user)
    #     context['followers'] = Follow.objects.followers(self.object.user)
    #
    #     # votes
    #     # vs = Vote.objects.filter(user=u).order_by('-vote', '-created')
    #     # TODO: rewrite queryset. this generates a tremendous amount of db-hits!
    #     # context['upvotes'] = self.object.user.votes.filter(vote__gt=0).order_by('content_type__model', '-created')
    #     # context['downvotes'] = self.object.user.votes.filter(vote__lt=0).order_by('content_type__model', '-created')
    #     context['upvotes'] = self.object.user.votes.filter(vote__gt=0).order_by('-created')
    #     context['downvotes'] = self.object.user.votes.filter(vote__lt=0).order_by('-created')
    #
    #     if context_object_name:
    #         context[context_object_name] = self.object
    #
    #     return context


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

    model = get_user_model()
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
