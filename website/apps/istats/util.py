from istats import settings as istats_settings
from istats.models import istats_publish

def istats_custom(route, body=None, type='update'):
    
    message = {
           'route': route,
           'type': type,
           'body': body
           }
    
    print message
    
    print istats_publish(istats_settings.get_channel(), type, message)
    
    print 'done'