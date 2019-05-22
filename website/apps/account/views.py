from __future__ import unicode_literals


import logging
import json
from braces.views import AnonymousRequiredMixin, LoginRequiredMixin
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View, FormView, RedirectView, TemplateView
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlunquote

from .forms import (
    AuthenticationForm,
    RegistrationForm,
    PasswordResetForm,
    PasswordRequestResetForm,
)

log = logging.getLogger(__name__)


PICKUP_COOKIE_NAME = "login-pickup"



class SetPickupCookieMixin(View):

    pickup_cookie_name = PICKUP_COOKIE_NAME
    pickup_cookie_dict = None

    def dispatch(self, request, *args, **kwargs):

        redirect_to = self.request.GET.get(REDIRECT_FIELD_NAME)
        if redirect_to and is_safe_url(url=redirect_to, host=self.request.get_host()):
            self.pickup_cookie_dict = {
                "location": redirect_to,
            }
        else:
            self.pickup_cookie_dict = None

        return super(SetPickupCookieMixin, self).dispatch(request, *args, **kwargs)


    def render_to_response(self, context, **response_kwargs):

        response = super(SetPickupCookieMixin, self).render_to_response(context, **response_kwargs)

        if self.pickup_cookie_dict:
            response.set_cookie(PICKUP_COOKIE_NAME, json.dumps(self.pickup_cookie_dict))

        return response



class LogoutView(LoginRequiredMixin, RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        redirect_to = self.request.GET.get(REDIRECT_FIELD_NAME)
        if redirect_to and is_safe_url(url=redirect_to, host=self.request.get_host()):
            return redirect_to
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class LoginView(AnonymousRequiredMixin, SetPickupCookieMixin, FormView):
    """
    Provides the ability to login as a user with a username (or e-mail) and password
    """
    success_url = reverse_lazy('account:login-pickup')
    form_class = AuthenticationForm
    # redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'account/login_form.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)


class RegistrationView(AnonymousRequiredMixin, FormView):
    """
    Provides the ability to login as a user with a username (or e-mail) and password
    """
    success_url = reverse_lazy('account:login-pickup')
    form_class = RegistrationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'account/registration_form.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        new_user = form.save()
        new_user = authenticate(
            username=getattr(new_user, "username"),
            password=form.cleaned_data["password1"],
        )
        auth_login(self.request, new_user)
        # TODO: implement signals
        # signals.user_registered.send(sender=self.__class__, user=new_user, request=self.request)

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(RegistrationView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url

        if self.request.user and self.request.user.is_staff:
            redirect_to += '?toolbar_off'

        return redirect_to


class PasswordRecoverView(AnonymousRequiredMixin, FormView):

    form_class = PasswordRequestResetForm
    template_name = 'account/password_recover_form.html'

    def form_valid(self, form):

        print(form)

        form.save(
            subject_template_name='account/password_recover_email_subject.txt',
            email_template_name='account/password_recover_email.txt',
        )
        return super(PasswordRecoverView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account:password-recover-sent')


class PasswordRecoverSentView(AnonymousRequiredMixin, TemplateView):

    template_name = 'account/password_recover_sent.html'


class PasswordRecoverResetView(AnonymousRequiredMixin, FormView):
    form_class = PasswordResetForm
    token_expires = None
    template_name = 'account/password_recover_reset_form.html'
    success_url = reverse_lazy('account:login-pickup')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):

        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return self.invalid_token()

        if not default_token_generator.check_token(user, token):
            return self.invalid_token()

        self.user = user
        return super(PasswordRecoverResetView, self).dispatch(request, *args, **kwargs)




    def invalid_token(self):
        return self.render_to_response(self.get_context_data(invalid_token=True))

    def check_token(self, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return user is not None and default_token_generator.check_token(user, token)

    # def get(self, request, **kwargs):
    #     pass


    def get_form_kwargs(self):
        kwargs = super(PasswordRecoverResetView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(PasswordRecoverResetView, self).get_context_data(**kwargs)

        if 'invalid_token' not in ctx:

            uidb64 = self.kwargs.get('uidb64')
            token = self.kwargs.get('token')

            ctx.update({
                'uidb64': uidb64,
                'token': token,
                'valid': self.check_token(uidb64, token),
            })

        return ctx


    def form_valid(self, form):
        form.save()
        # not so nice, needed to force `authenticate`
        self.user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(self.request, self.user)
        return redirect(self.get_success_url())




class LoginPickupView(LoginRequiredMixin, View):

    pickup_cookie_name = PICKUP_COOKIE_NAME

    def get(self, request, *args, **kwargs):

        url = request.GET.get("next", "/")
        raw_cookie = self.request.COOKIES.get(self.pickup_cookie_name, None)

        if raw_cookie:
            try:
                cookie = json.loads(urlunquote(raw_cookie))
                url = cookie.get("location", "/")

            except Exception as e:
                log.warning(
                    "unable to decode login-pickup cookie: {}".format(e)
                )

        if request.user and request.user.is_staff:
            url += '?toolbar_off'

        response = redirect(url)
        response.delete_cookie(self.pickup_cookie_name)

        return response
