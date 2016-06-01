#-*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now

from postman.models import Message, STATUS_PENDING, STATUS_ACCEPTED

def pm_broadcast(sender, recipients, subject, body='', skip_notification=False):
    """
    Broadcast a message to multiple Users.
    For an easier cleanup, all these messages are directly marked as archived
    and deleted on the sender side.
    The message is expected to be issued from a trusted application, so moderation
    is not necessary and the status is automatically set to 'accepted'.

    Optional argument:
        ``skip_notification``: if the normal notification event is not wished
    """
    message = Message(subject=subject, body=body, sender=sender,
        sender_archived=True, sender_deleted_at=now(),
        moderation_status=STATUS_ACCEPTED, moderation_date=now())
    if not isinstance(recipients, (tuple, list)):
        recipients = (recipients,)
    for recipient in recipients:
        message.recipient = recipient
        message.pk = None
        message.save()
        if not skip_notification:
            message.notify_users(STATUS_PENDING)

def pm_write(sender, recipient, subject, body='', skip_notification=False,
        auto_archive=False, auto_delete=False, auto_moderators=None):
    """
    Write a message to a User.
    Contrary to pm_broadcast(), the message is archived and/or deleted on
    the sender side only if requested.
    The message may come from an untrusted application, a gateway for example,
    so it may be useful to involve some auto moderators in the processing.

    Optional arguments:
        ``skip_notification``: if the normal notification event is not wished
        ``auto_archive``: to mark the message as archived on the sender side
        ``auto_delete``: to mark the message as deleted on the sender side
        ``auto_moderators``: a list of auto-moderation functions
    """
    message = Message(subject=subject, body=body, sender=sender, recipient=recipient)
    initial_status = message.moderation_status
    if auto_moderators:
        message.auto_moderate(auto_moderators)
    else:
        message.moderation_status = STATUS_ACCEPTED
    message.clean_moderation(initial_status)
    if auto_archive:
        message.sender_archived = True
    if auto_delete:
        message.sender_deleted_at = now()
    message.save()
    if not skip_notification:
        message.notify_users(initial_status)
