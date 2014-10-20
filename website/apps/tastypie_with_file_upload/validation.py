from django.core.exceptions import ImproperlyConfigured


class Validation(object):
    """
    A basic validation stub that does no validation.
    """
    def __init__(self, **kwargs):
        pass

    def is_valid(self, bundle, request=None):
        """
        Performs a check on the data within the bundle (and optionally the
        request) to ensure it is valid.

        Should return a dictionary of error messages. If the dictionary has
        zero items, the data is considered valid. If there are errors, keys
        in the dictionary should be field names and the values should be a list
        of errors, even if there is only one.
        """
        return {}


class FormValidation(Validation):
    """
    A validation class that uses a Django ``Form`` to validate the data.

    This class **DOES NOT** alter the data sent, only verifies it. If you
    want to alter the data, please use the ``CleanedDataFormValidation`` class
    instead.

    This class requires a ``form_class`` argument, which should be a Django
    ``Form`` (or ``ModelForm``, though ``save`` will never be called) class.
    This form will be used to validate the data in ``bundle.data``.
    """
    def __init__(self, **kwargs):
        if not 'form_class' in kwargs:
            raise ImproperlyConfigured("You must provide a 'form_class' to 'FormValidation' classes.")

        self.form_class = kwargs.pop('form_class')
        super(FormValidation, self).__init__(**kwargs)

    def is_valid(self, bundle, request=None):
        """
        Performs a check on ``bundle.data``to ensure it is valid.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """
        data = bundle.data

        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}

        form = self.form_class(data)

        if form.is_valid():
            return {}

        # The data is invalid. Let's collect all the error messages & return
        # them.
        return form.errors


class CleanedDataFormValidation(FormValidation):
    """
    A validation class that uses a Django ``Form`` to validate the data.

    This class **ALTERS** data sent by the user!!!

    This class requires a ``form_class`` argument, which should be a Django
    ``Form`` (or ``ModelForm``, though ``save`` will never be called) class.
    This form will be used to validate the data in ``bundle.data``.
    """
    def is_valid(self, bundle, request=None):
        """
        Checks ``bundle.data``to ensure it is valid & replaces it with the
        cleaned results.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """
        data = bundle.data

        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}

        form = self.form_class(data)

        if form.is_valid():
            # We're different here & relying on having a reference to the same
            # bundle the rest of the process is using.
            bundle.data = form.cleaned_data
            return {}

        # The data is invalid. Let's collect all the error messages & return
        # them.
        return form.errors


###############################################################################

# The following is to fix a bug in tastypie
# see https://github.com/toastdriven/django-tastypie/issues/152

from django.forms.models import ModelChoiceField

class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                if one_uri[-1] == '/': # /api/v1/<resource_name>/<pk>/
                    converted.append(int(one_uri.split('/')[-2]))
                else: # /api/v1/<resource_name>/<pk>
                    converted.append(int(one_uri.split('/')[-1]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
        # copy data, so we don't modify the bundle
        data = data.copy()

        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])

        # validate and return messages on error
        form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors



###############################################################################

# The following is an addition

class FormValidationExcluding(FormValidation):
    """
    An extension of FormValidation that allows to specify a list of fields
    that should not be validated. This is useful for ForeignKey, as the
    validation would fail if passed by ID rather than URL, because their
    actual URL is built by alter_deserialized_detail_data AFTER validation
    has taken place.
    """
    def __init__(self, **kwargs):
        if 'exclude' in kwargs:
            self.exclude = kwargs.pop('exclude')
        else:
            self.exclude = []
        super(FormValidationExcluding, self).__init__(**kwargs)

    def is_valid(self, bundle, request=None):
        errors = super(FormValidationExcluding, self).is_valid(bundle, request)
        for field_not_to_validate in self.exclude:
            errors.pop(field_not_to_validate, None)
        return errors
