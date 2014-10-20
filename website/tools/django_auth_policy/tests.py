# -*- coding: utf-8 -*-
import datetime
import logging
import collections
from cStringIO import StringIO

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model, SESSION_KEY
from django.core.urlresolvers import reverse
from django.utils import timezone

from django_auth_policy.models import LoginAttempt, PasswordChange
from django_auth_policy.forms import (StrictAuthenticationForm,
                                      StrictPasswordChangeForm,
                                      StrictSetPasswordForm)
from django_auth_policy.authentication import (AuthenticationLockedUsername,
                                               AuthenticationLockedRemoteAddress,
                                               AuthenticationDisableExpiredUsers)
from django_auth_policy.password_change import (PasswordChangeExpired,
                                                PasswordChangeTemporary)
from django_auth_policy.password_strength import (PasswordMinLength,
                                                  PasswordContainsUpperCase,
                                                  PasswordContainsLowerCase,
                                                  PasswordContainsNumbers,
                                                  PasswordContainsSymbols,
                                                  PasswordUserAttrs,
                                                  PasswordDisallowedTerms)


class LoginTests(TestCase):
    urls = 'django_auth_policy.testsite.urls'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='rf',
            email='rf@example.rf',
            password='password')

        self.factory = RequestFactory()

        self.logger = logging.getLogger()
        self.old_stream = self.logger.handlers[0].stream
        self.logger.handlers[0].stream = StringIO()

    def tearDown(self):
        self.logger.handlers[0].stream = self.old_stream

    def test_success(self):
        """ Test view with form and successful login """
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('login'), data={
            'username': 'rf', 'password': 'password'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(SESSION_KEY in self.client.session)
        self.assertEqual(self.client.session[SESSION_KEY], self.user.id)

        attempts = LoginAttempt.objects.filter(username=self.user.username,
                                               successful=True)

        self.assertEqual(attempts.count(), 1)

        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication success, username=rf, address=127.0.0.1\n'
            u'INFO User rf must change password; password-expired\n'))

    def test_username_lockout(self):
        """ Test too many failed login attempts for one username """
        pol = AuthenticationLockedUsername()
        text = unicode(pol.validation_msg)
        for x in xrange(0, pol.max_failed):

            req = self.factory.get(reverse('login'))
            req.META['REMOTE_ADDR'] = '10.0.0.%d' % (x + 1)

            form = StrictAuthenticationForm(request=req, data={
                'username': 'rf', 'password': 'wrong password'})

            self.assertEqual(form.non_field_errors(), [
                form.error_messages['invalid_login'] % {
                    'username': form.username_field.verbose_name}]
            )

        attempts = LoginAttempt.objects.filter(username=self.user.username,
                                               successful=False, lockout=True)

        self.assertEqual(attempts.count(),
                         pol.max_failed)

        # Another failed authentication triggers lockout
        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'wrong password'})
        self.assertEqual(form.non_field_errors(), [text])

        self.assertEqual(attempts.count(),
                         pol.max_failed + 1)

        # Even valid authentication will no longer work now
        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'password'})
        self.assertFalse(form.is_valid())

        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf, address=10.0.0.1\n'
            u'INFO Authentication failure, username=rf, address=10.0.0.1, '
            u'invalid authentication.\n'
            u'INFO Authentication attempt, username=rf, address=10.0.0.2\n'
            u'INFO Authentication failure, username=rf, address=10.0.0.2, '
            u'invalid authentication.\n'
            u'INFO Authentication attempt, username=rf, address=10.0.0.3\n'
            u'INFO Authentication failure, username=rf, address=10.0.0.3, '
            u'invalid authentication.\n'
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication failure, username=rf, address=127.0.0.1, '
            u'username locked\n'
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication failure, username=rf, address=127.0.0.1, '
            u'username locked\n'))

    def test_address_lockout(self):
        """ Test too many failed login attempts for one address """
        pol = AuthenticationLockedRemoteAddress()
        text = unicode(pol.validation_msg)

        addr = '1.2.3.4'

        for x in xrange(0, pol.max_failed):

            req = self.factory.get(reverse('login'))
            req.META['REMOTE_ADDR'] = addr

            form = StrictAuthenticationForm(request=req, data={
                'username': 'rf%d' % x, 'password': 'wrong password'})

            self.assertEqual(form.non_field_errors(), [
                form.error_messages['invalid_login'] % {
                    'username': form.username_field.verbose_name}]
            )

        attempts = LoginAttempt.objects.filter(source_address=addr,
                                               successful=False, lockout=True)

        self.assertEqual(attempts.count(), pol.max_failed)

        # Another failed authentication triggers lockout
        req = self.factory.get(reverse('login'))
        req.META['REMOTE_ADDR'] = addr
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'wrong password'})
        self.assertEqual(form.non_field_errors(), [text])

        self.assertEqual(attempts.count(), pol.max_failed + 1)

        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf0, address=1.2.3.4\n'
            u'INFO Authentication failure, username=rf0, address=1.2.3.4, '
            u'invalid authentication.\n'
            u'INFO Authentication attempt, username=rf1, address=1.2.3.4\n'
            u'INFO Authentication failure, username=rf1, address=1.2.3.4, '
            u'invalid authentication.\n'
            u'INFO Authentication attempt, username=rf2, address=1.2.3.4\n'
            u'INFO Authentication failure, username=rf2, address=1.2.3.4, '
            u'invalid authentication.\n'
            u'INFO Authentication attempt, username=rf, address=1.2.3.4\n'
            u'INFO Authentication failure, username=rf, address=1.2.3.4, '
            u'address locked\n'))

    def test_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        # Valid authentication data, but user is inactive
        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'password'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), [
            form.error_messages['invalid_login'] % {
                'username': form.username_field.verbose_name
            }]
        )

        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication failure, username=rf, address=127.0.0.1, '
            u'user inactive.\n'))

    def test_lock_period(self):
        pol = AuthenticationLockedUsername()
        text = unicode(pol.validation_msg)
        for x in xrange(0, pol.max_failed + 1):

            req = self.factory.get(reverse('login'))

            form = StrictAuthenticationForm(request=req, data={
                'username': 'rf', 'password': 'wrong password'})

            self.assertFalse(form.is_valid())

        # User locked out
        self.assertEqual(form.non_field_errors(), [text])

        # Alter timestamps as if they happened longer ago
        period = datetime.timedelta(seconds=pol.lockout_duration)
        expire_at = timezone.now() - period
        LoginAttempt.objects.all().update(timestamp=expire_at)

        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'password'})
        self.assertTrue(form.is_valid())

        # Successful login resets lock count
        locking_attempts = LoginAttempt.objects.filter(lockout=True)
        self.assertEqual(locking_attempts.count(), 0)

    def test_unlock(self):
        """ Resetting lockout data unlocks user """
        pol = AuthenticationLockedUsername()
        text = unicode(pol.validation_msg)
        for x in xrange(0, pol.max_failed + 1):

            req = self.factory.get(reverse('login'))

            form = StrictAuthenticationForm(request=req, data={
                'username': 'rf', 'password': 'wrong password'})

            self.assertFalse(form.is_valid())

        # User locked out
        self.assertEqual(form.non_field_errors(), [text])

        # Unlock user or address
        LoginAttempt.objects.all().update(lockout=False)

        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'password'})
        self.assertTrue(form.is_valid())


