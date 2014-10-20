from django.db import models

from cms.utils.helpers import reversion_register


class FileModel(models.Model):
    test_file = models.FileField(upload_to='fileapp/', blank=True, null=True)

reversion_register(FileModel)
