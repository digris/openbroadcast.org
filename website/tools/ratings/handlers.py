from django.db import IntegrityError
from django.db.models.base import ModelBase
from django.db.models.signals import pre_delete as pre_delete_signal

from ratings import settings, models, forms, exceptions, signals, cookies

class RatingHandler(object):
    """
    Encapsulates content rating options for a given model.
    
    This class can be subclassed to specify different behaviour and options
    for ratings of a given model, but can also be used directly, just to
    handle default rating for any model. 
    
    The default rating provides only one 1-5 ranged (without decimal places) 
    score for each content object, and allows voting only for authenticated
    users.
    
    The default rating handler uses the project's settings as options: this 
    way you can register not customized rating handlers and then modify
    their options just editing the settings file.
    
    Most common rating needs can be handled by subclassing *RatingHandler* 
    and changing the values of pre-defined attributes. 
    The full range of built-in options is as follows.
    
    
    .. py:attribute:: allow_anonymous 
    
        set to False to allow votes only by authenticated users 
        (default: *False*)
    
    .. py:attribute:: score_range 
        
        a sequence *(min_score, max_score) representing the allowed score range 
        (including extremes) 
        note that the score *0* is reserved for vote deletion
        (default: *(1, 5)*)
    
    .. py:attribute:: score_step
        
        the step allowed in scores (default: *1*)
    
    .. py:attribute:: weight 
        
        this is used while calculating the average score and represents 
        the difficulty for a target object to obtain a higher rating
        (default: *0*)
    
    .. py:attribute:: default_key
        
        default key to use for votes when there is only one vote-per-content 
        (default: *'main'*)
    
    .. py:attribute:: can_delete_vote
    
        set to False if you do not want to allow users to delete a 
        previously saved vote (default: *True*)
    
    .. py:attribute:: can_change_vote 
    
        set to False if you do not want to allow users to change the score of 
        a previously saved vote (default: *True*)
    
    .. py:attribute:: next_querystring_key
    
        querystring key that can contain the url of the redirection performed 
        after voting (default: *'next'*)
    
    .. py:attribute:: votes_per_ip_address 
    
        the number of allowed votes per ip address, only used if anonymous users 
        can vote (default: *0*, means no limit)
    
    .. py:attribute:: form_class
    
        form class that will be used to handle voting 
        (default: *ratings.forms.VoteForm*) 
        this app, out of the box, provides also *SliderVoteForm* and a *StarVoteForm*
        
    .. py:attribute:: cookie_max_age
    
        if anonymous rating is allowed, you can define here the cookie max age
        as a number of seconds (default: one year)
        
    .. py:attribute:: success_messages
    
        this should be a sequence of (vote created, vote changed, vote deleted)
        messages sent (using *django.contrib.messages*) to the 
        user after a successful vote creation, change, deletion 
        (scored without using AJAX)
        if this is None, then no message is sent (default: *None*)
    
        
    For situations where the built-in options listed above are not sufficient, 
    subclasses of *RatingHandler* can also override the methods which 
    actually perform the voting process, and apply any logic they desire.
    
    See the method's docstrings for a description of how each method is
    used during the voting process.
    """
    allow_anonymous = settings.ALLOW_ANONYMOUS
    score_range = settings.SCORE_RANGE
    score_step = settings.SCORE_STEP
    weight = settings.WEIGHT
    default_key = settings.DEFAULT_KEY
    next_querystring_key = settings.NEXT_QUERYSTRING_KEY
    votes_per_ip_address = settings.VOTES_PER_IP_ADDRESS
    cookie_max_age = settings.COOKIE_MAX_AGE
    
    success_messages = None
    can_delete_vote = True
    can_change_vote = True
    form_class = forms.VoteForm
    
    def __init__(self, model):
        self.model = model
            
    def get_key(self, request, instance):
        """
        Return the ratings key to be used to save the vote if the key
        is not provided by the user (for example with the optional
        argument *using* in templatetags).
        
        Subclasses can return different keys based on the *request* and
        the given target object *instance*.
        
        For example, if you want a different key to be used if the user is
        staff, you can override this method in this way::
        
            def get_key(self, request, instance):
                return 'staff' if request.user.is_superuser else 'normal'

        This method is called only if the user does not provide a rating key.
        """
        return self.default_key
        
    def allow_key(self, request, instance, key):
        """
        This method is called when the user tries to vote using the given
        rating *key* (e.g. when the voting view is called with POST data).
        
        The voting process continues only if this method returns True
        (i.e. a valid key is passed).
        
        For example, if you want to different rating for each target object,
        you can use two forms (each providing a different key, say 'main' and
        'other') and then allow those keys::
        
            def allow_key(self, request, instance, key):
                return key in ('main', 'other')        
        """
        return key == self.get_key(request, instance)
        
    def allow_vote(self, request, instance, key):
        """
        This method can block the voting process if the current user 
        actually is not allowed to vote for the given *instance*

        By default the only check made here is for anonymous users, but this
        method can be subclassed to implement more advanced validations
        by *key* or target object *instance*.
        
        If you want users to vote only active objects, for instance, you can
        write inyour subclas::
        
            def allow_vote(self, request, instance, key):
                allowed = super(MyClass, self).allow_vote(request, instance, key)
                return allowed and instance.is_active
        
        If anonymous votes are allowed, this method checks for ip adresses too.
        """
        if self.allow_anonymous:
            ip_address = request.META.get("REMOTE_ADDR")
            if ip_address is None:
                # anonymous user must at least own an ip adreess
                return False
            if self.votes_per_ip_address:
                # in case of vote-per-ip cap, check if this ip
                # can continue voting this object
                count = models.Vote.objects.filter_for(instance,
                    user__isnull=True, ip_address=ip_address).count()
                return count < self.votes_per_ip_address
            return True
        else:
            # for normal user voting the user must be authenticated
            return request.user.is_authenticated()
        
    # vote form
        
    def get_vote_form_class(self, request):
        """
        Return the vote form class that will be used to handle voting.
        This method can be overridden by view-level passed form class.
        """
        return self.form_class
        
    def get_vote_form_kwargs(self, request, instance, key):
        """
        Return the optional kwargs used to instantiate the voting form.
        """
        # score range and decimals (used during form validation)
        kwargs = {
            'score_range': self.score_range, 
            'score_step': self.score_step,
            'can_delete_vote': self.can_delete_vote,
        }
        # initial vote (if present)
        if self.allow_anonymous:
            vote = self.get_vote(instance, key, request.COOKIES)
        elif request.user.is_authenticated():
            vote = self.get_vote(instance, key, request.user)
        else:
            vote = None
        if vote is not None:
            kwargs['initial'] = {'score': vote.score}
        return kwargs
        
    # voting
        
    def pre_vote(self, request, vote):
        """
        Called just before the vote is saved to the db, this method takes
        the *request* and the unsaved *vote* instance.
        
        The unsaved vote can be a brand new vote instance (without *id*)
        or an existing vote object the user want to change.
        
        Subclasses can use this method to check if the vote can be saved and,
        if necessary, block the voting process returning False.
        
        This method is called by a *signals.vote_will_be_saved* listener
        always attached to the handler.
        It's up to the developer if override this method or just connect
        another listener to the signal: the voting process is killed if 
        just one receiver returns False.
        """
        return self.can_change_vote if vote.id else True
        
    def vote(self, request, vote):
        """
        Save the vote to the database.
        Must return True if the *vote* was created, False otherwise.
        
        By default this method just does *vote.save()* and recalculates
        the related score (average, total, number of votes).
        """
        created = not vote.id
        try:
            vote.save()
        except IntegrityError: # assume another thread created the vote
            created = False
        else:
            models.upsert_score(vote.content_object, vote.key, weight=self.weight)
        return created
        
    def post_vote(self, request, vote, created):
        """
        Called just after the vote is saved to the db.
        
        This method is called by a *signals.vote_was_saved* listener
        always attached to the handler.
        """
        pass
        
    # deleting vote
    
    def pre_delete(self, request, vote):
        """
        Called just before the vote is deleted from the db, this method takes
        the *request* and the *vote* instance.
        
        Subclasses can use this method to check if the vote can be deleted and,
        if necessary, block the vote deletion process returning False.
        
        This method is called by a *signals.vote_will_be_deleted* listener
        always attached to the handler.
        It's up to the developer if override this method or just connect
        another listener to the signal: the voting deletion process is killed 
        if just one receiver returns False.
        """
        return self.can_delete_vote and vote.id
        
    def delete(self, request, vote):
        """
        Delete the vote from the database.
        
        By default this method just do *vote.delete()* and recalculates
        the related score (average, total, number of votes).
        """
        # thread safe delete
        try:
            vote.delete()
        except AssertionError: # maybe the object was already deleted
            pass
        else:
            models.upsert_score(vote.content_object, vote.key, weight=self.weight)
        
    def post_delete(self, request, vote):
        """
        Called just after the vote is deleted to from db.
        
        This method is called by a *signals.vote_was_deleted* listener
        always attached to the handler.
        """
        pass
        
    # view callbacks
    
    def ajax_response(self, request, vote, created, deleted):
        """
        Called by *success_response* when the request is ajax.
        Return a json reponse containing::
        
            {
                'key': 'the_rating_key',
                'vote_id': vote.id,
                'vote_score': vote.score,
                'score_average': score.average,
                'score_num_votes': score.num_votes,
                'score_total': score.total,
            }
        """
        from django.http import HttpResponse
        from django.utils import simplejson as json
        score = vote.get_score()
        data = {
            'key': score.key,
            'vote_id': vote.id,
            'vote_score': vote.score,
            'score_average': score.average,
            'score_num_votes': score.num_votes,
            'score_total': score.total,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
        
    def normal_response(self, request, vote, created, deleted):
        """
        Called by *success_response* when the request is not ajax.
        Return a redirect response.
        """
        from django.shortcuts import redirect
        next = request.REQUEST.get('next') or request.META.get('HTTP_REFERER') or '/'
        return redirect(next)
        
    def set_cookies(self, request, response, vote, created, deleted):
        """
        Called by *success_response* when the vote is by an nonymous user.
        Set the cookie to the response.
        """
        cookie_name = str(cookies.get_name(vote.content_object, vote.key))
        if deleted:
            response.delete_cookie(cookie_name)
        else:
            response.set_cookie(cookie_name, vote.cookie, self.cookie_max_age)
        
    def set_message(self, request, response, vote, created, deleted):
        """
        Called by *success_response* if the handler is customized with
        a success message.
        """
        from django.contrib import messages
        created_msg, changed_msg, deleted_msg = self.success_messages
        if deleted and deleted_msg:
            messages.success(request, deleted_msg)
        elif created and created_msg:
            messages.success(request, created_msg)
        elif not created and changed_msg:
            messages.success(request, changed_msg)
    
    def success_response(self, request, vote, created, deleted):
        """
        Callback used by the voting views, called when the user successfully
        voted. Must return a Django http response (usually a redirect, or
        some json if the request is ajax).
        """
        if request.is_ajax():
            response = self.ajax_response(request, vote, created, deleted)
        else:
            response = self.normal_response(request, vote, created, deleted)    
        # handling anonymous votes
        if self.allow_anonymous:
            self.set_cookies(request, response, vote, created, deleted)
        # handling success message
        if self.success_messages:
            self.set_message(request, response, vote, created, deleted)
        return response
        
    def failure_response(self, request, errors):
        """
        Callback used by the voting views, called when vote form did not 
        validate. Must return a Django http response.
        """
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest('Invalid data in vote form.')
    
    # utils
    
    def _get_user_lookups(self, instance, key, user_or_cookies):
        """
        Return the correct db model lookup for given *user_or_cookies*.
        
        Return an empty dict if the lookup is for cookies and the user
        does not own a cookie corresponding to given *instance* and *key*.
        
        A *ValueError* is raised if you cookies are given but anonymous votes 
        are not allowed by the handler.
        """
        # here comes your duck
        if hasattr(user_or_cookies, 'pk'):
            return {'user': user_or_cookies}
        elif self.allow_anonymous:
            cookie_name = cookies.get_name(instance, key)
            if cookie_name in user_or_cookies:
                return {'cookie': user_or_cookies[cookie_name]}
            return {}
        raise ValueError('Anonymous vote not allowed')
    
    def has_voted(self, instance, key, user_or_cookies):
        """
        Return True if the user related to given *user_or_cookies* has 
        voted the given target object *instance* using the given *key*.
        
        The argument *user_or_cookies* can be a Django User instance
        or a cookie dict (for anonymous votes).
        
        A *ValueError* is raised if you give cookies but anonymous votes 
        are not allowed by the handler.
        """
        user_lookup = self._get_user_lookups(instance, key, user_or_cookies)
        if not user_lookup:
            return False
        return models.Vote.objects.filter_for(instance, key=key, 
            **user_lookup).exists()
        
    def get_vote(self, instance, key, user_or_cookies):
        """
        Return the vote instance created by the user related to given 
        *user_or_cookies* for the target object *instance* using 
        the given *key*.
        
        The argument *user_or_cookies* can be a Django User instance
        or a cookie dict (for anonymous votes).
        
        Return None if the vote does not exists.
        
        A *ValueError* is raised if you give cookies but anonymous votes 
        are not allowed by the handler.
        """
        user_lookup = self._get_user_lookups(instance, key, user_or_cookies)
        if not user_lookup:
            return None
        return models.Vote.objects.get_for(instance, key, **user_lookup)
        
    def get_votes_for(self, instance, **kwargs):
        """
        Return all votes given to *instance* and filtered by any given *kwargs*.
        All the content objects related to returned votes are evaluated
        together with votes.
        """
        return models.Vote.objects.filter_with_contents(
            content_object=instance, **kwargs)
            
    def get_votes_by(self, user, **kwargs):
        """
        Return all votes assigned by *user* to model instances handled
        by this handler, and filtered by any given *kwargs*.
        All the content objects related to returned votes are evaluated
        together with votes.
        """
        return models.Vote.objects.filter_with_contents(user=user, 
            content_object=self.model, **kwargs)

    def get_score(self, instance, key):
        """
        Return the score for the target object *instance* and the given *key*.
        Return None if the target object does not have a score.
        """
        return models.Score.objects.get_for(instance, key)
    
    def annotate_scores(self, queryset, key, **kwargs):
        """
        Annotate the *queryset* with scores using the given *key* and *kwargs*.
        
        In *kwargs* it is possible to specify the values to retreive mapped 
        to field names (it is up to you to avoid name clashes).
        You can annotate the queryset with the number of votes (*num_votes*), 
        the average score (*average*) and the total sum of all votes (*total*).

        For example, the following call::

            annotate_scores(Article.objects.all(), 'main',
                average='average', num_votes='num_votes')

        Will return a queryset of article and each article will have two new
        attached fields *average* and *num_votes*.

        Of course it is possible to sort the queryset by a score value, e.g.::

            for article in annotate_scores(Article, 'by_staff', 
                staff_avg='average', staff_num_votes='num_votes'
                ).order_by('-staff_avg', '-staff_num_votes'):
                print 'staff num votes:', article.staff_num_votes
                print 'staff average:', article.staff_avg
        
        This is basically a wrapper around *ratings.model.annotate_scores*.
        """
        return models.annotate_scores(queryset, key, **kwargs)
        
    def annotate_votes(self, queryset, key, user, score='score'):
        """
        Annotate the *queryset* with votes given by the passed *user* using the 
        given *key*.
        
        The score itself will be present in the attribute named *score* of 
        each instance of the returned queryset.

        Usage example::

            for article in annotate_votes(Article.objects.all(), 'main', myuser, 
                score='myscore'):
                print 'your vote:', article.myscore
        
        This is basically a wrapper around *ratings.model.annotate_votes*.
        For anonymous voters this functionality is unavailable.
        """
        return models.annotate_votes(queryset, key, user, score)
        
    def deleting_target_object(self, sender, instance, **kwargs):
        """
        The target object *instance* of the model *sender*, is being deleted,
        so we must delete all the votes and scores related to that instance.
        
        This receiver is usually connected by the ratings registry, when 
        a handler is registered.
        """
        models.delete_scores_for(instance)
        models.delete_votes_for(instance)
            
     
class Ratings(object):
    """
    Registry that stores the handlers for each content type rating system.

    An instance of this class will maintain a list of one or more models 
    registered for being rated, and their associated handler classes.

    To register a model, obtain an instance of *Ratings* (this module exports 
    one as *ratings*), and call its *register* method, passing the model class 
    and a handler class (which should be a subclass of *RatingHandler*). 
    Note that both of these should be the actual classes, not instances 
    of the classes.

    To cease ratings handling for a model, call the *unregister* method,
    passing the model class.

    For convenience, both *register* and *unregister* can also accept a list 
    of model classes in place of a single model; this allows easier 
    registration of multiple models with the same *RatingHandler* class.
    """
    def __init__(self):
        self._registry = {}
        self.connect()

    def connect(self):
        """
        Pre and post (delete) vote signals.
        """
        signals.vote_will_be_saved.connect(self.pre_vote, sender=models.Vote)
        signals.vote_was_saved.connect(self.post_vote, sender=models.Vote)
        signals.vote_will_be_deleted.connect(self.pre_delete, sender=models.Vote)
        signals.vote_was_deleted.connect(self.post_delete, sender=models.Vote)
        
    def connect_model_signals(self, model, handler):
        """
        Connect the *pre_delete* signal sent by given *model* to
        the *handler* receiver.
        """
        pre_delete_signal.connect(handler.deleting_target_object, sender=model)
    
    def get_handler_instance(self, model, handler_class, options):
        """
        Return an handler instance for the given *model*.
        """
        handler = handler_class(model)
        for k, v in options.items():
            setattr(handler, k, v)
        return handler

    def register(self, model_or_iterable, handler_class=None, **kwargs):
        """
        Register a model or a list of models for ratings handling, using a 
        particular *handler_class*, e.g.::
        
            from ratings.handlers import ratings, RatingHandler
            # register one model for rating
            ratings.register(Article, RatingHandler)
            # register other two models
            ratings.register([Film, Series], RatingHandler)
        
        If the handler class is not given, the default 
        *ratings.handlers.RatingHandler* class will be used.
        
        If *kwargs* are present, they are used to override the handler
        class attributes (using instance attributes), e.g.::
            
            ratings.register(Article, RatingHandler, 
                score_range=(1, 10), score_step=0.5)

        Raise *AlreadyHandled* if any of the models are already registered.
        """
        if handler_class is None:
            handler_class = RatingHandler
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise exceptions.AlreadyHandled(
                    "The model '%s' is already being handled" % 
                    model._meta.module_name)
            handler = self.get_handler_instance(model, handler_class, kwargs)
            self._registry[model] = handler
            self.connect_model_signals(model, handler)
        
    def unregister(self, model_or_iterable):
        """
        Remove a model or a list of models from the list of models that will
        be handled.

        Raise *NotHandled* if any of the models are not currently registered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise exceptions.NotHandled(
                    "The model '%s' is not currently being handled" % 
                    model._meta.module_name)
            del self._registry[model]
            
    def get_handler(self, model_or_instance):
        """
        Return the handler for given model or model instance.
        Return None if model is not registered.
        """
        if isinstance(model_or_instance, ModelBase):
            model = model_or_instance
        else:
            model = type(model_or_instance)
        return self._registry.get(model)

    def pre_vote(self, sender, vote, request, **kwargs):
        """
        Apply any necessary pre-save ratings steps to new votes.
        """
        model = vote.content_type.model_class()
        if model not in self._registry:
            return False
        return self._registry[model].pre_vote(request, vote)

    def post_vote(self, sender, vote, request, created, **kwargs):
        """
        Apply any necessary post-save ratings steps to new votes.
        """
        model = vote.content_type.model_class()
        if model in self._registry:
            return self._registry[model].post_vote(request, vote, created)
        
    def pre_delete(self, sender, vote, request, **kwargs):
        """
        Apply any necessary pre-delete ratings steps.
        """
        model = vote.content_type.model_class()
        if model not in self._registry:
            return False
        return self._registry[model].pre_delete(request, vote)

    def post_delete(self, sender, vote, request, **kwargs):
        """
        Apply any necessary post-delete ratings steps.
        """
        model = vote.content_type.model_class()
        if model in self._registry:
            return self._registry[model].post_delete(request, vote)
            
    def get_votes_by(self, user, **kwargs):
        """
        Return all votes assigned by *user* and filtered by any given *kwargs*.
        All the content objects related to returned votes are evaluated
        together with votes.
        """
        return models.Vote.objects.filter_with_contents(user=user, **kwargs)
        
# import this instance in your code to use in registering models for ratings
ratings = Ratings()
