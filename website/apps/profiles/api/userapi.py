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
            url(
                r"^(?P<resource_name>%s)/?P<email>[A-Za-z0-9._+-]+@[A-Za-z0-9._+-]+\.[A-Za-z]{2,4}%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="profile-api-login"),
            url(r"^(?P<resource_name>%s)/register%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="profile-api-register"),
            url(r"^(?P<resource_name>%s)/reset-password%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_password'), name="profile-api-reset-password"),
            url(r"^(?P<resource_name>%s)/(?P<email>[A-Za-z0-9._+-]+@[A-Za-z0-9._+-]+\.[A-Za-z]{2,4})/forget-device%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('forget_device'), name="profile-api-forget-device"),
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


    def register(self, request, **kwargs):

        self.method_check(request, allowed=['post', ])
        self.throttle_check(request)

        try:
            data = json.loads(request.body)

        except ValueError, e:

            if request.POST:
                data = request.POST

        REQUIRED_FIELDS = ('email', 'password', )
        for field in REQUIRED_FIELDS:
            if field not in data:
                log.warning('missing key "{missing_key}" when creating a user.'.format(missing_key=field))
                raise APIBadRequest(
                    code="missing_key",
                    message=_('Must provide {missing_key} when creating a user.').format(missing_key=field)
                )

        try:
            email = data['email'].strip()
            if User.objects.filter(email=email):
                log.warning('duplicate_email: %s' % email)
                raise APIBadRequest(
                    code="duplicate_email",
                    message=_('That email is already used.'))
        except KeyError as missing_key:
            log.warning('missing key "{missing_key}" when creating a user.'.format(missing_key=field))
            raise APIBadRequest(
                code="missing_key",
                message=_('Must provide {missing_key} when creating a user.')
                .format(missing_key=missing_key))
        except User.DoesNotExist:
            pass


        # handle duplicate serial numbers
        try:
            serial_number = data['serial_number']
        except:
            serial_number = None

        if serial_number:
            if Device.objects.filter(serial_number=serial_number).exists():
                log.warning('duplicate serial number: %s' % (serial_number))
                raise APIBadRequest(
                    code="duplicate_serial_number",
                    message=_('That serial-number is already used.'))


        # create the user as active
        # separate flag in profile model to track email confirmation
        user = create_user(data['email'], data['password'], is_active=True)

        # hook up with registration
        registration_profile = RegistrationProfile.objects.create_profile(user)
        registration_signals.user_registered.send(sender=self.__class__, user=user, request=request)
        send_activation_email(registration_profile)

        # create device for user
        if serial_number:
            # device, created = Device.objects.get_or_create(profiles__in=[user.pk, ], serial_number=serial_number)
            device, created = Device.objects.get_or_create(serial_number=serial_number, status=2)
        else:
            # no serial provided, so create a 'app' device and generate a serial for it
            device = Device()
            device.generate_serial_number(user.pk)
            device.status = 2
            device.save()

        # finally create the user profile
        profile, created = UserProfile.objects.get_or_create(user=user, device=device)

        log.info('registraion success: %s - serial number: %s' % (email, device.serial_number))

        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)

        # provide api key
        bundle.data['api_key'] = bundle.obj.api_key.key

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


    def forget_device(self, request, **kwargs):
        """
        'forgetting' a device happens if a user unlinks a 'hardware' device from daysyView
        """
        self.method_check(request, allowed=['get', ])
        self.throttle_check(request)
        self.is_authenticated(request)

        user = User.objects.get(**self.remove_api_resource_names(kwargs))
        log.info('forget device for %s' % user.email)

        try:
            device = user.profile.device
        except Exception, e:
            device = None
            log.warning('unable to get device: %s' % e)


        if device:

            if device.profiles.count() > 1:
                log.warning('device has %s users assigned. so will not flush it!' % device.profiles.count())
                new_device = Device()
                new_device.generate_serial_number(id=user.pk)
                new_device.status = 2
                new_device.save()

                user.profile.device = new_device
                user.profile.save()


            else:
                device.generate_serial_number(id=user.pk)
                device.reset()
                device.status = 2
                device.save()

        # refresh user
        user = User.objects.get(pk=user.pk)

        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)

    # old version
    def __forget_device(self, request, **kwargs):
        """
        'forgetting' a device happens if a user unlinks a 'hardware' device from daysyView

        what happens:
         - a new device with a 'virtual' serial-number is created and attached to the user/profile
         - data (files) form the old device are copied to the new one
         - old device and its data (files) are deleted.
        """
        self.method_check(request, allowed=['get', ])
        self.throttle_check(request)
        self.is_authenticated(request)


        user = User.objects.get(**self.remove_api_resource_names(kwargs))

        log.info('forget device for %s' % user.email)

        old_device = user.profile.device

        device = Device()
        device.generate_serial_number(user.pk)
        from django.core.files.base import ContentFile
        # temporary store data
        try:
            data_file = ContentFile(old_device.data_file.read())
        except Exception, e:
            data_file = None
            print e

        try:
            analyse_file = ContentFile(old_device.analyse_file.read())
        except Exception, e:
            analyse_file = None
            print e

        # delete old instance (will also remove files from filesystem)
        old_device.delete()

        # store temporary data to file
        if data_file:
            device.data_file.save('data_file.xml', data_file)

        if analyse_file:
            device.analyse_file.save('data_file.xml', data_file)

        device.status = 2
        device.save()

        user.profile.device = device
        user.profile.save()


        # refresh user
        user = User.objects.get(pk=user.pk)

        bundle = self.build_bundle(obj=user, request=request)
        bundle = self.full_dehydrate(bundle)

        self.log_throttled_access(request)
        return self.create_response(request, bundle)