# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
                ),
                ("name", models.CharField(max_length=250, db_index=True)),
                ("slug", models.SlugField(editable=False, blank=True)),
                (
                    "visibility",
                    models.PositiveIntegerField(
                        default=0, choices=[(0, "private"), (1, "public")]
                    ),
                ),
                ("description", models.TextField(null=True, blank=True)),
            ],
            options={
                "ordering": ("name",),
                "verbose_name": "Collection",
                "verbose_name_plural": "Collections",
            },
        ),
        migrations.CreateModel(
            name="CollectionItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("content_type", models.ForeignKey(to="contenttypes.ContentType")),
            ],
            options={
                "verbose_name": "Collection Item",
                "verbose_name_plural": "Collection Items",
            },
        ),
        migrations.CreateModel(
            name="CollectionMaintainer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("collection", models.ForeignKey(to="collection.Collection")),
                ("user", models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="CollectionMember",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        related_name="members", to="collection.Collection"
                    ),
                ),
                ("item", models.ForeignKey(to="collection.CollectionItem")),
            ],
        ),
        migrations.AddField(
            model_name="collection",
            name="items",
            field=models.ManyToManyField(
                to="collection.CollectionItem",
                through="collection.CollectionMember",
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="collection",
            name="maintainers",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL,
                through="collection.CollectionMaintainer",
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="collection",
            name="owner",
            field=models.ForeignKey(
                related_name="owned_collections", to=settings.AUTH_USER_MODEL, null=True
            ),
        ),
        migrations.AlterUniqueTogether(
            name="collectionmember", unique_together=set([("collection", "item")])
        ),
    ]
