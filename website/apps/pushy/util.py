from pushy import settings as pushy_settings
from pushy.models import pushy_publish

def pushy_custom(route, body=None, type='update'):
    
    message = {
           'route': route,
           'type': type,
           'body': body
           }
    
    print message
    
    print pushy_publish(pushy_settings.get_channel(), type, message)
    
    print 'done'