import django
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse, resolve
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

from django_auth_policy.views import login
from django_auth_policy.user_admin import StrictUserAdmin
from django_auth_policy.admin import (LoginAttemptAdmin, admin_login,
                                      admin_password_change)
from django_auth_policy.forms import (StrictAuthenticationForm,
                                      StrictPasswordChangeForm)

user_model = get_user_model()


class Command(BaseCommand):
    help = "Checks if all settings for django_auth_policy are in place."

    def handle(self, *args, **options):
        self.check_middleware()
        self.check_settings()
        self.views()
        self.admin()

    def check_middleware(self):
        middle = 'django_auth_policy.middleware.AuthenticationPolicyMiddleware'
        d_middle = 'django.contrib.auth.middleware.AuthenticationMiddleware'
        m_classes = list(settings.MIDDLEWARE_CLASSES)
        if not middle in m_classes:
            self.stderr.write('WARNING: AuthenticationPolicyMiddleware is '
                              'missing in MIDDLEWARE_CLASSES')

        elif not d_middle in m_classes:
            self.stderr.write('WARNING: Djangos AuthenticationMiddleware is '
                              'missing in MIDDLEWARE_CLASSES')

        elif m_classes.index(d_middle) > m_classes.index(middle):
            self.stderr.write('WARNING: Djangos AuthenticationMiddleware must '
                              'come before AuthenticationPolicyMiddleware in '
                              'MIDDLEWARE_CLASSES')


        if not 'django.middleware.csrf.CsrfViewMiddleware' in m_classes:
            self.stderr.write('WARNING: CsrfViewMiddleware is missing in '
                              'MIDDLEWARE_CLASSES')

        clickjack = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
        if not clickjack in m_classes:
            self.stderr.write('WARNING: clickjacking protection using '
                              'XFrameOptionsMiddleware missing in '
                              'MIDDLEWARE_CLASSES')

    def check_settings(self):
        if not settings.X_FRAME_OPTIONS in ('DENY', 'SAMEORIGIN'):
            self.stderr.write('WARNING: X_FRAME_OPTIONS set to %s' %
                              settings.X_FRAME_OPTIONS)

        if not settings.SESSION_COOKIE_SECURE:
            self.stderr.write('WARNING: SESSION_COOKIE_SECURE is set to False')

        if not settings.SESSION_COOKIE_HTTPONLY:
            self.stderr.write('WARNING: SESSION_COOKIE_HTTPONLY is set to False')

        if settings.SESSION_COOKIE_AGE > 60 * 60 * 24:
            self.stderr.write('WARNING: SESSION_COOKIE_AGE is set to more '
                              'than 24 hours')
        else:
            self.stdout.write('INFO: SESSION_COOKIE_AGE is set to %d seconds' %
                              settings.SESSION_COOKIE_AGE)

        if not settings.CSRF_COOKIE_SECURE:
            self.stderr.write('WARNING: CSRF_COOKIE_SECURE is set to False')

        if (django.VERSION[0] >= 1 and django.VERSION[1] >= 6 and
            not settings.CSRF_COOKIE_HTTPONLY):

            self.stderr.write('WARNING: CSRF_COOKIE_HTTPONLY is set to False')

        if settings.DEBUG:
            self.stderr.write('WARNING: DEBUG is set to True')

        if settings.TEMPLATE_DEBUG:
            self.stderr.write('WARNING: TEMPLATE_DEBUG is set to True')


    def views(self):
        # Check login view
        url = reverse('login')
        if url != settings.LOGIN_URL:
            self.stderr.write('WARNING: login URL not equal to '
                              'settings.LOGIN_URL')

        func, args, kwargs = resolve(url)
        if func != login:
            self.stderr.write('WARNING: login view isn\'t the '
                              'django_auth_policy.views.login view')

        if 'authentication_form' in kwargs:
            if not issubclass(kwargs['authentication_form'],
                              StrictAuthenticationForm):
                self.stderr.write('WARNING: login view doesn\'t use '
                                  'the StrictAuthenticationForm')
        else:
            self.stderr.write('WARNING: could not check if login view uses '
                              'the StrictAuthenticationForm')

        # Check password change view
        url = reverse(getattr(settings, 'ENFORCED_PASSWORD_CHANGE_VIEW_NAME',
                              'password_change'))
        func, args, kwargs = resolve(url)
        if 'password_change_form' in kwargs:
            if not issubclass(kwargs['password_change_form'],
                              StrictPasswordChangeForm):
                self.stderr.write('WARNING: password_change view doesn\'t use '
                                  'the StrictPasswordChangeForm')
        else:
            self.stderr.write('WARNING: could not check if password_change '
                              'view uses the StrictAuthenticationForm')

    def admin(self):
        if not 'django.contrib.admin' in settings.INSTALLED_APPS:
            return

        # Check login view
        if admin.site.login != admin_login:
            self.stderr.write('WARNING: admin doesn\'t use the '
                              'django_auth_policy admin_login view')

        if not issubclass(admin.site.login_form, StrictAuthenticationForm):
            self.stderr.write('WARNING: admin doesn\'t use the '
                              'django_auth_policy StrictAuthenticationForm')

        # Check password change
        if not admin.site.password_change == admin_password_change:
            self.stderr.write('WARNING: admin doesn\'t use the '
                              'django_auth_policy admin_password_change view')

        # Check UserAdmin
        if not getattr(settings, 'REPLACE_AUTH_USER_ADMIN', True):
            # Replacing disabled
            pass
        elif not user_model in admin.site._registry:
            self.stderr.write('WARNING: Could not check if user admin '
                              'doesn\'t use django_auth_policy\'s '
                              'StrictUserAdmin')
        elif not isinstance(admin.site._registry[user_model], StrictUserAdmin):
            self.stderr.write('WARNING: User admin doesn\'t use '
                              'django_auth_policy\'s StrictUserAdmin')
