from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

def change_url(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return urlresolvers.reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(obj.pk,))

def delete_url(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return urlresolvers.reverse('admin:%s_%s_delete' % (content_type.app_label, content_type.model), args=(obj.pk,))
