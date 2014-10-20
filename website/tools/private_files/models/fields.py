import os

from django.db.models.fields.files import FileField, FieldFile
from django.core.urlresolvers import reverse

PROTECTION_METHODS = ['basic', 'nginx', 'lighttpd', 'apache']

class PrivateFieldFile(FieldFile):
    def _get_url(self):
        self._require_file()
        app_label = self.instance._meta.app_label
        model_name  = self.instance._meta.object_name.lower()
        field_name = self.field.name
        pk = self.instance.pk
        filename = os.path.basename(self.path)
        return reverse('private_files-file', args=[app_label, model_name, field_name, pk, filename])
        

    url = property(_get_url)
    
    def _get_contidion(self):
        return self.field.condition

    condition = property(_get_contidion) 
   
    def _get_attachment(self):
        return self.field.attachment
    
    attachment = property(_get_attachment)
    


def is_user_authenticated(request, instance):
    return (not request.user.is_anonymous()) and request.user.is_authenticated

class PrivateFileField(FileField):
    attr_class = PrivateFieldFile
    
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, condition = is_user_authenticated, attachment = True, **kwargs):
        super(PrivateFileField, self).__init__(verbose_name, name, upload_to, storage, **kwargs)
        self.condition = condition
        self.attachment = attachment



from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^private_files\.models\.fields\.PrivateFileField"])