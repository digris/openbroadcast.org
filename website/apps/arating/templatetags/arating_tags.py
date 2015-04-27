# -*- coding: utf-8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from cacheops import cached_as
from django.db.models import Avg
from arating.models import Vote, VOTE_CHOICES

register = template.Library()




     
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

    @cached_as(Vote.objects.filter(object_id=object.pk), timeout=86400*7, extra=object.pk)
    def _calculate_top_flop():

        avg_vote = object.votes.aggregate(Avg('vote')).values()[0]
        upvotes = object.votes.filter(vote__gt=0).count()
        downvotes = object.votes.filter(vote__lt=0).count()

        choices = []
        for choice in reversed(VOTE_CHOICES):
            count = object.votes.filter(vote=choice[0]).count()
            tc = {'key': choice[0], 'count': count }
            choices.append(tc)

        return {
            'upvotes': upvotes,
            'downvotes': downvotes,
            'avg_vote': avg_vote,
        }

    return _calculate_top_flop()
     
     
