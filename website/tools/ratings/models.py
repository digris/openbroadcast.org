import string

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.datastructures import SortedDict
from django.contrib.auth.models import User

from ratings import managers

# MODELS

class Score(models.Model):
    """
    A score for a content object.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    key = models.CharField(max_length=16)
    
    average = models.FloatField(default=0)
    total = models.IntegerField(default=0)
    num_votes = models.PositiveIntegerField(default=0)
    
    # manager
    objects = managers.RatingsManager()
        
    class Meta:
        unique_together = ('content_type', 'object_id', 'key')

    def __unicode__(self):
        return u'Score for %s' % self.content_object
        
    def get_votes(self):
        """
        Return all the related votes (same *content_object* and *key*).
        """
        return Vote.objects.filter(content_type=self.content_type,
            object_id=self.object_id, key=self.key)
    
    def recalculate(self, weight=0, commit=True):
        """
        Recalculate the score using all the related votes, and updating
        average score, total score and number of votes.
        
        The optional argument *weight* is used to calculate the average
        score: an higher value means a lot of votes are needed to increase
        the average score of the target object.
        
        If the optional argument *commit* is False then the object
        is not saved.
        """
        data = self.get_votes().aggregate(total=models.Sum('score'), 
            num_votes=models.Count('id'))
        # total is None in MySQL if there are no votes
        self.total = data['total'] or 0
        self.num_votes = data['num_votes']
        if self.num_votes:
            self.average = self.total / (self.num_votes + weight)
        else:
            self.average = 0
        if commit:
            self.save()
        
    def get_stats(self):
        """
        Return useful statistics for all the related votes 
        (same *content_object* and *key*). as a *SortedDict* mapping
        the single score with stats, e.g.::
    
            1.0: {
                'score': 1.0, 
                'percent': 37.5, 
                'total_num_votes': 8, 
                'num_votes': 3
            }
        """
        return get_stats_for(self.get_votes(), num_votes=self.num_votes)
        
        
class Vote(models.Model):
    """
    A single vote relating a content object.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    key = models.CharField(max_length=16)
    score = models.FloatField()

    user = models.ForeignKey(User, blank=True, null=True, related_name='votes')
    ip_address = models.IPAddressField(null=True)
    cookie = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # manager
    objects = managers.RatingsManager()
    
    class Meta:
        unique_together = (
            ('content_type', 'object_id', 'key', 'user'),
            ('content_type', 'object_id', 'key', 'ip_address', 'cookie'),
        )

    def __unicode__(self):
        return u'Vote %d to %s by %s' % (self.score, self.content_object,
            self.user or self.ip_address)
            
    def get_score(self):
        """
        Return the score related to current *content_object* and *key*.
        Return None if score does not exist.
        """
        if not hasattr(self, '_score_cache'):
            try:
                self._score_cache = Score.objects.get(key=self.key, 
                    content_type=self.content_type, object_id=self.object_id)
            except Score.DoesNotExist:
                self._score_cache = None
        return self._score_cache
        
    def by_anonymous(self):
        """
        Return True if this vote is given by an anonymous user.
        """
        return not self.user_id
        

# UTILS

def _get_content(instance_or_content):
    """
    Given a model instance or a sequence *(content_type, object_id)*
    return a tuple *(content_type, object_id)*.
    """
    try:
        object_id = instance_or_content.pk
    except AttributeError:
        return instance_or_content
    else:
        return (managers.get_content_type_for_model(type(instance_or_content)), 
            object_id)
 

# STATS         
            
def get_stats_for(votes, num_votes=None):
    """
    Return useful statistics for given *votes* as a *SortedDict* mapping
    the single score with stats, e.g.::
    
        1.0: {
            'score': 1.0, 
            'percent': 37.5, 
            'total_num_votes': 8, 
            'num_votes': 3
        }
    """
    if num_votes is None:
        try:
            num_votes = votes.count()
        except AttributeError:
            num_votes = len(votes)
    votes_stats = votes.order_by('score').values('score').annotate(
        num_votes=models.Count('score'))
    stats = SortedDict()
    for i in votes_stats:
        i.update({
            'total_num_votes': num_votes,
            'percent': i['num_votes'] * 100.0 / num_votes,
        })
        stats[i['score']] = i
    return stats
        
        
# ADDING OR CHANGING SCORES AND VOTES

def upsert_score(instance_or_content, key, weight=0):
    """
    Update or create current score values (average score, total score and 
    number of votes) for target object *instance_or_content* and 
    the given *key*. 
    
    The argument *instance_or_content* can be a model instance or 
    a sequence *(content_type, object_id)*.
    
    You can use the optional argument *weight* to make more difficult
    for a target object to obtain a higher rating.
    
    Return a sequence *score, created*.
    """
    content_type, object_id = _get_content(instance_or_content)
    score, created = Score.objects.get_or_create(content_type=content_type,
        object_id=object_id, key=key)
    score.recalculate(weight=weight)
    return score, created


