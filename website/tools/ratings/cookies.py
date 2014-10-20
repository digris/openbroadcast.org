import datetime

from django.utils.crypto import salted_hmac

from ratings import settings

def get_name(instance, key):
    """
    Return a cookie name for anonymous vote of *instance* using *key*.
    """
    mapping = {
        'model': str(instance._meta),
        'object_id': instance.pk,
        'key': key,
    }
    return settings.COOKIE_NAME_PATTERN % mapping

def get_value(ip_address):
    """
    Return a cookie value for an anonymous vote.
    """
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return salted_hmac("gr.cookie", "%s-%s" % (now, ip_address)).hexdigest()