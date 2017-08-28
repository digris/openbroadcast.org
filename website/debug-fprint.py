from importer.models import ImportFile
from importer.util.identifier import Identifier


ifile = ImportFile.objects.last()

i = Identifier()

i.id_by_fprint(ifile.file)