# DELETING SCORES AND VOTES

def delete_scores_for(instance_or_content):
    """
    Delete all score objects related to *instance_or_content*, that can be 
    a model instance or a sequence *(content_type, object_id)*.
    """
    content_type, object_id = _get_content(instance_or_content)
    Score.objects.filter(content_type=content_type, object_id=object_id).delete()
    
def delete_votes_for(instance_or_content):
    """
    Delete all vote objects related to *instance_or_content*, that can be 
    a model instance or a sequence *(content_type, object_id)*.
    """
    content_type, object_id = _get_content(instance_or_content)
    Vote.objects.filter(content_type=content_type, object_id=object_id).delete()

# IN BULK SELECT QUERIES
    
def annotate_scores(queryset_or_model, key, **kwargs):
    """
    Annotate *queryset_or_model* with scores, in order to retreive from
    the database all score values in bulk.

    The first argument *queryset_or_model* must be, of course, a queryset
    or a Django model object. The argument *key* is the score key.
    
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
    """
    # getting the queryset
    if isinstance(queryset_or_model, models.base.ModelBase):
        queryset = queryset_or_model.objects.all()
    else:
        queryset = queryset_or_model
    # annotations are done only if fields are requested
    if kwargs:
        # preparing arguments for *extra* query
        select = SortedDict() # not really needed (see below)
        select_params = []
        opts = queryset.model._meta
        content_type = managers.get_content_type_for_model(queryset.model)
        mapping = {
            'score_table': Score._meta.db_table,
            'model_table': opts.db_table,
            'model_pk_name': opts.pk.name,
            'content_type_id': content_type.pk,
        }
        # building base query
        template = """
        SELECT ${field_name} FROM ${score_table} WHERE 
        ${score_table}.object_id = ${model_table}.${model_pk_name} AND 
        ${score_table}.content_type_id = ${content_type_id} AND
        ${score_table}.key = %s
        """
        template = string.Template(template).safe_substitute(mapping)
        # building one query for each requested field
        for alias, field_name in kwargs.items():
            query = string.Template(template).substitute(
                {'field_name': field_name})
            select[alias] = query
            # and that's why SortedDict are not really needed
            select_params.append(key) 
        return queryset.extra(select=select, select_params=select_params)
    return queryset
    
def annotate_votes(queryset_or_model, key, user, score='score'):
    """
    Annotate *queryset_or_model* with votes, in order to retreive from
    the database all vote values in bulk.
    
    The first argument *queryset_or_model* must be, of course, a queryset
    or a Django model object. The argument *key* is the score key.
    
    The votes are filtered using given *user*. For anonymous voters this
    functionality is unavailable.
    
    The score itself will be present in the attribute named *score* of 
    each instance of the returned queryset.
    
    Usage example::
    
        for article in annotate_votes(Article.objects.all(), 'main', myuser, 
            score='myscore'):
            print 'your vote:', article.myscore    
    """
    # getting the queryset
    if isinstance(queryset_or_model, models.base.ModelBase):
        queryset = queryset_or_model.objects.all()
    else:
        queryset = queryset_or_model
    # preparing arguments for *extra* query
    opts = queryset.model._meta
    content_type = managers.get_content_type_for_model(queryset.model)
    mapping = {
        'vote_table': Vote._meta.db_table,
        'model_table': opts.db_table,
        'model_pk_name': opts.pk.name,
        'content_type_id': content_type.pk,
    }
    # building base query
    template = """
    SELECT score FROM ${vote_table} WHERE 
    ${vote_table}.object_id = ${model_table}.${model_pk_name} AND 
    ${vote_table}.content_type_id = ${content_type_id} AND
    ${vote_table}.user_id = %s AND
    ${vote_table}.key = %s
    """
    select = {score: string.Template(template).substitute(mapping)}
    return queryset.extra(select=select, select_params=[user.pk, key])
    

# ABSTRACT MODELS
    
class RatedModel(models.Model):
    """
    Mixin for votable models.
    """
    rating_scores = generic.GenericRelation(Score)
    rating_votes = generic.GenericRelation(Vote)
    
    class Meta:
        abstract = True 
        
    def get_score(self, key):
        """
        Return the score for the current model instance and *key*.
        Useful attrs:
        
            - self.get_score(mykey).average
            - self.get_score(mykey).total
            - self.get_score(mykey).num_votes
            
        If score does not exist, return None.
        """
        return Score.objects.get_for(self, key)
