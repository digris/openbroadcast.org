from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.cache import get_cache
from django.db.models import Avg
from arating.models import VOTE_CHOICES 

register = template.Library()


arating_cache = get_cache('default')

     
@register.inclusion_tag('arating/inline.html', takes_context=True)
def rating_for_object(context, object):
    
    request = context['request']
    
    try:
        user_vote = object.votes.filter(user=request.user)[0].vote
    except (TypeError, IndexError) as e:
        user_vote = None
    
    choices = []
    for choice in reversed(VOTE_CHOICES):
        count = object.votes.filter(vote=choice[0]).count()
        tc = {'key': choice[0], 'count': count, 'active': user_vote==choice[0] }
        choices.append(tc)

    data = {}
    data['choices'] = choices
    data['request'] = request
    data['object'] = object
    data['ct'] = '%s.%s' % (ContentType.objects.get_for_model(object).app_label, object.__class__.__name__.lower())
    
    
    return data



@register.inclusion_tag('arating/topflop.html', takes_context=True)
def topflop_for_object(context, object):

    try:
        data = arating_cache.get(object.get_absolute_url())
    except:
        data = None

    if not data:

        avg_vote = object.votes.aggregate(Avg('vote')).values()[0]
        upvotes = object.votes.filter(vote__gt=0).count()
        downvotes = object.votes.filter(vote__lt=0).count()

        choices = []
        for choice in reversed(VOTE_CHOICES):
            count = object.votes.filter(vote=choice[0]).count()
            tc = {'key': choice[0], 'count': count }
            choices.append(tc)

        data = {}
        data['upvotes'] = upvotes
        data['downvotes'] = downvotes
        data['avg_vote'] = avg_vote

        try:
            arating_cache.set(object.get_absolute_url(), data)
        except:
            pass



    return data
     
     
