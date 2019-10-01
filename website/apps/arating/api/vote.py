import logging

from arating.models import Vote
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from tastypie.authentication import (
    MultiAuthentication,
    Authentication,
    SessionAuthentication,
    ApiKeyAuthentication,
)
from tastypie.authorization import Authorization
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

log = logging.getLogger(__name__)


class VoteResource(ModelResource):
    class Meta:
        queryset = Vote.objects.all()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        resource_name = "rating/vote"
        include_resource_uri = False
        # TODO: double-check for sensitive information
        fields = ["id", "created"]
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication(), Authentication()
        )
        authorization = Authorization()
        always_return_data = True
        filtering = {}

    def dehydrate(self, bundle):
        return bundle

    def prepend_urls(self):

        return [
            url(
                r"^(?P<resource_name>%s)/(?P<content_type>[\w.]+)/(?P<object_id>\d+)(?:/(?P<vote>-?\d{1}))?(?:/(?P<user_id>-?[0-9]+))?%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view("vote_by_ct"),
                name="arating-vote_api-by-ct",
            )
        ]

    # vote for user
    """
    30  onair.api.resources              INFO     Processing vote by root: -1 - alibrary.media - 123
    fields:
     - vote/value: -1, 0, 1
     - ct:         alibrary.media
     - ct_id:      123
     - user:       how to handle? request?

     default url schema:
     http://local.openbroadcast.org:8080/en/vote/alibrary.release/2202/-1/
     http://local.openbroadcast.org:8080/en/vote/alibrary.media/13530/1/



    """

    def vote_by_ct(self, request, **kwargs):

        self.method_check(request, allowed=["get"])
        self.is_authenticated(request)
        self.throttle_check(request)

        # v = Vote.objects.get(**self.remove_api_resource_names(kwargs))

        object_id = kwargs.get("object_id", None)
        if object_id:
            object_id = int(object_id)
        content_type = kwargs.get("content_type", None)
        orig_ct = content_type
        vote = kwargs.get("vote", None)
        if vote:
            vote = int(vote)
        user_id = kwargs.get("user_id", None)
        if user_id:
            user_id = int(user_id)

        log.debug(
            "vote_by_ct - content_type: %s - object_id: %s - vote: %s - user_id: %s"
            % (content_type, object_id, vote, user_id)
        )

        if isinstance(content_type, basestring) and "." in content_type:
            app, modelname = content_type.split(".")
            content_type = ContentType.objects.get(
                app_label=app, model__iexact=modelname
            )
        elif isinstance(content_type, basestring):
            content_type = ContentType.objects.get(id=int(content_type))
        else:
            raise ValueError('content_type must a ct id or "app.modelname" string')

        # no vot & no user_id: get the current vote(s)

        if user_id:
            log.debug("voting in _behalf_ of user with id: %s" % user_id)

            if request.user.has_perm("arating.vote_for_user"):
                user = get_user_model().objects.get(pk=user_id)
                log.info("voting for user by id: %s" % user.username)
            else:
                log.warning(
                    "no permission for %s to vote in behalf of %s"
                    % (request.user, user_id)
                )
                user = None

        elif request.user and request.user.is_authenticated():
            user = request.user
            log.info("voting for user by request: %s" % user.username)

        else:
            log.debug("no authenticated user")
            user = None

        if vote and vote != 0:

            if not user:
                return HttpUnauthorized("No permission to update this resource.")

            if not vote in (-1, 1):
                return HttpUnauthorized("Bad vote value.")

            vote_object, created = Vote.objects.get_or_create(
                content_type=content_type,
                object_id=object_id,
                user=user,
                defaults={"vote": vote},
            )
            if not created:
                vote_object.vote = vote
                vote_object.save()
            else:
                vote_object.save()

        elif vote == 0:

            if not user:
                return HttpUnauthorized("No permission to update this resource.")

            Vote.objects.filter(
                content_type=content_type, object_id=object_id, user=user
            ).delete()

        obj = content_type.model_class().objects.get(pk=object_id)

        avg_vote = obj.votes.aggregate(Avg("vote")).values()[0]
        upvotes = obj.votes.filter(vote__gt=0).count()
        downvotes = obj.votes.filter(vote__lt=0).count()

        try:
            uuid = obj.uuid
        except:
            uuid = None

        bundle = {
            "object_id": obj.id,
            "uuid": uuid,
            "ct": orig_ct,
            "up": upvotes,
            "down": downvotes,
            "total": avg_vote,
        }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)
