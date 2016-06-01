from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf.urls import *
from uuid import uuid4
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404

import json

from tastypie.authentication import MultiAuthentication, Authentication
from tastypie.authorization import *
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.http import HttpCreated
from django.http import HttpResponseForbidden, Http404
from tastypie import fields



from profiles.exceptions import APIBadRequest


import logging
log = logging.getLogger(__name__)



class UserResource(ModelResource):
    """

    """
    profile = fields.ForeignKey('profiles.api.ProfileResource', 'profile', null=True, full=True)

    class Meta:
        queryset = User.objects.all()
        detail_uri_name = 'username'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'patch', 'delete']
        resource_name = 'auth/user'
        #excludes = ['id', 'username', 'password', 'is_active', 'is_staff', 'is_superuser',]
        excludes = ['password',]
        authentication = MultiAuthentication(Authentication(), )
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'email': ['exact', ],
        }

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(username=request.user.username)

    def dehydrate(self, bundle):

        try:
            bundle.data['full_name'] = bundle.obj.get_full_name()
        except:
            bundle.data['full_name'] = None

        bundle.data['groups'] = ','.join(bundle.obj.groups.values_list('name', flat=True))

        return bundle


    # additional methods
    def prepend_urls(self):

        return [
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="profile-api-login"),

            url(r"^(?P<resource_name>%s)/register%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="profile-api-register"),

            url(r"^(?P<resource_name>%s)/validate-registration%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('validate_registration'), name="profile-api-validate-registration"),

            url(r"^(?P<resource_name>%s)/reset-password%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_password'), name="profile-api-reset-password"),

            url(r"^(?P<resource_name>%s)/get-or-create-social-user%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_or_create_social_user'), name="profile-api-get-or-create-social-user"),
        ]


    def login(self, request, **kwargs):

        self.method_check(request, allowed=['get', 'post', ])
        self.throttle_check(request)

        data = []
        try:
            data = json.loads(request.body)

        except ValueError as e:

            if request.GET:
                data = request.GET
            if request.POST:
                data = request.POST

        REQUIRED_FIELDS = ('username', 'password', )
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when logging in.').format(missing_key=field)
                )

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if not user:
            log.info('login failed for %s' % username)
            return HttpResponseForbidden(json.dumps({
                'error': {
                    'code': 'unauthorized',
                    'message': _('Invalid login data.'),
                }
            }))

        log.info('successfully login for %s' % username)

        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)

        # provide api key
        # bundle.data['api_key'] = bundle.obj.api_key.key

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

