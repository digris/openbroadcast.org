from __future__ import unicode_literals

from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Model


class ChangeTrackerModelRegistry(object):
    """
    A registry that keeps track of the models that use ChangeTracker to track changes.
    """
    def __init__(self, create=True, update=True, delete=True, custom=None):
        from changetracker.receivers import tracker_create, tracker_update, tracker_delete

        self._registry = {}
        self._signals = {}

#        if create:
#            self._signals[post_save] = tracker_create
        if update:
            self._signals[pre_save] = tracker_update
#        if delete:
#            self._signals[post_delete] = tracker_delete

        if custom is not None:
            self._signals.update(custom)

    def register(self, model, include_fields=None, exclude_fields=None, diff_function=None):
        """
        Register a model with changetracker. ChangeTracker will then track mutations on this model's instances.

        :param model: The model to register.
        :type model: Model
        :param include_fields: The fields to include. Implicitly excludes all other fields.
        :type include_fields: list
        :param exclude_fields: The fields to exclude. Overrides the fields to include.
        :type exclude_fields: list
        """

        include_fields = include_fields or []
        exclude_fields = exclude_fields or []

        if issubclass(model, Model):
            self._registry[model] = {
                'include_fields': include_fields,
                'exclude_fields': exclude_fields,
            }


            self._connect_signals(model, diff_function)
        else:
            raise TypeError("Supplied model is not a valid model.")

    def contains(self, model):
        """
        Check if a model is registered with changetracker.

        :param model: The model to check.
        :type model: Model
        :return: Whether the model has been registered.
        :rtype: bool
        """
        return model in self._registry

    def unregister(self, model):
        """
        Unregister a model with changetracker. This will not affect the database.

        :param model: The model to unregister.
        :type model: Model
        """
        try:
            del self._registry[model]
        except KeyError:
            pass
        else:
            self._disconnect_signals(model)

    def _connect_signals(self, model, diff_function):
        """
        Connect signals for the model.
        """
        for signal in self._signals:
            receiver = self._signals[signal]

            kwargs = {
                #'diff_function': diff_function,
            }

            signal.connect(receiver, sender=model, dispatch_uid=self._dispatch_uid(signal, model), **kwargs)

    def _disconnect_signals(self, model):
        """
        Disconnect signals for the model.
        """
        for signal, receiver in self._signals:
            signal.disconnect(dispatch_uid=self._dispatch_uid(signal, model))

    def _dispatch_uid(self, signal, model):
        """
        Generate a dispatch_uid.
        """
        return (self.__class__, model, signal)

    def get_model_fields(self, model):

        return {
            'include_fields': self._registry[model]['include_fields'],
            'exclude_fields': self._registry[model]['exclude_fields'],
        }


tracker = ChangeTrackerModelRegistry()