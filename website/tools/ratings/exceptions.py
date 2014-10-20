class RatingsError(Exception):
    """
    Base exception class for genric ratings app.
    """
    pass
        
class AlreadyHandled(RatingsError):
    """
    Raised when a model which is already registered for ratings is
    attempting to be registered again.
    """
    pass

class NotHandled(RatingsError):
    """
    Raised when a model which is not registered for ratings is
    attempting to be unregistered.
    """
    pass

class DataError(RatingsError):
    """
    Something went really wrong...
    """
    pass