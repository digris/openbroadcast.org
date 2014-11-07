import os
import binascii
import re
import emailit.api
from django.conf import settings
from django.contrib.sites.models import Site

import logging
log = logging.getLogger(__name__)

MINIMUM_PASSWORD_LENGTH = 6
REGEX_VALID_PASSWORD = (
    ## Don't allow any spaces, e.g. '\t', '\n' or whitespace etc.
    r'^(?!.*[\s])'
    ## Check for a digit
    '((?=.*[\d])'
    ## Check for an uppercase letter
    '(?=.*[A-Z])'
    ## check for special characters. Something which is not word, digit or
    ## space will be treated as special character
    '(?=.*[^\w\d\s])).'
    ## Minimum 8 characters
    '{' + str(MINIMUM_PASSWORD_LENGTH) + ',}$')


def validate_password(password):
    if re.match(REGEX_VALID_PASSWORD, password):
        return True
    return False


def reset_password(user):

    site = Site.objects.get_current()

    log.info('password reset for %s - %s' % (user.pk, user.email))
    password = binascii.b2a_hex(os.urandom(4)).lower()
    user.set_password(password)
    user.save()
    context = {
        'password': password,
        'site': site,
    }
    emailit.api.send_mail([user.email], context, 'email/member/reset_password')

def send_activation_email(registration_profile):

    site = Site.objects.get_current()
    context = {
        'activation_key': registration_profile.activation_key,
        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        'site': site,
    }
    emailit.api.send_mail([registration_profile.user.email], context, 'email/member/activation')