import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.conf import settings
from base.mixins import TimestampedModelMixin, UUIDModelMixin

log = logging.getLogger(__name__)


USER_MODEL = settings.AUTH_USER_MODEL


class Collection(TimestampedModelMixin, UUIDModelMixin, models.Model):
    PRIVATE = 0
    PUBLIC = 1
    VISIBILITY_CHOICES = ((PRIVATE, "private"), (PUBLIC, "public"))

    name = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(editable=False, blank=True)
    visibility = models.PositiveIntegerField(
        default=PRIVATE, choices=VISIBILITY_CHOICES
    )
    description = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(USER_MODEL, related_name="owned_collections", null=True)
    items = models.ManyToManyField(
        "CollectionItem", through="CollectionMember", blank=True
    )
    maintainers = models.ManyToManyField(
        USER_MODEL, through="CollectionMaintainer", blank=True
    )

    class Meta:
        app_label = "collection"
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy(
            "collection:collection-detail", kwargs={"slug": self.slug or self.pk}
        )


class CollectionMember(TimestampedModelMixin, models.Model):
    collection = models.ForeignKey(
        "Collection", on_delete=models.CASCADE, related_name="members"
    )
    item = models.ForeignKey("CollectionItem", on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        app_label = "collection"
        unique_together = ("collection", "item")

    def __str__(self):
        return f"{self.collection.name} - {self.item.content_object}"


class CollectionItem(UUIDModelMixin, models.Model):
    class Meta:
        app_label = "collection"
        verbose_name = "Collection Item"
        verbose_name_plural = "Collection Items"

    ct_limit = (
        models.Q(app_label="alibrary", model="media")
        | models.Q(app_label="alibrary", model="release")
        | models.Q(app_label="alibrary", model="artist")
        | models.Q(app_label="alibrary", model="playlist")
    )

    content_type = models.ForeignKey(ContentType, limit_choices_to=ct_limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"<{self.content_type}> {self.content_object}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CollectionMaintainer(models.Model):
    collection = models.ForeignKey(Collection)
    user = models.ForeignKey(USER_MODEL)
