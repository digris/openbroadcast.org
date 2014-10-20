import logging

from atracker.models import Event
log = logging.getLogger(__name__)

def create_event(user, content_object, event_content_object=None, event_type=''):

    Event.create_event(user, content_object, event_content_object, event_type)