class UserExpiryTests(TestCase):
    urls = 'django_auth_policy.testsite.urls'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='rf',
            email='rf@example.rf',
            password='password')

        self.factory = RequestFactory()

        self.logger = logging.getLogger()
        self.old_stream = self.logger.handlers[0].stream
        self.logger.handlers[0].stream = StringIO()

    def tearDown(self):
        self.logger.handlers[0].stream = self.old_stream

    def test_expiry(self):
        pol = AuthenticationDisableExpiredUsers()

        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'password'})
        self.assertTrue(form.is_valid())

        # Simulate user didn't log in for a long time
        period = datetime.timedelta(days=pol.inactive_period)
        expire_at = timezone.now() - period
        self.user.last_login = expire_at
        self.user.save()
        LoginAttempt.objects.all().update(timestamp=expire_at)

        # Login attempt disabled user
        req = self.factory.get(reverse('login'))
        form = StrictAuthenticationForm(request=req, data={
            'username': 'rf', 'password': 'password'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_field_errors(), [
            form.error_messages['invalid_login'] % {
                'username': form.username_field.verbose_name
            }]
        )

        # Check log messages
        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication success, username=rf, address=127.0.0.1\n'
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO User rf disabled because last login was at %s\n'
            u'INFO Authentication failure, username=rf, address=127.0.0.1, '
            u'user inactive.\n' % expire_at))


