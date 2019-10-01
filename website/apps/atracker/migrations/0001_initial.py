# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                ("archived", models.BooleanField(default=False)),
                ("distributed", models.BooleanField(default=False)),
                ("object_id", models.PositiveIntegerField(null=True, blank=True)),
                ("event_object_id", models.PositiveIntegerField(null=True, blank=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        related_name="event_content_objects",
                        blank=True,
                        to="contenttypes.ContentType",
                        null=True,
                    ),
                ),
                (
                    "event_content_type",
                    models.ForeignKey(
                        related_name="event_objects",
                        blank=True,
                        to="contenttypes.ContentType",
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "permissions": (
                    ("track_for_user", "Can create events in behalf of other user"),
                ),
            },
        ),
        migrations.CreateModel(
            name="EventType",
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
                    "title",
                    models.SlugField(
                        help_text='Please use a slugified name, e.g. "student-news".',
                        unique=True,
                        max_length=255,
                        verbose_name="Title",
                    ),
                ),
            ],
            options={
                "ordering": ("title",),
                "verbose_name": "Event Type",
                "verbose_name_plural": "Event Types",
            },
        ),
        migrations.AddField(
            model_name="event",
            name="event_type",
            field=models.ForeignKey(
                related_name="events", verbose_name="Type", to="atracker.EventType"
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="user",
            field=models.ForeignKey(
                related_name="atracker_events",
                verbose_name="User",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
        ),
    ]
