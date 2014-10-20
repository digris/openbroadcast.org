from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from genericrelations.admin import GenericTabularInline

"""
https://github.com/jschrewe/django-genericadmin

Usage:
a = Article.objects.get(pk=1)
ct = ContentType.objects.get_for_model(a)

UP:
rc = RelatedContent.objects.filter(content_type__pk=ct.id,object_id=a.id)

DOWN:
rc = RelatedContent.objects.filter(parent_content_type=ct,parent_object_id=a.id)

rc[0].content_object.get_absolute_url()
"""

class RelatedContent(models.Model):
    """
    Relates any one entry to another entry irrespective of their individual models.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    parent_content_type = models.ForeignKey(ContentType, related_name="parent_test_link")
    parent_object_id = models.PositiveIntegerField()
    parent_content_object = generic.GenericForeignKey('parent_content_type', 'parent_object_id')

    def __unicode__(self):
        return "%s: %s" % (self.content_type.name, self.content_object)
    
class RelatedContentInline(GenericTabularInline):
    model = RelatedContent
    ct_field = 'parent_content_type'
    ct_fk_field = 'parent_object_id'