from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from importer.models import ImportFile

@dajaxice_register
def get_import(request, *args, **kwargs):

    data = []
    for import_file in ImportFile.objects.all():
        data.append({'id': import_file.pk, 'status': import_file.status})

    data = simplejson.dumps(data)

    return data
