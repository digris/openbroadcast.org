import json

from django.template import loader, RequestContext
from django.http import (HttpResponse, HttpResponseRedirect, Http404,
                         HttpResponseForbidden)
from django.db.models.base import ModelBase
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.decorators import login_required

from arating.models import Vote
from arating.models import VOTE_CHOICES

@login_required
def vote(request, content_type, object_id, vote=0, can_vote_test=None,
              redirect_url=None, template_name=None, template_loader=loader,
              extra_context=None, context_processors=None, mimetype=None):
 

    if isinstance(content_type, ContentType):
        pass
    elif isinstance(content_type, ModelBase):
        content_type = ContentType.objects.get_for_model(content_type)
    elif isinstance(content_type, basestring) and '.' in content_type:
        app, modelname = content_type.split('.')
        content_type = ContentType.objects.get(app_label=app, model__iexact=modelname)
    elif isinstance(content_type, basestring):
        content_type = ContentType.objects.get(id=int(content_type))
    else:
        raise ValueError('content_type must be an instance of ContentType, a model, or "app.modelname" string')

    # do the action
    if vote:

        # 404 if object to be voted upon doesn't exist
        if content_type.model_class().objects.filter(pk=object_id).count() == 0:
            raise Http404

        # if there is a can_vote_test func specified, test then 403 if needed
        if can_vote_test:
            if not can_vote_test(request, content_type, object_id, vote):
                return HttpResponseForbidden("vote was forbidden")

        vobj,new = Vote.objects.get_or_create(content_type=content_type,
                                              object_id=object_id, user=request.user,
                                              defaults={'vote':vote})
        if not new:
            vobj.vote = vote
            vobj.save()
    else:
        Vote.objects.filter(content_type=content_type, 
                            object_id=object_id, user=request.user).delete() 

    # build the response
    if redirect_url:
        return HttpResponseRedirect(redirect_url)
    elif template_name:
        content_obj = content_type.get_object_for_this_type(pk=object_id)
        c = RequestContext(request, {'content_obj':content_obj}, 
                           context_processors)

        # copy extra_context into context, calling any callables
        for k,v in extra_context.items():
            if callable(v):
                c[k] = v()
            else:
                c[k] = v

        t = template_loader.get_template(template_name)
        body = t.render(c)
    else:
        
        object = content_type.model_class().objects.filter(pk=object_id)[0]
    
        try:
            user_vote = object.votes.filter(user=request.user)[0].vote
        except (TypeError, IndexError) as e:
            user_vote = None
        
        choices = []
        for choice in reversed(VOTE_CHOICES):
            print 'choice: %s user_vote: %s' % (choice[0], user_vote)
            count = object.votes.filter(vote=choice[0]).count()
            tc = {'key': choice[0], 'count': count, 'active': user_vote==choice[0] }
            choices.append(tc)
            
        
        data = {'choices': choices}

        
    return HttpResponse(json.dumps(data), mimetype="application/json")
    #return HttpResponse(data, mimetype=mimetype)

