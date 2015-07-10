from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf.urls import *
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

    def hydrate(self, bundle):

        if bundle.data.has_key('password'):
            try:
                bundle.obj.set_password(bundle.data['password'])
            except Exception, e:
                raise APIBadRequest(
                    code="error",
                    message=_('unable to update password. %s' % e)
                )
            log.info('updated password for %s' % bundle.obj.email)

        if bundle.data.has_key('email'):
            # check if changed
            if bundle.data['email'] != bundle.obj.email:

                if User.objects.filter(email=bundle.data['email']):
                    raise APIBadRequest(
                        code="duplicate_email",
                        message=_('That email is already used.'))

                user = bundle.obj
                user.email = bundle.data['email']
                user.username = bundle.data['email']
                log.info('updating email: %s to %s' % (user.email, bundle.data['email']))
                user.save()
                user.profile.email_confirmed = False
                user.profile.save()

                # hook up with registration
                RegistrationProfile.objects.filter(user=user).delete()
                registration_profile = RegistrationProfile.objects.create_profile(user)
                registration_signals.user_registered.send(sender=self.__class__, user=user, request=bundle.request)
                send_activation_email(registration_profile)

        # map to profile fields
        if bundle.data.has_key('height'):
            try:
                bundle.obj.profile.height = bundle.data['height']
                bundle.obj.profile.save()
            except Exception, e:
                raise APIBadRequest(
                    code="error",
                    message=_('unable to update height. %s' % e)
                )
            log.info('updated height for %s' % bundle.obj.email)

        if bundle.data.has_key('full_name'):
            try:
                bundle.obj.profile.full_name = bundle.data['full_name']
                bundle.obj.profile.save()
            except Exception, e:
                raise APIBadRequest(
                    code="error",
                    message=_('unable to update full_name. %s' % e)
                )
            log.info('updated full_name for %s' % bundle.obj.email)


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

            url(r"^(?P<resource_name>%s)/get-social-user%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_social_user'), name="profile-api-get-social-user"),
        ]


    def login(self, request, **kwargs):

        self.method_check(request, allowed=['get', 'post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError, e:

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

        except ValueError, e:
            if request.POST:
                data = request.POST


        print data

        REQUIRED_FIELDS = ('key', 'value', )
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when logging in.').format(missing_key=field)
                )

        key = data.get('key', None)
        value = data.get('value', None)


        print key
        print value

        error = None

        # logic goes here...
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

        except ValueError, e:

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


        # create the user as active
        # separate flag in profile model to track email confirmation
        #user = create_user(data['email'], data['password'], is_active=True)

        user = User.objects.create_user(username=data['username'],
                                        email=data['email'],
                                        password=data['password'])


        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)

        # provide api key
        #bundle.data['api_key'] = bundle.obj.api_key.key

        self.log_throttled_access(request)

        return self.create_response(request, bundle, response_class=HttpCreated)


    def reset_password(self, request, **kwargs):

        self.method_check(request, allowed=['get', 'post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError, e:

            if request.GET:
                data = request.GET

            if request.POST:
                data = request.POST

        REQUIRED_FIELDS = ('email', )
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when reseting password.').format(missing_key=field)
                )

        email = data.get('email', None)
        log.info('password reset request for %s' % email)

        try:
            user = User.objects.get(email=email)
            reset_password(user)

        except User.DoesNotExist, e:
            raise APIBadRequest(
                code="not_found",
                message=_('User does not exist.')
            )

        bundle = {
            'code': 'ok',
            'message': _('Sending new password to %s' % email)
        }

        self.log_throttled_access(request)
        return self.create_response(request, bundle)


    def get_social_user(self, request, **kwargs):

        self.method_check(request, allowed=['get', 'post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError, e:

            if request.GET:
                data = request.GET

            if request.POST:
                data = request.POST

        REQUIRED_FIELDS = ('provider', 'uid')
        for field in REQUIRED_FIELDS:
            if field not in data:
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when looking up a social user.').format(missing_key=field)
                )


        print data

        provider = data.get('provider', None)
        uid = data.get('uid', None)

        qs = User.objects.filter(social_auth__provider=provider, social_auth__uid=uid)

        if qs.exists():
            bundle = {
                'id': qs[0].id,
            }
        else:
            bundle = {
                'id': None,
            }


        self.log_throttled_access(request)
        return self.create_response(request, bundle)
