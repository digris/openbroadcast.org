import md5
import logging

from django.contrib.auth.models import User

from obp_legacy.models_legacy import ElggUsers as LegacyUser

log = logging.getLogger(__name__)


class LegacyBackend(object):
    """
    Authenticate against the 'legacy_legacy database'
    fortunately passwords there are stored md5-hashed
    also set password from legacy-db for new user in case of successful login.
    """

    def authenticate(self, username=None, password=None):

        log = logging.getLogger('%s.%s' % (__name__, 'authenticate'))
        log.info('legacy login: %s | %s' % (username, '*******************'))

        return self.legacy_auth(username, password)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    def legacy_auth(self, username=None, password=None):

        log = logging.getLogger('%s.%s' % (__name__, 'legacy_auth'))

        user = None
        try:
            lu = LegacyUser.objects.using('legacy_legacy').get(username=username,
                                                               password=md5.new(password).hexdigest())

        except LegacyUser.DoesNotExist:
            lu = None

        if lu:
            log.info('username : %s' % (lu.username))
            log.info('email    : %s' % (lu.email))
            log.info('pw md5   : %s' % (lu.password))

            try:
                user = User.objects.get(username=username)
                user.set_password(password)

            except User.DoesNotExist:
                pass

        return user

