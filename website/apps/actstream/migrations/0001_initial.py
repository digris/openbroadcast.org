# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("actor_object_id", models.CharField(max_length=255)),
                ("verb", models.CharField(max_length=255)),
                ("description", models.TextField(null=True, blank=True)),
                (
                    "target_object_id",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "action_object_object_id",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("public", models.BooleanField(default=True)),
                ("data", jsonfield.fields.JSONField(null=True, blank=True)),
                (
                    "action_object_content_type",
                    models.ForeignKey(
                        related_name="action_object",
                        blank=True,
                        to="contenttypes.ContentType",
                        null=True,
                    ),
                ),
                (
                    "actor_content_type",
                    models.ForeignKey(
                        related_name="actor", to="contenttypes.ContentType"
                    ),
                ),
                (
                    "target_content_type",
                    models.ForeignKey(
                        related_name="target",
                        blank=True,
                        to="contenttypes.ContentType",
                        null=True,
                    ),
                ),
            ],
            options={"ordering": ("-timestamp",)},
        ),
        migrations.CreateModel(
            name="Follow",
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
                ("object_id", models.CharField(max_length=255)),
                (
                    "actor_only",
                    models.BooleanField(
                        default=True,
                        verbose_name=b"Only follow actions where the object is the target.",
                    ),
                ),
                ("started", models.DateTimeField(default=django.utils.timezone.now)),
                ("content_type", models.ForeignKey(to="contenttypes.ContentType")),
                ("user", models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="follow", unique_together=set([("user", "content_type", "object_id")])
        ),
    ]
