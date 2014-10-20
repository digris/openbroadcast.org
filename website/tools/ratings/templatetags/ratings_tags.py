import re

from django import template

from ratings import handlers

register = template.Library()

def _parse(token):
    """
    Argument validation for common templatetags.
    The following args are accepted::
    
        for object as varname -> ('object', None, 'varname')
        for object using key as varname -> ('object', 'key', 'varname')
        
    Return a sequence *(target_object, key, varname)*.
    The argument key can be None.
    """
    tokens = token.contents.split()
    if tokens[1] != 'for':
        msg = "Second argument in %r tag must be 'for'" % tokens[0]
        raise template.TemplateSyntaxError(msg)
    token_count = len(tokens)
    if token_count == 5:
        if tokens[3] != 'as':
            msg = "Fourth argument in %r tag must be 'as'" % tokens[0]
            raise template.TemplateSyntaxError(msg)
        return tokens[2], None, tokens[4]
    elif token_count == 7:
        if tokens[3] != 'using':
            msg = "Fourth argument in %r tag must be 'using'" % tokens[0]
            raise template.TemplateSyntaxError(msg)
        if tokens[5] != 'as':
            msg = "Sixth argument in %r tag must be 'as'" % tokens[0]
            raise template.TemplateSyntaxError(msg)
        return tokens[2::2]
    msg = '%r tag requires 4 or 6 arguments' % tokens[0]
    raise template.TemplateSyntaxError(msg)


# FORM

@register.tag
def get_rating_form(parser, token):
    """
    Return (as a template variable in the context) a form object that can be 
    used in the template to add, change or delete a vote for the 
    specified target object.
    Usage:
    
    .. code-block:: html+django
    
        {% get_rating_form for *target object* [using *key*] as *var name* %}
        
    Example:
    
        .. code-block:: html+django
    
        {% get_rating_form for object as rating_form %} # key here is 'main'
        {% get_rating_form for target_object using 'mykey' as rating_form %}
        
    The key can also be passed as a template variable (without quotes).
        
    If you do not specify the key, then the key is taken using the registered
    handler for the model of given *object*.
        
    Having the form object, it is quite easy to display the form, e.g.:
    
    .. code-block:: html+django
        
        <form action="{% url ratings_vote %}" method="post">
            {% csrf_token %}
            {{ rating_form }}
            <p><input type="submit" value="Vote &rarr;"></p>
        </form>
        
    If the target object's model is not handled, then the template variable 
    will not be present in the context.
    """
    return RatingFormNode(*_parse(token))

class RatingFormNode(template.Node):
    def __init__(self, target_object, key, varname):
        self.target_object = template.Variable(target_object)
        # key
        self.key_variable = None
        if key is None:
            self.key = None
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # varname
        self.varname = varname
        
    def render(self, context):
        target_object = self.target_object.resolve(context)
        # validating given args
        handler = handlers.ratings.get_handler(type(target_object))
        request = context.get('request')
        if handler and request:
            # getting the rating key
            if self.key_variable:
                key = self.key_variable.resolve(context)
            elif self.key is None:
                key = handler.get_key(request, target_object)
            else:
                key = self.key            
            # getting the form
            form_class = handler.get_vote_form_class(request)
            form = form_class(target_object, key, 
                **handler.get_vote_form_kwargs(request, target_object, key))
            context[self.varname] = form
        return u''


# SCORES

@register.tag
def get_rating_score(parser, token):
    """
    Return (as a template variable in the context) a score object 
    representing the score given to the specified target object.
    Usage:
    
    .. code-block:: html+django
    
        {% get_rating_score for *target object* [using *key*] as *var name* %}
        
    Example:
    
    .. code-block:: html+django
    
        {% get_rating_score for object as score %}
        {% get_rating_score for target_object using 'mykey' as score %}
        
    The key can also be passed as a template variable (without quotes).
    
    If you do not specify the key, then the key is taken using the registered
    handler for the model of given *object*.
    
    Having the score model instance you can display score info, as follows:
    
    .. code-block:: html+django
    
        Average score: {{ score.average }}
        Number of votes: {{ score.num_votes }}
    
    If the target object's model is not handled, then the template variable 
    will not be present in the context.
    """
    return RatingScoreNode(*_parse(token))
    
