from django.db.models import get_model
from django import http

from ratings import handlers, signals

def vote(request, extra_context=None, form_class=None, using=None):
    """
    Vote view: this view is available only if request's method is POST.
    """
    if request.method == 'POST':
        
        # first superficial post data validation
        content_type = request.POST.get('content_type')
        object_pk = request.POST.get('object_pk')
        key = request.POST.get('key')
        if content_type is None or object_pk is None or key is None:
            # no content type, object id or key: no party
            return http.HttpResponseBadRequest('Missing required fields.')
        
        # getting current model and rating handler
        model = get_model(*content_type.split('.'))
        handler = handlers.ratings.get_handler(model)
        if handler is None:
            # bad or unregistered content type, bad request
            return http.HttpResponseBadRequest('Bad or unregistered content type.')
        
        # current target object getting voted
        try:
            target_object = model.objects.using(using).get(pk=object_pk)
        except model.DoesNotExist:
            return http.HttpResponseBadRequest('Invalid target object.')
        
        # validating the rating key
        if not handler.allow_key(request, target_object, key):
            return http.HttpResponseBadRequest('Invalid key.')
            
        # validating the user that wants to vote and the instance to be voted
        if not handler.allow_vote(request, target_object, key):
            return http.HttpResponseBadRequest('User cannot vote the instance.')
        
        # getting the form
        form_class = form_class or handler.get_vote_form_class(request)
        form = form_class(target_object, key, data=request.POST, 
            **handler.get_vote_form_kwargs(request, target_object, key))
        
        if form.is_valid():
            created = deleted = False
        
            # getting unsaved vote
            vote = form.get_vote(request, handler.allow_anonymous)
            
            # handling vote deletion
            if form.delete(request):
                deleted = True
                # pre-delete signal: receivers can stop the delete process
                # note: one receiver is always called: *handler.pre_delete*
                # handler can disallow the vote deletion
                responses = signals.vote_will_be_deleted.send(
                    sender=vote.__class__, 
                    vote=vote, request=request)

                # if one of the receivers reurns False then vote deletion 
                # must be killed
                for receiver, response in responses:
                    if response == False:
                        return http.HttpResponseBadRequest(
                            'Receiver %r killed the deletion process' % 
                            receiver.__name__)
                
                # actually delete the vote    
                handler.delete(request, vote)
                
                # post-delete signal
                # note: one receiver is always called: *handler.post_delete*
                signals.vote_was_deleted.send(sender=vote.__class__, 
                    vote=vote, request=request)
            
            else:
                                
                # pre-vote signal: receivers can stop the vote process
                # note: one receiver is always called: *handler.pre_vote*
                # handler can disallow the vote
                responses = signals.vote_will_be_saved.send(
                    sender=vote.__class__, 
                    vote=vote, request=request)
        
                # if one of the receivers reurns False then voting must be killed
                for receiver, response in responses:
                    if response == False:
                        return http.HttpResponseBadRequest(
                            'Receiver %r killed the voting process' % 
                            receiver.__name__)
        
                # actually save the vote
                created = handler.vote(request, vote)
        
                # post-vote signal
                # note: one receiver is always called: *handler.post_vote*
                signals.vote_was_saved.send(sender=vote.__class__, 
                    vote=vote, request=request, created=created)
        
            # vote is saved or deleted: redirect
            return handler.success_response(request, vote, created, deleted)
        
        # form is not valid: must handle errors
        return handler.failure_response(request, form.errors)
        
    # only answer POST requests
    return http.HttpResponseForbidden('Forbidden.')
