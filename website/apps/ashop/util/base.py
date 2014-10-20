from django.contrib.auth.models import AnonymousUser

from alibrary.models import Release
from shop.models.ordermodel import Order


"""
check if user is allowed to download
TODO: make more efficient for anonymous users (e.g. cache etc)
"""
def get_download_permissions(request, product, format, version):
    
    can_download = False

    
    if request.user and not isinstance(request.user, AnonymousUser):
        if request.user.has_perm('download', product):
            pass
            can_download = True
            
        # check for related release-permission
        try:
            if request.user.has_perm('download', product.media.release.releaseproduct.filter(downloadrelease__format__format=format, downloadrelease__active=True)[0]):
                can_download = True
        except Exception, e:
            print e
            pass

    else:
        session = getattr(request, 'session', None)
        
        if session != None:
            order_id = session.get('order_id')
            
            if order_id:
                
                order = Order.objects.get(pk=order_id)
                order_releases = Release.objects.filter(pk=product.releaseproduct.id, releaseproduct__orderitem__order=order) 
                
                if len(order_releases) >= 1:
                    can_download = True

    return can_download


"""
returns downloadable objects (object = Release or Track model)
"""
def get_object_products(request, object):
    
    products = []
    
    try:
        for product in object.mediaproduct.all():
            
            action = 'buy'
            
            print product.format
            
            try:
                # check if permission
                if request.user.has_perm('download', product):
                    action = 'download'
    
                # check for related release-permission
                if request.user.has_perm('download', product.media.release.releaseproduct.filter(downloadrelease__format=product.format, downloadrelease__active=True)[0]):
                    action = 'download'
                    
                    
            except Exception, e:
                print e
                pass
                
            tproduct = {'product': product, 'action': action}
            products.append(tproduct)
              
    except Exception, e:
        print e
        pass
    
    try:
        for product in object.releaseproduct.all():
            
            action = 'buy'
            
            # check if permission
            if request.user and not isinstance(request.user, AnonymousUser):
                if request.user.has_perm('download', product):
                    action = 'download'
                
            tproduct = { 'product': product, 'action': action }
            products.append(tproduct)
              
              
    except Exception, e:
        print e
        pass


    return products