class RatingScoreNode(template.Node):
    def __init__(self, target_object, key, varname):
        self.target_object = template.Variable(target_object)
        # key
        self.key_variable = None
        if key is None:
            self.key = None
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # varname
        self.varname = varname
        
    def render(self, context):
        target_object = self.target_object.resolve(context)
        # validating given args
        handler = handlers.ratings.get_handler(type(target_object))
        request = context.get('request')
        if handler and request:
            # getting the rating key
            if self.key_variable:
                key = self.key_variable.resolve(context)
            elif self.key is None:
                key = handler.get_key(request, target_object)
            else:
                key = self.key            
            # getting the score
            context[self.varname] = handler.get_score(target_object, key)
        return u''
        
        
SCORES_ANNOTATE_PATTERN = r"""
    ^ # begin of line
    (?P<queryset>\w+) # queryset
    \s+with\s+(?P<fields>[\w=,.'"]+) # fields mapping
    \s+using\s+(?P<key>[\w'"]+) # key
    (\s+ordering\s+by\s+(?P<order_by>[\w\-'",]+))? # order
    (\s+as\s+(?P<varname>\w+))? # varname
    $ # end of line
"""
SCORES_ANNOTATE_EXPRESSION = re.compile(SCORES_ANNOTATE_PATTERN, re.VERBOSE)
 
