import logging

from atracker.models import Event
from atracker.util import create_event
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
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


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        list_allowed_methods = ["get"]
        detail_allowed_methods = ["get"]
        resource_name = "atracker/event"
        include_resource_uri = False
        # TODO: double-check for sensitive information
        fields = ["created"]
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
                r"^(?P<resource_name>%s)/(?P<content_type>[\w.]+)/(?P<object_uuid>[\w.-]+)(?:/(?P<action>[\w-]+))?(?:/(?P<user_id>-?[0-9]+))?%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view("create_event_for_user"),
                name="atracker-create-event-for-user",
            )
        ]

    # creante event in behalf of user
    """
    call via curl

    curl -i \
        -H "Accept: application/json" \
        -H "Authorization: ApiKey remote:d65b075c593f27a42c26e65be74c047e5b50d215" \
        http://local.openbroadcast.org:8080/api/v1/atracker/event/alibrary.media/4faa159c-87f4-43eb-b2b7-a4de124a05e5/stream/1/?format=json


    """

    def create_event_for_user(self, request, **kwargs):

        self.method_check(request, allowed=["get"])
        self.is_authenticated(request)
        self.throttle_check(request)

        object_uuid = kwargs.get("object_uuid", None)

        content_type = kwargs.get("content_type", None)
        orig_ct = content_type
        action = kwargs.get("action", None)
        user_id = kwargs.get("user_id", None)
        if user_id:
            user_id = int(user_id)

        log.debug(
            "create_event_for_user - content_type: %s - object_uuid: %s - action: %s - user_id: %s"
            % (content_type, object_uuid, action, user_id)
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

        if user_id:
            log.debug("creating event on _behalf_ of user with id: %s" % user_id)

            if request.user.has_perm("atracker.track_for_user"):
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
            log.info("creating event for user by request: %s" % user.username)

        else:
            log.debug("no authenticated user")
            user = None

        object = content_type.model_class().objects.get(uuid=object_uuid)

        if action:
            if not user:
                return HttpUnauthorized("No permission to update this resource.")

            create_event(user, object, None, action)

        bundle = {
            "object_id": object.id,
            "object_uuid": object.uuid,
            "ct": orig_ct,
            "action": action,
        }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)
