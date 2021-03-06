from actstream import actions, models
from actstream.filters import ActionFilter
from actstream.models import Action
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin

PAGINATE_BY = getattr(settings, "ACTSTREAM_PAGINATE_BY", (30, 60, 120))
PAGINATE_BY_DEFAULT = getattr(settings, "ACTSTREAM_PAGINATE_BY_DEFAULT", 120)


class ActionListView(PaginationMixin, ListView):

    context_object_name = "action_list"
    paginate_by = 120

    def get_queryset(self):

        kwargs = {}
        qs = Action.objects.filter(**kwargs)

        user_filter = self.request.GET.get("username", None)
        if user_filter:
            user = get_object_or_404(get_user_model(), username=user_filter)
            qs = qs.filter(actor_object_id=user.pk).distinct()

        qs = qs.select_related(
            "actor_content_type", "target_content_type", "action_object_content_type"
        ).prefetch_related("actor", "target", "action_object")

        # apply (legacy) filters
        self.filter = ActionFilter(self.request.GET, queryset=qs)

        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(ActionListView, self).get_context_data(**kwargs)
        context.update({"filter": self.filter})
        context["filter"] = self.filter
        return context


def respond(request, code):
    """
    Responds to the request with the given response code.
    If ``next`` is in the form, it will redirect instead.
    """
    if "next" in request.GET:
        return HttpResponseRedirect(request.GET["next"])
    return type("Response%d" % code, (HttpResponse,), {"status_code": code})()


@login_required
@csrf_exempt
def follow_unfollow(
    request, content_type_id, object_id, do_follow=True, actor_only=True
):
    """
    Creates or deletes the follow relationship between ``request.user`` and the
    actor defined by ``content_type_id``, ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = get_object_or_404(ctype.model_class(), pk=object_id)

    if do_follow:
        actions.follow(request.user, actor, actor_only=actor_only)
        return respond(request, 201)  # CREATED
    actions.unfollow(request.user, actor)
    return respond(request, 204)  # NO CONTENT


@login_required
def stream(request):
    """
    Index page for authenticated user's activity stream. (Eg: Your feed at
    github.com)
    """
    return render_to_response(
        ("actstream/actor.html", "activity/actor.html"),
        {
            "ctype": ContentType.objects.get_for_model(get_user_model()),
            "actor": request.user,
            "action_list": models.user_stream(request.user),
        },
        context_instance=RequestContext(request),
    )


def followers(request, content_type_id, object_id):
    """
    Creates a listing of ``User``s that follow the actor defined by
    ``content_type_id``, ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = get_object_or_404(ctype.model_class(), pk=object_id)
    return render_to_response(
        ("actstream/followers.html", "activity/followers.html"),
        {"followers": models.followers(actor), "actor": actor},
        context_instance=RequestContext(request),
    )


def following(request, user_id):
    """
    Returns a list of actors that the user identified by ``user_id`` is following (eg who im following).
    """
    user = get_object_or_404(get_user_model(), pk=user_id)
    return render_to_response(
        ("actstream/following.html", "activity/following.html"),
        {"following": models.following(user), "user": user},
        context_instance=RequestContext(request),
    )


def user(request, username):
    """
    ``User`` focused activity stream. (Eg: Profile page twitter.com/justquick)
    """
    user = get_object_or_404(get_user_model(), username=username, is_active=True)
    return render_to_response(
        ("actstream/actor.html", "activity/actor.html"),
        {
            "ctype": ContentType.objects.get_for_model(get_user_model()),
            "actor": user,
            "action_list": models.user_stream(user),
        },
        context_instance=RequestContext(request),
    )


def detail(request, action_id):
    """
    ``Action`` detail view (pretty boring, mainly used for get_absolute_url)
    """
    return render_to_response(
        ("actstream/detail.html", "activity/detail.html"),
        {"action": get_object_or_404(models.Action, pk=action_id)},
        context_instance=RequestContext(request),
    )


def actor(request, content_type_id, object_id):
    """
    ``Actor`` focused activity stream for actor defined by ``content_type_id``,
    ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = get_object_or_404(ctype.model_class(), pk=object_id)
    return render_to_response(
        ("actstream/actor.html", "activity/actor.html"),
        {"action_list": models.actor_stream(actor), "actor": actor, "ctype": ctype},
        context_instance=RequestContext(request),
    )


def model(request, content_type_id):
    """
    ``Actor`` focused activity stream for actor defined by ``content_type_id``,
    ``object_id``.
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    actor = ctype.model_class()
    return render_to_response(
        ("actstream/actor.html", "activity/actor.html"),
        {"action_list": models.model_stream(actor), "ctype": ctype, "actor": ctype},
        context_instance=RequestContext(request),
    )
