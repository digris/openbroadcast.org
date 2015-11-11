from __future__ import unicode_literals
from django.conf import settings
import json

from changetracker.diff import model_instance_diff
#from changetracker.models import LogEntry


#TRACKED_MODELS = getattr(settings, 'CHANGETRACKER_TRACKED_MODELS', {})


def tracker_create(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is first saved to the database.

    Direct use is discouraged, connect your model through :py:func:`changetracker.registry.register` instead.
    """
    if created:
        changes = model_instance_diff(None, instance)

        log_entry = LogEntry.objects.log_create(
            instance,
            action=LogEntry.Action.CREATE,
            changes=json.dumps(changes),
        )


def tracker_update(sender, instance, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is changed and saved to the database.

    Direct use is discouraged, connect your model through :py:func:`changetracker.registry.register` instead.
    """

    print '/////////////////////////////////////////////'
    print sender
    print instance

    if instance.pk is not None:
        try:
            old = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            new = instance

            changes = model_instance_diff(old, new)

            print changes

            #
            # # Log an entry only if there are changes
            # if changes:
            #     log_entry = LogEntry.objects.log_create(
            #         instance,
            #         action=LogEntry.Action.UPDATE,
            #         changes=json.dumps(changes),
            #     )


def tracker_delete(sender, instance, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is deleted from the database.

    Direct use is discouraged, connect your model through :py:func:`changetracker.registry.register` instead.
    """
    if instance.pk is not None:
        changes = model_instance_diff(instance, None)

        log_entry = LogEntry.objects.log_create(
            instance,
            action=LogEntry.Action.DELETE,
            changes=json.dumps(changes),
        )