from django.db import models

# Create your models here.

class Documentation(models.Model):

    name = models.CharField(max_length=256, null=True)
    slug = models.SlugField()
    public = models.BooleanField(default=True)
    path = models.CharField(max_length=1024)
