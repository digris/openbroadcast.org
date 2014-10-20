import logging

from django.core.urlresolvers import resolve, reverse
from django.views.decorators.csrf import requires_csrf_token
from django.conf import settings
from django import http

from django_auth_policy.handlers import PasswordChangePolicyHandler
from django_auth_policy.forms import StrictPasswordChangeForm


logger = logging.getLogger(__name__)


class AuthenticationPolicyMiddleware(object):
    """ This middleware enforces the following policy:
    - Change of password when password has expired;
    - Change of password when user has a temporary password;
    - Logout disabled users;

    This is enforced using middleware to prevent users from accessing any page
    handled by Django without the policy being enforced.
    """

    change_password_path = reverse(getattr(
        settings, 'ENFORCED_PASSWORD_CHANGE_VIEW_NAME', 'password_change'))
    login_path = reverse(getattr(settings, 'LOGIN_VIEW_NAME', 'login'))
    logout_path = reverse(getattr(settings, 'LOGOUT_VIEW_NAME', 'logout'))

    password_change_policy_handler = PasswordChangePolicyHandler()

    def process_request(self, request):
        assert hasattr(request, 'user'), (
            'AuthenticationPolicyMiddleware needs a user attribute on '
            'request, add AuthenticationMiddleware before '
            'AuthenticationPolicyMiddleware in MIDDLEWARE_CLASSES')

        if not request.user.is_authenticated():
            return None

        # Log out disabled users
        if not request.user.is_active:
            logger.info('Log out inactive user, user=%s', request.user)
            view_func, args, kwargs = resolve(self.logout_path)
            return view_func(request, *args, **kwargs)

        # Do not do password change for certain URLs
        if request.path in (self.change_password_path, self.login_path,
                            self.logout_path):
            return None

        # Check for 'enforce_password_change' in session set by login view
        if request.session.get('password_change_enforce', False):
            return self.password_change(request)

        return None

    def process_response(self, request, response):
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            return response

        # When password change is enforced, check if this is still required
        # for next request
        if not request.session.get('password_change_enforce', False):
            return response

        self.password_change_policy_handler.update_session(
            request, request.user)

        return response

    def password_change(self, request):
        """ Return 'password_change' view.
        This resolves the view with the name 'password_change'.

        Overwrite this method when needed.
        """
        view_func, args, kwargs = resolve(self.change_password_path)

        if 'password_change_form' in kwargs:
            assert issubclass(kwargs['password_change_form'],
                              StrictPasswordChangeForm), (
                "Use django_auth_policy StrictPasswordChangeForm for password "
                "changes.")

        # Provide extra context to be used in the password_change template
        if 'extra_context' in kwargs:
            kwargs['extra_context']['password_change_enforce'] = \
                request.session.get('password_change_enforce')
            kwargs['extra_context']['password_change_enforce_msg'] = \
                request.session.get('password_change_enforce_msg')

        # Run 'requires_csrf_token' because CSRF middleware might have been
        # skipped over here
        return requires_csrf_token(view_func)(request, *args, **kwargs)


class LoginRequiredMiddleware(object):
    """ Middleware which enforces authentication for all requests.
    """
    login_path = reverse(getattr(settings, 'LOGIN_VIEW_NAME', 'login'))
    logout_path = reverse(getattr(settings, 'LOGOUT_VIEW_NAME', 'logout'))
    public_urls = getattr(settings, 'PUBLIC_URLS', [])
    public_urls.append(login_path)
    public_urls.append(logout_path)

    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise Exception('Install Authentication middleware before '
                            'LoginRequiredMiddleware')

        if request.user.is_authenticated():
            return None

        # Do not require authentication for certain URLs
        if request.path in self.public_urls:
            return None

        # Django should not serve STATIC files in production, but for
        # development this should be no problem
        if (settings.STATIC_URL and
                request.path.startswith(settings.STATIC_URL)):

            if settings.DEBUG:
                return None
            else:
                return http.HttpResponseForbidden('Login required')

        # When serving MEDIA files through Django we will not display a login
        # form, but instead return HTTP 403 Forbidden
        if (settings.MEDIA_URL and
                request.path.startswith(settings.MEDIA_URL)):

            return http.HttpResponseForbidden('Login required')

        view_func, args, kwargs = resolve(self.login_path)
        return requires_csrf_token(view_func)(request, *args, **kwargs)
