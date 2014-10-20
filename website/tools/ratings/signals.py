"""
Signals relating to ratings.
"""
from django.dispatch import Signal

# fired before a vote is saved
vote_will_be_saved = Signal(providing_args=['vote', 'request'])
# fired after a vote is saved
vote_was_saved = Signal(providing_args=['vote', 'request', 'created'])
# fired before a vote is deleted
vote_will_be_deleted = Signal(providing_args=['vote', 'request'])
# fired after a vote is deleted
vote_was_deleted = Signal(providing_args=['vote', 'request'])
