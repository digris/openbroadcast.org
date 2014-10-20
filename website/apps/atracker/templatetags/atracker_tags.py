from django import template

from ..models import Event
from ..util import summary_for_object

register = template.Library()


@register.inclusion_tag('atracker/templatetags/events_for_object.html', takes_context=True)
def events_for_object(context, obj):

    events = Event.objects.by_obj(obj=obj)
    
    if events:
        return {
            'request': context['request'],
            'events': events
        }

    return {}


@register.inclusion_tag('atracker/templatetags/events_for_object_by_verb.html', takes_context=True)
def events_for_object_by_verb(context, obj, verb):

    events = Event.objects.by_obj(obj=obj).filter(event_type__title='%s' % verb)[0:2000]

    if events:
        return {
            'request': context['request'],
            'events': events
        }

    return {}


@register.inclusion_tag('atracker/templatetags/stats_for_object.html', takes_context=True)
def stats_for_object(context, obj):

    statistics = summary_for_object(obj)
    
    if statistics:
        return {
            'request': context['request'],
            'statistics': statistics
        }

    return {}


@register.inclusion_tag('atracker/templatetags/stats_for_user.html', takes_context=True)
def stats_for_user(context, user):

    events = Event.objects.filter(user=user)

    return {
        'request': context['request'],
        'events': events
    }

    return {}





@register.inclusion_tag('object_events/notifications.html', takes_context=True)
def render_notifications(context, notification_amount=8):
    """Template tag to render fresh notifications for the current user."""
    if context.get('request') and context['request'].user.is_authenticated():
        events = ObjectEvent.objects.filter(user=context['request'].user)
        if events:
            return {
                'authenticated': True,
                'request': context['request'],
                'unread_amount': events.filter(read_by_user=False).count(),
                'notifications': events[:notification_amount],
            }
        return {'authenticated': True}
    return {}