class PasswordChangeTests(TestCase):
    urls = 'django_auth_policy.testsite.urls'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='rf',
            email='rf@example.rf',
            password='password')

        self.factory = RequestFactory()

        self.logger = logging.getLogger()
        self.old_stream = self.logger.handlers[0].stream
        self.logger.handlers[0].stream = StringIO()

    def tearDown(self):
        self.logger.handlers[0].stream = self.old_stream

    def test_expiry(self):
        pol = PasswordChangeExpired()

        # Create one recent password change
        pw = PasswordChange.objects.create(user=self.user, successful=True,
                                           is_temporary=False)

        # Redirect to login
        resp = self.client.get(reverse('login_required_view'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request['PATH_INFO'], reverse('login'))

        # Login
        resp = self.client.post(reverse('login'), data={
            'username': 'rf', 'password': 'password'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(SESSION_KEY in self.client.session)
        self.assertEqual(self.client.session[SESSION_KEY], self.user.id)
        self.assertTrue('password_change_enforce' in self.client.session)
        self.assertFalse(self.client.session['password_change_enforce'])
        self.assertFalse(self.client.session['password_change_enforce_msg'])
        self.assertNotContains(resp, 'new_password1')

        # Test if login worked ok
        resp = self.client.get(reverse('login_required_view'), follow=False)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.request['PATH_INFO'], '/')

        # Logout
        resp = self.client.get(reverse('logout'), follow=True)
        self.assertFalse(SESSION_KEY in self.client.session)

        # Move PasswordChange into the past
        period = datetime.timedelta(days=pol.max_age)
        expire_at = timezone.now() - period
        pw.timestamp = expire_at
        pw.save()

        # Login will still work
        resp = self.client.post(reverse('login'), data={
            'username': 'rf', 'password': 'password'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(SESSION_KEY in self.client.session)
        self.assertEqual(self.client.session[SESSION_KEY], self.user.id)
        self.assertTrue('password_change_enforce' in self.client.session)
        self.assertEqual(self.client.session['password_change_enforce'],
                         'password-expired')
        self.assertEqual(self.client.session['password_change_enforce_msg'],
                         unicode(pol.text))
        self.assertContains(resp, 'old_password')
        self.assertContains(resp, 'new_password1')
        self.assertContains(resp, 'new_password2')

        # And try requesting a different page still displays a change
        # password view
        resp = self.client.get(reverse('another_view'), follow=False)
        self.assertTrue('password_change_enforce' in self.client.session)
        self.assertEqual(self.client.session['password_change_enforce'],
                         'password-expired')
        self.assertContains(resp, 'old_password')
        self.assertContains(resp, 'new_password1')
        self.assertContains(resp, 'new_password2')

        # Post a new password
        resp = self.client.post(reverse('login_required_view'), data={
            'old_password': 'password',
            'new_password1': 'abcABC123!@#',
            'new_password2': 'abcABC123!@#'}, follow=True)
        self.assertFalse(self.client.session['password_change_enforce'])
        self.assertNotContains(resp, 'old_password')
        self.assertNotContains(resp, 'new_password1')
        self.assertNotContains(resp, 'new_password2')
        self.assertEqual(resp.redirect_chain, [('http://testserver/', 302)])

        # Recheck, change password view should be gone
        resp = self.client.get(reverse('login_required_view'), follow=False)
        self.assertNotContains(resp, 'old_password')
        self.assertNotContains(resp, 'new_password1')
        self.assertNotContains(resp, 'new_password2')

        # Logging tests
        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication success, username=rf, address=127.0.0.1\n'
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication success, username=rf, address=127.0.0.1\n'
            u'INFO User rf must change password; password-expired\n'
            u'INFO Password change successful for user rf\n'))

    def test_temporary_password(self):
        pol = PasswordChangeTemporary()
        # Create one recent password change
        PasswordChange.objects.create(user=self.user, successful=True,
                                      is_temporary=True)

        # Login
        resp = self.client.post(reverse('login'), data={
            'username': 'rf', 'password': 'password'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(SESSION_KEY in self.client.session)
        self.assertTrue('password_change_enforce' in self.client.session)
        self.assertEqual(self.client.session[SESSION_KEY], self.user.id)
        self.assertEqual(self.client.session['password_change_enforce'],
                         'password-temporary')
        self.assertEqual(self.client.session['password_change_enforce_msg'],
                         unicode(pol.text))

        # Requesting a page shows password change view
        resp = self.client.get(reverse('login_required_view'), follow=True)
        self.assertEqual(resp.request['PATH_INFO'], '/')
        self.assertContains(resp, 'old_password')
        self.assertContains(resp, 'new_password1')
        self.assertContains(resp, 'new_password2')

        # Change the password:
        resp = self.client.post(reverse('login_required_view'), data={
            'old_password': 'password',
            'new_password1': 'A-New-Passw0rd-4-me',
            'new_password2': 'A-New-Passw0rd-4-me'}, follow=True)
        self.assertEqual(resp.redirect_chain, [('http://testserver/', 302)])
        self.assertEqual(resp.request['PATH_INFO'], '/')
        self.assertNotContains(resp, 'old_password')
        self.assertNotContains(resp, 'new_password1')
        self.assertNotContains(resp, 'new_password2')

        self.assertEqual(PasswordChange.objects.all().count(), 2)
        self.assertEqual(PasswordChange.objects.filter(
            is_temporary=True).count(), 1)

        # Logging tests
        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            u'INFO Authentication attempt, username=rf, address=127.0.0.1\n'
            u'INFO Authentication success, username=rf, address=127.0.0.1\n'
            u'INFO User rf must change password; password-temporary\n'
            u'INFO Password change successful for user rf\n'))

    def password_change_login_required(self):
        resp = self.client.post(reverse('password_change'), follow=True)
        self.assertEqual(resp.redirect_chain, [
            ('http://testserver/login/?next=/password_change/', 302)])


class PasswordStrengthTests(TestCase):
    urls = 'django_auth_policy.testsite.urls'

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='rf',
            email='rf@example.rf',
            password='password')

        self.factory = RequestFactory()

        self.logger = logging.getLogger()
        self.old_stream = self.logger.handlers[0].stream
        self.logger.handlers[0].stream = StringIO()

    def tearDown(self):
        self.logger.handlers[0].stream = self.old_stream

    def test_password_length(self):
        pol = PasswordMinLength()

        new_passwd = 'Aa1.$Bb2.^Cc.Dd5%.Ee6&.Dd7*'
        short_passwd = new_passwd[:pol.min_length]

        # Too short password doesnt work
        form = StrictPasswordChangeForm(self.user, data={
            'old_password': 'password',
            'new_password1': short_passwd[:-1],
            'new_password2': short_passwd[:-1]})

        self.assertFalse(form.is_valid())
        msg = unicode(pol.policy_text)
        self.assertEqual(form.errors['new_password1'], [msg])

        # Longer password does work
        form = StrictPasswordChangeForm(self.user, data={
            'old_password': 'password',
            'new_password1': short_passwd,
            'new_password2': short_passwd})
        self.assertTrue(form.is_valid())

        # Check correct PasswordChange items were created
        self.assertEqual(PasswordChange.objects.all().count(), 2)
        self.assertEqual(PasswordChange.objects.filter(
            successful=True).count(), 1)
        self.assertEqual(PasswordChange.objects.filter(
            successful=False).count(), 1)

        # Logging tests
        self.assertEqual(self.logger.handlers[0].stream.getvalue(), (
            'INFO Password change failed for user rf\n'
            'INFO Password change successful for user rf\n'))

    def test_password_complexity(self):
        # List of policies to check, this must match PasswordContains... items
        # of testsettings.PASSWORD_STRENGTH_POLICIES
        policies = collections.deque([
            PasswordContainsUpperCase(),
            PasswordContainsLowerCase(),
            PasswordContainsNumbers(),
            PasswordContainsSymbols(),
        ])
        for x in xrange(0, len(policies)):
            # Create a password with 4 chars from every policy except one
            passwd = u''.join([pol.chars[:4] for pol in list(policies)[:-1]])
            form = StrictPasswordChangeForm(self.user, data={
                'old_password': 'password',
                'new_password1': passwd,
                'new_password2': passwd})
            failing_policy = policies[-1]
            self.assertFalse(form.is_valid())
            err_msg = unicode(failing_policy.policy_text)
            self.assertEqual(form.errors['new_password1'], [err_msg])

            policies.rotate(1)

    def test_password_differ_old(self):
        """ Make sure new password differs from old password """
        passwd = 'Aa1.$Bb2.^Cc.Dd5%.Ee6&.Dd7*'
        self.user.set_password(passwd)
        self.user.save()

        form = StrictPasswordChangeForm(self.user, data={
            'old_password': passwd,
            'new_password1': passwd,
            'new_password2': passwd})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password1'],
                         [form.error_messages['password_unchanged']])

    def test_password_user_attrs(self):
        policy = PasswordUserAttrs()

        self.user.username = 'rf'
        self.user.email = 'rf@example.com'
        self.user.first_name = 'Rudolph'
        # Try names with accents:
        self.user.last_name = u'Frögér'
        self.user.save()

        passwds = [
            ('AbcDef#12Rudolph', False),
            ('1234rf#examplE', False),
            ('Rudolph#12345', False),
            # Should match froger with accents:
            (u'Froger#12345', False),
            # Short pieces are allowed, like 'rf':
            ('rf54321#AbCd', True),
        ]
        for passwd, valid in passwds:
            form = StrictSetPasswordForm(self.user, data={
                'new_password1': passwd,
                'new_password2': passwd})
            self.assertEqual(form.is_valid(), valid)
            if not valid:
                self.assertEqual(form.errors['new_password1'],
                                 [unicode(policy.text)])

    def test_password_disallowed_terms(self):
        policy = PasswordDisallowedTerms(terms=['Testsite'])

        passwds = [
            ('123TestSite###', False),
            ('123Site###Test', True),
        ]
        for passwd, valid in passwds:
            form = StrictSetPasswordForm(self.user, data={
                'new_password1': passwd,
                'new_password2': passwd})
            self.assertEqual(form.is_valid(), valid)
            if not valid:
                errs = [unicode(policy.policy_text)]
                self.assertEqual(form.errors['new_password1'], errs)
