from django.db import models

class Timestamped(models.Model):
    
    # auto-update
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        app_label = 'lib'
        abstract = True