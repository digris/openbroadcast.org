from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

# Create your models here.
class Backfeed(models.Model):

    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    user = models.ForeignKey(User, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    class Meta:
        app_label = 'backfeed'
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
        ordering = ('-created', )

    def __unicode__(self):
        return self.subject