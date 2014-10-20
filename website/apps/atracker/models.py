"""Models for the ``object_events`` app."""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import date
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class EventType(models.Model):
    """
    Masterdata table containing event types.

    :title: Unique title of this event type. This will be used to decide which
      notification message to display or which partial to render.

    """
    title = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_('Title'),
        help_text=_('Please use a slugified name, e.g. "student-news".'),
    )

    class Meta:
        app_label = 'atracker'
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class EventManager(models.Manager):

    def by_obj(self, obj):
        ctype = ContentType.objects.get_for_model(obj)
        return self.get_query_set().filter(object_id=obj.pk, content_type=ctype)


class Event(models.Model):
    """
    An event created by a user related to any object.

    :user: FK to the user who created this event. Leave this empty if this
      event was created by no user but automatically.
    :created: Creation date of this event.
    :event_type: Type of this event.
    :email_sent: True, if user has received this event via email.
    :read_by_user: True, if user has noticed this event.
    :content_object: Generic foreign key to the object this event is attached
      to. Leave this empty if it is a global event.
    :event_content_object: Generic foreign key to the object that has been
      created by this event. Leave this empty if the event did not create any
      object.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
        related_name='atracker_events',
        null=True, blank=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
    )

    event_type = models.ForeignKey(
        EventType,
        verbose_name=_('Type'),
        related_name='events',
    )
    
    archived = models.BooleanField(default=False)
    distributed = models.BooleanField(default=False)


    # Generic FK to the object this event is attached to
    content_type = models.ForeignKey(
        ContentType,
        related_name='event_content_objects',
        null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # Generic FK to the object that created this event
    event_content_type = models.ForeignKey(
        ContentType,
        related_name='event_objects',
        null=True, blank=True
    )
    event_object_id = models.PositiveIntegerField(null=True, blank=True)
    event_content_object = generic.GenericForeignKey(
        'event_content_type', 'event_object_id')
    
    objects = EventManager()

    class Meta:
        app_label = 'atracker'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('-created',)

    @staticmethod
    def create_event(user, content_object, event_content_object=None,
                     event_type=''):
        """
        Creates an event for the given user, object and type.

        If the type doesn't exist, yet, it will be created, so make sure that
        you don't have any typos in your type title.

        :param user: The user who created this event.
        :param content_object: The object this event is attached to.
        :param event_content_object: The object that created this event.
        :event_type: String representing the type of this event.

        """
        event_type_obj, created = EventType.objects.get_or_create(
            title=event_type)
        obj = Event(user=user, content_object=content_object,
                          event_type=event_type_obj)
        if event_content_object is not None:
            obj.event_content_object = event_content_object
        obj.save()
        return obj

    def __unicode__(self):
        return '{0}'.format(self.content_object)

    """
    somehow obsolete... use |timesince template-tag
    """
    def get_timesince(self):
        delta = (now() - self.created)
        if delta.days <= 1:
            return '{0} ago'.format(timesince(self.created, now()))
        if self.created.year != now().year:
            return date(self.created, 'd F Y')
        return date(self.created, 'd F')
    
    
    
def actstream_link(sender, instance, created, **kwargs):
    from actstream import action
    try:
        action.send(instance.user, verb=instance.event_type.title, target=instance.content_object)
    except Exception, e:
        print e

post_save.connect(actstream_link, sender=Event)