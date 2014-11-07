from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_delete
from registration.signals import user_activated
from device.models import Device

import logging
log = logging.getLogger(__name__)

class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, related_name='profiles', null=True, blank=True, on_delete=models.SET_NULL)
    email_confirmed = models.BooleanField(default=False)

    full_name = models.CharField(max_length=256, null=True, blank=True)

    # additional fields, API-wise handled through hydrate
    date_of_birth = models.DateField(null=True, blank=True)
    weight = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)

    MEASUREMENT_SYSTEM_CHOICES = (
        ('metric', _('Metric')),
        ('imperial', _('Imperial')),
    )

    measurement_system = models.CharField(max_length=20, default='metric', choices=MEASUREMENT_SYSTEM_CHOICES)

    def __unicode__(self):
        return self.user.email


def pre_delete_user_profile(sender, **kwargs):
    obj = kwargs['instance']
    try:
        if obj.device:
            log.info('cascading profile deletion. will delete device as well: %s' % obj.device.serial_number)
            obj.device.delete()
    except:
        # device already deleted
        pass

def post_delete_user_profile(sender, **kwargs):
    obj = kwargs['instance']
    try:
        if obj.user:
            log.info('cascading profile deletion. will delete user as well: %s' % obj.user.email)
            obj.user.delete()
    except Exception, e:
        log.warning('unable to cascade delete to user %s' % e)


pre_delete.connect(pre_delete_user_profile, sender=UserProfile)
post_delete.connect(post_delete_user_profile, sender=UserProfile)



def confirm_email(sender, user, request, **kwarg):

    user.profile.email_confirmed = True
    user.profile.save()

    log.info('email confirmed for %s' % user.email)


def signals_import():
    """ A note on signals.

    The signals need to be imported early on so that they get registered
    by the application. Putting the signals here makes sure of this since
    the models package gets imported on the application startup.
    """
    from tastypie.models import create_api_key
    try:
        models.signals.post_save.connect(create_api_key, sender=User)
    except Exception, e:
        log.warning('errr creating api-key: %s' % e)

    user_activated.connect(confirm_email)


signals_import()