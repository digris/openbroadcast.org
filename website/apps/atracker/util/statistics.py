import logging

from atracker.models import Event, EventType
log = logging.getLogger(__name__)

def summary_for_object(content_object, event_content_object=None, event_type=''):

    types = EventType.objects.all()
    statistics = []
    
    for type in types:
        events = Event.objects.by_obj(content_object).filter(event_type=type)
        statistics.append({'title': type.title,
                            'count': events.count()
                           })

    return statistics

