from django.conf import settings

# set to False to allow votes only by authenticated users
ALLOW_ANONYMOUS = getattr(settings, 'GENERIC_RATINGS_ALLOW_ANONYMOUS', False)

# a sequence of minimum and maximum values available for scores
SCORE_RANGE = getattr(settings, 'GENERIC_RATINGS_SCORE_RANGE', (1, 5))

# step allowed in scores
SCORE_STEP = getattr(settings, 'GENERIC_RATINGS_SCORE_STEP', 1)

# the weight used to calculate average score
WEIGHT = getattr(settings, 'GENERIC_RATINGS_WEIGHT', 0)

# default key to use for votes when there is only one vote-per-content
DEFAULT_KEY = getattr(settings, 'GENERIC_RATINGS_DEFAULT_KEY', 'main')

# querystring key that can contain the url of the redirection 
# performed after voting
NEXT_QUERYSTRING_KEY = getattr(settings, 
    'GENERIC_RATINGS_NEXT_QUERYSTRING_KEY', 'next')

# in case of anonymous users it is possible to limit votes per ip address 
# (0 = no limits)
VOTES_PER_IP_ADDRESS = getattr(settings, 
    'GENERIC_RATINGS_VOTES_PER_IP_ADDRESS', 0)

# the pattern used to create a cookie name
COOKIE_NAME_PATTERN = getattr(settings, 'GENERIC_RATINGS_COOKIE_NAME_PATTERN', 
    'grvote_%(model)s_%(object_id)s_%(key)s')

# the cookie max age (number of seconds) for anonymous votes
COOKIE_MAX_AGE = getattr(settings, 'GENERIC_RATINGS_COOKIE_MAX_AGE', 
    60 * 60 * 24 * 365) # one year