from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class Panel(CMSPlugin):

	extra_classes = models.CharField(max_length=100, null=True, blank=True)

	def get_extra_classes(self, separator=" "):
		return separator.join(self.extra_classes.split(','))

