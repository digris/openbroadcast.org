import django.dispatch

importitem_created = django.dispatch.Signal(providing_args=['content_object', 'user', 'collection_name'])
