from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class LoginAttemptManager(models.Manager):
    def unlock(self, usernames=[], addresses=[]):
        """ Unlocks given usernames and IP addresses

        Returns the number of attempts that have been unlocked.
        """
        if not usernames and not addresses:
            return 0

        selection = models.Q()

        if usernames:
            selection |= models.Q(username__in=set(usernames))

        if addresses:
            selection |= models.Q(source_address__in=set(addresses))

        return self.get_query_set().filter(selection,
                                           lockout=True).update(lockout=False)

    def unlock_queryset(self, queryset):
        """ Unlocks all usernames and IP addresses found in ``queryset``

        Returns the number of attempts that have been unlocked.
        """
        selected_attempts = queryset.filter(
            lockout=True).order_by().values_list('username', 'source_address')

        if not selected_attempts:
            return 0

        usernames, addresses = zip(*selected_attempts)

        return self.unlock(usernames=usernames, addresses=addresses)


class LoginAttempt(models.Model):
    username = models.CharField(_('username'), max_length=100, db_index=True)
    source_address = models.GenericIPAddressField(
        _('source address'), protocol='both', db_index=True)
    hostname = models.CharField(_('hostname'), max_length=100)
    successful = models.BooleanField(_('successful'), default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             verbose_name=_('user'), on_delete=models.PROTECT)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True,
                                     default=timezone.now, db_index=True)
    # This is enabled for all failed login attempts. It is reset for every
    # successful login and can be reset by 'user admins'.
    lockout = models.BooleanField(_('lockout'), default=True,
                                  help_text=_('Counts towards lockout count'))

    objects = LoginAttemptManager()

    class Meta:
        verbose_name = _('login attempt')
        verbose_name_plural = _('login attempts')
        ordering = ('-id',)
        permissions = (
            ('unlock', _('Unlock by username or IP address')),
            )

    def __unicode__(self):
        return u'{0} at {1} from {2}'.format(self.username,
                                             self.timestamp,
                                             self.source_address)


class PasswordChangeAdmin(models.Manager):
    def set_temporary_password(self, user):
        """Returns a random password and sets this as temporary password for
        provided user."""
        # Characters used to generate temporary passwords
        allowed_chars = getattr(settings, 'TEMP_PASSWORD_CHARS',
                                'abcdefghijlkmnopqrstuvwxyz'
                                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                '0123456789')
        # Temporary password length
        length = getattr(settings, 'TEMP_PASSWORD_LENGTH', 12)

        password = get_random_string(length, allowed_chars)

        PasswordChange.objects.create(user=user, is_temporary=True,
                                      successful=True)
        user.set_password(password)
        user.save()

        return password


class PasswordChange(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             on_delete=models.PROTECT)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True,
                                     default=timezone.now)
    successful = models.BooleanField(_('successful'), default=False)
    # 'is_temporary is used by 'user managers' to set a temporary password
    # for a user, this password must be changed at first login
    is_temporary = models.BooleanField(_('is temporary'), default=False)
    # Optionally keep password a history of hashes to prevent users from
    # reusing old passwords. FIXME This has *NOT* been implemented
    password = models.CharField(_('password'), max_length=128, default='',
                                editable=False)

    objects = PasswordChangeAdmin()

    class Meta:
        verbose_name = _('password change')
        verbose_name_plural = _('password changes')
        ordering = ('-id',)

    def __unicode__(self):
        return u'{0} at {1}'.format(self.user, self.timestamp)


class UserChange(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'),
                             on_delete=models.PROTECT)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    by_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_('by user'),
                                related_name='changed_users',
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('user change')
        verbose_name_plural = _('user changes')
        ordering = ('-id',)

    def __unicode__(self):
        return u'{0} at {1} by {1}'.format(self.user, self.timestamp,
                                           self.by_user)
