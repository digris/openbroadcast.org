import json
import logging
from uuid import uuid4

from django.conf.urls import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _
from profiles.exceptions import APIBadRequest
from tastypie import fields
from tastypie.authentication import MultiAuthentication, Authentication
from tastypie.authorization import *
from tastypie.http import HttpCreated
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

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

            url(r"^(?P<resource_name>%s)/get-or-create-social-user%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_or_create_social_user'), name="profile-api-get-or-create-social-user"),
        ]


    def login(self, request, **kwargs):

        self.method_check(request, allowed=['get', 'post', ])
        self.throttle_check(request)

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


    def validate_registration(self, request, **kwargs):

        self.method_check(request, allowed=['post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError as e:
            if request.POST:
                data = request.POST


        REQUIRED_FIELDS = ('key', 'value', )
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when logging in.').format(missing_key=field)
                )

        key = data.get('key', None)
        value = data.get('value', None)

        error = None

        if key == 'email':
            if User.objects.filter(email=value).exists():
                error = _('That email is already used.')

        if key == 'username':
            if User.objects.filter(username=value).exists():
                error = _('That username is already used.')


        bundle = {
            'error': error,
            'key': key,
            'value': value,
        }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)




    def register(self, request, **kwargs):

        self.method_check(request, allowed=['post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError as e:

            if request.POST:
                data = request.POST

        REQUIRED_FIELDS = ('username', 'email', 'password', )
        for field in REQUIRED_FIELDS:
            if field not in data:
                log.warning('missing key "{missing_key}" when creating a user.'.format(missing_key=field))
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when creating a user.').format(missing_key=field)
                )


        user = User.objects.create_user(username=data['username'],
                                        email=data['email'],
                                        password=data['password'])


        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)

        return self.create_response(request, bundle, response_class=HttpCreated)




    def get_or_create_social_user(self, request, **kwargs):

        self.method_check(request, allowed=['get', 'post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError as e:

            if request.GET:
                data = request.GET

            if request.POST:
                data = request.POST

        REQUIRED_FIELDS = ('provider', 'uid', 'extra_data', 'user')
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when looking up a social user.').format(missing_key=field)
                )


        provider = data['provider']
        uid = data['uid']
        extra_data = data['extra_data']
        user = json.loads(data['user'])

        user_qs = User.objects.filter(social_auth__provider=provider, social_auth__uid=uid)

        if not user_qs.exists():
            """
            create new account & social user
            """

            # TODO: hack!!! try to create unique username
            username = user['username']

            while User.objects.filter(username=username).exists():
                username += uuid4().get_hex()[:8]

            remote_user = User.objects.create_user(username=username,
                                            email=user['email'],
                                            password=None)

            remote_user.first_name = user['first_name']
            remote_user.last_name = user['last_name']
            remote_user.save()

            from social_auth.models import UserSocialAuth
            social_user = UserSocialAuth(
                user=remote_user,
                provider=provider,
                uid=uid,
                extra_data=extra_data,
            )
            social_user.save()

        else:
            remote_user = user_qs[0]
            remote_user.extra_data = extra_data
            remote_user.save()



        bundle = {
            'id': remote_user.id,
            'user': {
                'id': remote_user.id,
                'username': remote_user.username,
                'first_name': remote_user.first_name,
                'last_name': remote_user.last_name,
            }
        }


        self.log_throttled_access(request)
        return self.create_response(request, bundle)
