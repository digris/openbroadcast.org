import logging

from django.conf import settings
from django.utils.module_loading import import_by_path
from django.db import transaction
from django.core.exceptions import ValidationError

from django_auth_policy.models import (LoginAttempt, PasswordChange)

logger = logging.getLogger(__name__)


class PasswordStrengthPolicyHandler(object):
    """ Runs all policies related to password strength requirements
    Raises a ValidationError when a password doesn't comply
    """
    _policies = []
    policy_texts = []

    def __init__(self):
        if self._policies:
            return

        for policy_path, kwargs in settings.PASSWORD_STRENGTH_POLICIES:
            policy_class = import_by_path(policy_path)
            policy = policy_class(**kwargs)

            self._policies.append(policy)

            if policy.show_policy and policy.policy_text:
                self.policy_texts.append({
                    'text': policy.policy_text,
                    'caption': policy.policy_caption,
                })

    def validate(self, password, user):
        """ Validate password strength against all password policies.
        One should also provide the user that (will) use this password.
        Policies will raise a ValidationError when the password doesn't comply
        """
        for pol in self._policies:
            pol.validate(password, user)


class PasswordChangePolicyHandler(object):
    """ Runs all policies related to enforced password changes
    Raises a ValidationError when a user is enforced to change its password
    """
    _policies = []
    policy_texts = []

    def __init__(self):
        if self._policies:
            return

        for policy_path, kwargs in settings.PASSWORD_CHANGE_POLICIES:
            policy_class = import_by_path(policy_path)
            policy = policy_class(**kwargs)

            self._policies.append(policy)

    def validate(self, user):
        try:
            last_pw_change = PasswordChange.objects.filter(
                user=user, successful=True).order_by('-id')[0]
        except IndexError:
            last_pw_change = None

        for pol in self._policies:
            pol.validate(last_pw_change)

    def update_session(self, request, user):
        if not hasattr(request, 'session'):
            return

        try:
            self.validate(user)
        except ValidationError as exc:
            if request.session.get('password_change_enforce') != exc.code:
                logger.info(u'User %s must change password; %s',
                            user, exc.code)
            request.session['password_change_enforce'] = exc.code
            request.session['password_change_enforce_msg'] = \
                unicode(exc.message)
        else:
            request.session['password_change_enforce'] = False
            request.session['password_change_enforce_msg'] = None


class AuthenticationPolicyHandler(object):
    """ Runs all policies related to authentication
    Raises a ValidationError when an authentication attempt does not comply
    """
    _policies = []
    policy_texts = []

    def __init__(self):
        if self._policies:
            return

        for policy_path, kwargs in settings.AUTHENTICATION_POLICIES:
            policy_class = import_by_path(policy_path)
            policy = policy_class(**kwargs)

            self._policies.append(policy)

    def pre_auth_checks(self, username, password, remote_addr, host):
        """ Policy checks before a user is authenticated
        No `User` instance is available yet

        Raises ValidationError for failed login attempts
        On success it returns a LoginAttempt instance

        `username` must be a string that uniquely identifies a user.
        """
        logger.info('Authentication attempt, username=%s, address=%s',
                    username, remote_addr)

        with transaction.atomic():
            username_len = LoginAttempt._meta.get_field('username').max_length
            hostname_len = LoginAttempt._meta.get_field('hostname').max_length
            attempt = LoginAttempt.objects.create(
                username=username[:username_len] if username else '-',
                source_address=remote_addr,
                hostname=host[:hostname_len],
                successful=False,
                lockout=True)

        for pol in self._policies:
            pol.pre_auth_check(attempt, password)

        return attempt

    def post_auth_checks(self, attempt):
        """ Policy checks after the user has been authenticated.
        The attempt should now have a `user`
        """
        for pol in self._policies:
            pol.post_auth_check(attempt)

        # Authentication was successful
        logger.info(u'Authentication success, username=%s, address=%s',
                    attempt.username, attempt.source_address)

        attempt.successful = True
        attempt.lockout = False
        attempt.save()

        for pol in self._policies:
            pol.auth_success(attempt)

        return attempt
