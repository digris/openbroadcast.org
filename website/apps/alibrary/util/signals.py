# library post save

from filer.models.foldermodels import Folder

def library_post_save(sender, **kwargs):

    obj = kwargs['instance']
    
    #if not obj.folder:
    #    app_folder, created = Folder.objects.get_or_create(name=obj._meta.app_label)
    #    model_folder, created = Folder.objects.get_or_create(name=obj._meta.object_name.lower(), parent=app_folder)
    #    obj.folder, created = Folder.objects.get_or_create(name=obj.uuid, parent=model_folder)
    #    obj.save()
