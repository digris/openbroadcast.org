from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from actstream import actions, models
from actstream.models import *

from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from actstream.filters import ActionFilter


PAGINATE_BY = getattr(settings, 'ACTSTREAM_PAGINATE_BY', (30,60,120))
PAGINATE_BY_DEFAULT = getattr(settings, 'ACTSTREAM_PAGINATE_BY_DEFAULT', 30)

class ActionListView(PaginationMixin, ListView):
    
    context_object_name = "action_list"
    # template_name = "alibrary/artist_list.html"
    paginate_by = PAGINATE_BY_DEFAULT
    
    def get_paginate_by(self, queryset):
        
        ipp = self.request.GET.get('ipp', None)
        if ipp:
            try:
                if int(ipp) in PAGINATE_BY:
                    return int(ipp)
            except Exception, e:
                pass

        return self.paginate_by
    
    def get_queryset(self):

        kwargs = {}
        
        qs = Action.objects.filter(**kwargs)

        
        user_filter = self.request.GET.get('username', None)
        if user_filter:
            user = get_object_or_404(User, username=user_filter)
            qs = qs.filter(actor_object_id=user.pk).distinct()


        # apply filters
        self.filter = ActionFilter(self.request.GET, queryset=qs)

        qs = self.filter.qs


        
        return qs
    

    def get_context_data(self, **kwargs):
        context = super(ActionListView, self).get_context_data(**kwargs)

        context.update({'filter': self.filter})
        context['filter'] = self.filter
        # context['user_stream'] = actor_stream(self.request.user)
        return context


class ActionDetailView(DetailView):

    context_object_name = "action"
    model = Action

    
    def render_to_response(self, context):
        return super(ActionDetailView, self).render_to_response(context, mimetype="text/html")
        
    def get_context_data(self, **kwargs):
        context = super(ActionDetailView, self).get_context_data(**kwargs)
        return context



def respond(request, code):
    """
    Responds to the request with the given response code.
    If ``next`` is in the form, it will redirect instead.
    """
    if 'next' in request.REQUEST:
        return HttpResponseRedirect(request.REQUEST['next'])
    return type('Response%d' % code, (HttpResponse, ), {'status_code': code})()


@login_required
@csrf_exempt
def follow_unfollow(request, content_type_id, object_id, do_follow=True, actor_only=True):
    """
    Creates or deletes the follow relationship between ``request.user`` and the
    actor defined by ``content_type_id``, ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = get_object_or_404(ctype.model_class(), pk=object_id)

    if do_follow:
        actions.follow(request.user, actor, actor_only=actor_only)
        return respond(request, 201)   # CREATED
    actions.unfollow(request.user, actor)
    return respond(request, 204)   # NO CONTENT


@login_required
def stream(request):
    """
    Index page for authenticated user's activity stream. (Eg: Your feed at
    github.com)
    """
    return render_to_response(('actstream/actor.html', 'activity/actor.html'), {
        'ctype': ContentType.objects.get_for_model(User),
        'actor': request.user, 'action_list': models.user_stream(request.user)
    }, context_instance=RequestContext(request))


def followers(request, content_type_id, object_id):
    """
    Creates a listing of ``User``s that follow the actor defined by
    ``content_type_id``, ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = get_object_or_404(ctype.model_class(), pk=object_id)
    return render_to_response(('actstream/followers.html', 'activity/followers.html'), {
        'followers': models.followers(actor), 'actor': actor
    }, context_instance=RequestContext(request))


def following(request, user_id):
    """
    Returns a list of actors that the user identified by ``user_id`` is following (eg who im following).
    """
    user = get_object_or_404(User, pk=user_id)
    return render_to_response(('actstream/following.html', 'activity/following.html'), {
        'following': models.following(user), 'user': user
    }, context_instance=RequestContext(request))


def user(request, username):
    """
    ``User`` focused activity stream. (Eg: Profile page twitter.com/justquick)
    """
    user = get_object_or_404(User, username=username, is_active=True)
    return render_to_response(('actstream/actor.html', 'activity/actor.html'), {
        'ctype': ContentType.objects.get_for_model(User),
        'actor': user, 'action_list': models.user_stream(user)
    }, context_instance=RequestContext(request))


def detail(request, action_id):
    """
    ``Action`` detail view (pretty boring, mainly used for get_absolute_url)
    """
    return render_to_response(('actstream/detail.html', 'activity/detail.html'), {
        'action': get_object_or_404(models.Action, pk=action_id)
    }, context_instance=RequestContext(request))


def actor(request, content_type_id, object_id):
    """
    ``Actor`` focused activity stream for actor defined by ``content_type_id``,
    ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = get_object_or_404(ctype.model_class(), pk=object_id)
    return render_to_response(('actstream/actor.html', 'activity/actor.html'), {
        'action_list': models.actor_stream(actor), 'actor': actor,
        'ctype': ctype
    }, context_instance=RequestContext(request))


def model(request, content_type_id):
    """
    ``Actor`` focused activity stream for actor defined by ``content_type_id``,
    ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = ctype.model_class()
    return render_to_response(('actstream/actor.html', 'activity/actor.html'), {
        'action_list': models.model_stream(actor), 'ctype': ctype,
        'actor': ctype
    }, context_instance=RequestContext(request))