@register.tag
def scores_annotate(parser, token):
    """
    Use this templatetag when you need to update a queryset in bulk 
    adding score values, e.g:
    
    .. code-block:: html+django
    
        {% scores_annotate queryset with myaverage='average' using 'main' %}
        
    After this call each queryset instance has a *myaverage* attribute
    containing his average score for the key 'main'.
    The score field name and the key can also be passed as 
    template variables, without quotes, e.g.:
    
    .. code-block:: html+django
    
        {% scores_annotate queryset with myaverage=average_var using key_var %}
    
    You can also specify a new context variable for the modified queryset, e.g.:
    
    .. code-block:: html+django
    
        {% scores_annotate queryset with myaverage='average' using 'main' as new_queryset %}
        {% for instance in new_queryset %}
            Average score: {{ instance.myaverage }}
        {% endfor %}
                
    You can annotate a queryset with different score values at the same time, 
    remembering that accepted values are 'average', 'total' and 'num_votes':
    
    .. code-block:: html+django
    
        {% scores_annotate queryset with myaverage='average',num_votes='num_votes' using 'main' %}
        
    Finally, you can also sort the queryset, e.g.:
    
    .. code-block:: html+django
    
        {% scores_annotate queryset with myaverage='average' using 'main' ordering by '-myaverage' %}
        
    The order of arguments is important: the following example shows how
    to use this tempaltetag with all arguments:
    
    .. code-block:: html+django
    
        {% scores_annotate queryset with myaverage='average',num_votes='num_votes' using 'main' ordering by '-myaverage' as new_queryset %}
        
    The following example shows how to display in the template the ten most 
    rated films (and how is possible to order the queryset using multiple fields):
    
    .. code-block:: html+django
        
        {% scores_annotate films with avg='average',num='num_votes' using 'user_votes' ordering by '-avg,-num' as top_rated_films %}
        {% for film in top_rated_films|slice:":10" %}
            Film: {{ film }} 
            Average score: {{ film.avg }} 
            ({{ film.num }} vote{{ film.num|pluralize }})
        {% endfor %}
        
    If the queryset's model is not handled, then this templatetag 
    returns the original queryset.
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        error = u"%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, error
    # args validation
    match = SCORES_ANNOTATE_EXPRESSION.match(arg)
    if not match:
        error = u"%r tag has invalid arguments" % tag_name
        raise template.TemplateSyntaxError, error
    kwargs = match.groupdict()
    # fields validation
    fields = kwargs.pop('fields')
    try:
        fields_map = dict(i.split("=") for i in fields.split(","))
    except (TypeError, ValueError):
        error = u"%r tag has invalid field arguments" % tag_name
        raise template.TemplateSyntaxError, error
    # to the node
    return ScoresAnnotateNode(fields_map, **kwargs)

class ScoresAnnotateNode(template.Node):
    def __init__(self, fields_map, queryset, key, order_by, varname):
        # fields
        self.fields_map = {}
        for k, v in fields_map.items():
            data = {'value': None, 'variable': None}
            if v[0] in ('"', "'") and v[-1] == v[0]:
                data['value'] = v[1:-1]
            else:
                data['variable'] = template.Variable(v)
            self.fields_map[k] = data
        # queryset
        self.queryset = template.Variable(queryset)
        # key
        self.key_variable = None
        if key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # ordering
        self.order_by_variable = None
        if order_by is None:
            self.order_by = None
        elif order_by[0] in ('"', "'") and order_by[-1] == order_by[0]:
            self.order_by = order_by[1:-1]
        else:
            self.order_by = template.Variable(order_by)
        # varname
        self.varname = varname or queryset
        
    def render(self, context):
        # fields
        fields_map = {}
        for k, v in self.fields_map.items():
            if v['variable'] is None:
                fields_map[k] = v['value']
            else:
                fields_map[k] = v['variable'].resolve(context)
        # queryset
        queryset = self.queryset.resolve(context)
        # handler
        handler = handlers.ratings.get_handler(queryset.model)
        # if model is not handled the original queryset is returned
        if handler is not None:
            # key
            if self.key_variable is None:
                key = self.key
            else:
                key = self.key_variable.resolve(context)
            # annotation
            queryset = handler.annotate_scores(queryset, key, **fields_map)
            # ordering
            if self.order_by_variable:
                queryset = queryset.order_by(
                    *self.order_by_variable.resolve(context).split(','))
            elif self.order_by is not None:
                queryset = queryset.order_by(*self.order_by.split(','))
        # returning queryset
        context[self.varname] = queryset
        return u''
        
        
# VOTES

GET_RATING_VOTE_PATTERN = r"""
    ^ # begin of line
    for\s+(?P<target_object>[\w.]+) # target object
    (\s+by\s+(?P<user>[\w.]+))? # user
    (\s+using\s+(?P<key>[\w'"]+))? # key
    \s+as\s+(?P<varname>\w+) # varname
    $ # end of line
"""
GET_RATING_VOTE_EXPRESSION = re.compile(GET_RATING_VOTE_PATTERN, re.VERBOSE)
        
@register.tag
def get_rating_vote(parser, token):
    """
    Return (as a template variable in the context) a vote object 
    representing the vote given to the specified target object by
    the specified user.
    Usage:
    
    .. code-block:: html+django
    
        {% get_rating_vote for *target object* [by *user*] [using *key*] as *var name* %}
        
    Example:
    
    .. code-block:: html+django
    
        {% get_rating_vote for object as vote %}
        {% get_rating_vote for target_object using 'mykey' as vote %}
        {% get_rating_vote for target_object by myuser using 'mykey' as vote %}
        
    The key can also be passed as a template variable (without quotes).
    
    If you do not specify the key, then the key is taken using the registered
    handler for the model of given *object*.
    
    If you do not specify the user, then the vote given by the user of 
    current request will be returned. In this case, if user is anonymous
    and the rating handler allows anonymous votes, current cookies
    are used.
    
    Having the vote model instance you can display vote info, as follows:
    
    .. code-block:: html+django
    
        Vote: {{ vote.score }}
        Ip Address: {{ vote.ip_address }}
    
    If the target object's model is not handled, or the given user did not
    vote for that object, then the template variable will not be present 
    in the context.
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        error = u"%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, error
    # args validation
    match = GET_RATING_VOTE_EXPRESSION.match(arg)
    if not match:
        error = u"%r tag has invalid arguments" % tag_name
        raise template.TemplateSyntaxError, error
    return RatingVoteNode(**match.groupdict())
    
class RatingVoteNode(template.Node):
    def __init__(self, target_object, user, key, varname):
        self.target_object = template.Variable(target_object)
        self.user_variable = template.Variable(user) if user else None
        # key
        self.key_variable = None
        if key is None:
            self.key = None
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # varname
        self.varname = varname
        
    def render(self, context):
        target_object = self.target_object.resolve(context)
        # validating given args
        handler = handlers.ratings.get_handler(type(target_object))
        request = context.get('request')
        if handler and request:
            # getting user
            if self.user_variable is None:
                if request.user.is_authenticated():
                    user = request.user
                elif handler.allow_anonymous:
                    user = request.COOKIES
                else:
                    return u''
            else:
                user = self.user_variable.resolve(context)
            # getting the rating key
            if self.key_variable:
                key = self.key_variable.resolve(context)
            elif self.key is None:
                key = handler.get_key(request, target_object)
            else:
                key = self.key            
            # getting the score
            context[self.varname] = handler.get_vote(target_object, key, user)
        return u''


GET_LATEST_VOTES_FOR_PATTERN = r"""
    ^ # begin of line
    (?P<target_object>[\w.]+) # target object
    (\s+using\s+(?P<key>[\w'"]+))? # key
    \s+as\s+(?P<varname>\w+) # varname
    $ # end of line
"""
GET_LATEST_VOTES_FOR_EXPRESSION = re.compile(GET_LATEST_VOTES_FOR_PATTERN, 
    re.VERBOSE)
        
@register.tag
def get_latest_votes_for(parser, token):
    """
    Return (as a template variable in the context) the latest vote objects
    given to a target object.
    
    Usage:
    
    .. code-block:: html+django
    
        {% get_latest_votes_for *target object* [using *key*] as *var name* %}
        
    Usage example:
    
    .. code-block:: html+django
    
        {% get_latest_votes_for object as latest_votes %}
        {% get_latest_votes_for content.instance using 'main' as latest_votes %}
        
    In the following example we display latest 10 votes given to an *object*
    using the 'by_staff' key:
    
    .. code-block:: html+django
    
        {% get_latest_votes_for object uning 'mystaff' as latest_votes %}
        {% for vote in latest_votes|slice:":10" %}
            Vote by {{ vote.user }}: {{ vote.score }}
        {% endfor %}
        
    The key can also be passed as a template variable (without quotes).
        
    If you do not specify the key, then all the votes are taken regardless 
    what key they have.
    """
    return _get_latest_vote(parser, token, GET_LATEST_VOTES_FOR_EXPRESSION)

    
GET_LATEST_VOTES_BY_PATTERN = r"""
    ^ # begin of line
    (?P<user>[\w.]+) # user
    (\s+using\s+(?P<key>[\w'"]+))? # key
    \s+as\s+(?P<varname>\w+) # varname
    $ # end of line
"""
GET_LATEST_VOTES_BY_EXPRESSION = re.compile(GET_LATEST_VOTES_BY_PATTERN, 
    re.VERBOSE)
        
@register.tag
def get_latest_votes_by(parser, token):
    """
    Return (as a template variable in the context) the latest vote objects
    given by a user.
    
    Usage:
    
    .. code-block:: html+django
    
        {% get_latest_votes_by *user* [using *key*] as *var name* %}
        
    Usage example:
    
    .. code-block:: html+django
    
        {% get_latest_votes_by user as latest_votes %}
        {% get_latest_votes_for object.created_by using 'main' as latest_votes %}
        
    In the following example we display latest 10 votes given by *user*
    using the 'by_staff' key:
    
    .. code-block:: html+django
    
        {% get_latest_votes_by user using 'mystaff' as latest_votes %}
        {% for vote in latest_votes|slice:":10" %}
            Vote for {{ vote.content_object }}: {{ vote.score }}
        {% endfor %}
        
    The key can also be passed as a template variable (without quotes).
        
    If you do not specify the key, then all the votes are taken regardless 
    what key they have.
    """
    return _get_latest_vote(parser, token, GET_LATEST_VOTES_BY_EXPRESSION)


def _get_latest_vote(parser, token, expression):
    """
    Used by *get_latest_votes_for* and *get_latest_votes_by* templatetags:
    they use the same node.
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        error = u"%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, error
    # args validation
    match = expression.match(arg)
    if not match:
        error = u"%r tag has invalid arguments" % tag_name
        raise template.TemplateSyntaxError, error
    # to the node
    return LatestVotesNode(**match.groupdict())
    
class LatestVotesNode(template.Node):
    def __init__(self, key, varname, target_object=None, user=None):
        assertion = 'This node must be called with either target_object or user'
        assert target_object or user, assertion
        # target object
        self.target_object = None
        if target_object:
            self.target_object = template.Variable(target_object)
        # user
        self.user = None
        if user:
            self.user = template.Variable(user)
        # key
        self.key_variable = None
        if key is None:
            self.key = None
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # varname
        self.varname = varname
        
    def _get_key_lookup(self, context):
        lookups = {}
        if self.key_variable:
            lookups['key'] = self.key_variable.resolve(context)
        elif self.key is not None:
            lookups['key'] = self.key
        return lookups
        
    def render(self, context):
        lookups = self._get_key_lookup(context)
        if self.target_object:
            target_object = self.target_object.resolve(context)
            # validating given args
            handler = handlers.ratings.get_handler(type(target_object))
            if handler:
                # getting the latest votes
                latest_votes = handler.get_votes_for(target_object, **lookups)
                context[self.varname] = latest_votes.order_by('modified_at')
        else:
            user = self.user.resolve(context)
            latest_votes = handlers.ratings.get_votes_by(user, **lookups)
            context[self.varname] = latest_votes.order_by('modified_at')
        return u''


VOTES_ANNOTATE_PATTERN = r"""
    ^ # begin of line
    (?P<queryset>\w+) # queryset
    \s+with\s+(?P<field>\w+) # fields mapping
    \s+for\s+(?P<user>[\w\.]+) # user
    \s+using\s+(?P<key>[\w'"]+) # key
    (\s+ordering\s+by\s+(?P<order_by>[\w\-'",]+))? # order
    (\s+as\s+(?P<varname>\w+))? # varname
    $ # end of line
"""
VOTES_ANNOTATE_EXPRESSION = re.compile(VOTES_ANNOTATE_PATTERN, re.VERBOSE)
 
@register.tag
def votes_annotate(parser, token):
    """
    Use this templatetag when you need to update a queryset in bulk 
    adding vote values given by a particular user, e.g:
    
    .. code-block:: html+django
    
        {% votes_annotate queryset with 'user_score' for myuser using 'main' %}
        
    After this call each queryset instance has a *user_score* attribute
    containing the score given by *myuser* for the key 'main'.
    The score field name and the key can also be passed as 
    template variables, without quotes, e.g.:
    
    .. code-block:: html+django
    
        {% votes_annotate queryset with score_var for user using key_var %}
    
    You can also specify a new context variable for the modified queryset, e.g.:
    
    .. code-block:: html+django
    
        {% votes_annotate queryset with 'user_score' for user using 'main' as new_queryset %}
        {% for instance in new_queryset %}
            User's score: {{ instance.user_score }}
        {% endfor %}
                
    Finally, you can also sort the queryset, e.g.:
    
    .. code-block:: html+django
    
        {% votes_annotate queryset with 'myscore' for user using 'main' ordering by '-myscore' %}
        
    The order of arguments is important: the following example shows how
    to use this tempaltetag with all arguments:
    
    .. code-block:: html+django
    
        {% votes_annotate queryset with 'score' for user using 'main' ordering by 'score' as new_queryset %}
        
    Note: it is not possible to annotate querysets with anonymous votes.
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        error = u"%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, error
    # args validation
    match = VOTES_ANNOTATE_EXPRESSION.match(arg)
    if not match:
        error = u"%r tag has invalid arguments" % tag_name
        raise template.TemplateSyntaxError, error
    # to the node
    return VotesAnnotateNode(**match.groupdict())

class VotesAnnotateNode(template.Node):
    def __init__(self, field, queryset, user, key, order_by, varname):
        # field
        self.field_variable = None
        if field[0] in ('"', "'") and field[-1] == field[0]:
            self.field = field[1:-1]
        else:
            self.field_variable = template.Variable(field)
        # queryset
        self.queryset = template.Variable(queryset)
        # user
        self.user = template.Variable(user)
        # key
        self.key_variable = None
        if key[0] in ('"', "'") and key[-1] == key[0]:
            self.key = key[1:-1]
        else:
            self.key_variable = template.Variable(key)
        # ordering
        self.order_by_variable = None
        if order_by is None:
            self.order_by = None
        elif order_by[0] in ('"', "'") and order_by[-1] == order_by[0]:
            self.order_by = order_by[1:-1]
        else:
            self.order_by = template.Variable(order_by)
        # varname
        self.varname = varname or queryset
        
    def render(self, context):
        # field
        if self.field_variable is None:
            field = self.field
        else:
            field = self.field_variable.resolve(context)
        # queryset
        queryset = self.queryset.resolve(context)
        # user
        user = self.user.resolve(context)
        # handler
        handler = handlers.ratings.get_handler(queryset.model)
        # if user is anonymous or model is not handled 
        #then the original queryset is returned
        if handler is not None and user.is_authenticated():
            # key
            if self.key_variable is None:
                key = self.key
            else:
                key = self.key_variable.resolve(context)
            # annotation
            queryset = handler.annotate_votes(queryset, key, user, score=field)
            # ordering
            if self.order_by_variable:
                queryset = queryset.order_by(
                    *self.order_by_variable.resolve(context).split(','))
            elif self.order_by is not None:
                queryset = queryset.order_by(*self.order_by.split(','))
        # returning queryset
        context[self.varname] = queryset
        return u''


# STARRATING

@register.inclusion_tag("ratings/star_widget.html")
def show_starrating(score_or_vote, stars=None, split=None):
    """
    Show the starrating widget in read-only mode for the given *score_or_vote*.
    If *score_or_vote* is a score instance, then the average score is displayed.
    
    Usage:
    
    .. code-block:: html+django
    
        {# show star rating for the given vote #}
        {% show_starrating vote %}
        
        {# show star rating for the given score #}
        {% show_starrating score %}
        
        {# show star rating for the given score, using 10 stars with half votes #}
        {% show_starrating score 10 2 %}
    
    Normally the handler is used to get the number of stars and the how each 
    one must be splitted, but you can override using *stars* and *split*
    arguments.
    """
    model = score_or_vote.content_type.model_class()
    handler = handlers.ratings.get_handler(model)
    if handler:
        # getting *max_value* and *step*
        max_value = stars or handler.score_range[1]
        if split:
            from decimal import Decimal
            step = Decimal(1) / split
        else:
            step =  handler.score_step
        # using starrating widget displaying it in read-only mode
        from ratings.forms import StarWidget
        widget = StarWidget(1, max_value, step, score_or_vote.content_object,
            can_delete_vote=handler.can_delete_vote, read_only=True)
        # duck taking the score value
        try:
            value = score_or_vote.average
        except AttributeError:
            value = score_or_vote.score
        # the widget has a *get_context* method: how lucky we are!
        return widget.get_context(u'score', value, {'id': u'id_score'})
    return {}
