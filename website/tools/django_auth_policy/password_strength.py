import unicodedata
import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django_auth_policy import BasePolicy


def _normalize_unicode(value):
    value = unicodedata.normalize('NFKD', unicode(value))
    return value.encode('ascii', 'ignore').strip().lower()


class PasswordStrengthPolicy(BasePolicy):
    """ Password strength policy classes must implement:

    `validate` a method which accept a password and the related user and raises
    a validation error when the password doesn't validate the policy.

    Optionally:

    `policy_text` a property which returns a short text to be displayed in
    password policy explenations

    `policy_caption` a property which returns a short caption to be displayed
    with the password policy.
    """
    show_policy = True

    def validate(self, value, user):
        raise NotImplemented()

    @property
    def policy_text(self):
        return None

    @property
    def policy_caption(self):
        return None


class PasswordMinLength(PasswordStrengthPolicy):
    min_length = 10
    text = _('Passwords must be at least {min_length} characters in length.')

    def validate(self, value, user):
        if self.min_length is None:
            return

        if len(value) < self.min_length:
            msg = self.text.format(min_length=self.min_length)
            raise ValidationError(msg, code='password_min_length')

    @property
    def policy_text(self):
        return self.text.format(min_length=self.min_length)


class PasswordContains(PasswordStrengthPolicy):
    """ Base class which validates if passwords contain at least a certain
    number of characters from a certain set.
    """
    chars = None
    min_count = 1
    text = None
    plural_text = None

    def validate(self, value, user):
        pw_set = set(value)
        if len(pw_set.intersection(self.chars)) < self.min_count:
            raise ValidationError(self.text, 'password_complexity')

    @property
    def policy_text(self):
        if self.min_count > 1:
            return self.plural_text.format(min_count=self.min_count)
        else:
            return self.text.format(min_count=self.min_count)

    @property
    def policy_caption(self):
        return self.chars


class PasswordContainsUpperCase(PasswordContains):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = _('Passwords must have at least one lowercase character')
    plural_text = _('Passwords must have at least {min_count} '
                    'lowercase characters')


class PasswordContainsLowerCase(PasswordContains):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    text = _('Passwords must have at least one uppercase character')
    plural_text = _('Passwords must have at least {min_count} '
                    'uppercase characters')


class PasswordContainsNumbers(PasswordContains):
    chars = '0123456789'
    text = _('Passwords must have at least one number')
    plural_text = _('Passwords must have at least {min_count} '
                    'numbers')


class PasswordContainsSymbols(PasswordContains):
    chars = '!@#$%^&*()_+-={}[]:;"\'|\\,.<>?/~` '
    text = _('Passwords must have at least one special character (punctuation)')
    plural_text = _('Passwords must have at least {min_count} special '
                    'characters (punctuation)')


class PasswordContainsAlphabetics(PasswordContains):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = _('Passwords must have at least one alphabetic character')
    plural_text = _('Passwords must have at least {min_count} '
                    'alphabetic characters')


class PasswordUserAttrs(PasswordStrengthPolicy):
    """ Validate if password doesn't contain values from a list of user
    attributes. Every attribute will be normalized into ascii and split
    on non alphanumerics.

    Use this in the clean method of password forms

    `value`: password
    `user`: user object with attributes

    Example, which would raise a ValidationError:

        user.first_name = 'John'
        password_user_attrs('johns_password', user)
    """
    user_attrs = ('email', 'first_name', 'last_name', 'username')
    text = _('Passwords are not allowed to contain (pieces of) your name '
             'or email.')

    _non_alphanum = re.compile(r'[^a-z0-9]')

    def validate(self, value, user):
        simple_pass = _normalize_unicode(value)
        for attr in self.user_attrs:
            v = getattr(user, attr, None)
            if not attr or len(attr) < 4:
                continue

            v = _normalize_unicode(v)

            for piece in self._non_alphanum.split(v):
                if len(piece) < 4:
                    continue

                if piece in simple_pass:
                    raise ValidationError(self.text, 'password_user_attrs')

    @property
    def policy_text(self):
        return self.text


class PasswordDisallowedTerms(PasswordStrengthPolicy):
    """ Disallow a (short) list of terms in passwords
    Ideal for too obvious terms like the name of the site or company
    """
    terms = None
    text = _('Passwords are not allowed to contain the following term(s): '
             '{terms}')
    show_policy = False

    def __init__(self, **kwargs):
        terms = kwargs.pop('terms')
        self.terms = [_normalize_unicode(term) for term in terms]

        super(PasswordDisallowedTerms, self).__init__(**kwargs)

    def validate(self, value, user):
        simple_pass = _normalize_unicode(value)
        found = []
        for term in self.terms:
            if term in simple_pass:
                found.append(term)

        if found:
            msg = self.text.format(terms=u', '.join(found))
            raise ValidationError(msg, 'password_disallowed_terms')

    @property
    def policy_text(self):
        return self.text.format(terms=u', '.join(self.terms))
