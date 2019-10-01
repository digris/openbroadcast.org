# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import importer.models
import django_extensions.db.fields.json
import django.db.models.deletion
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("alibrary", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Import",
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
                ("uuid_key", models.CharField(max_length=60, null=True, blank=True)),
                (
                    "status",
                    models.PositiveIntegerField(
                        default=0,
                        choices=[
                            (0, "Init"),
                            (1, "Done"),
                            (2, "Ready"),
                            (3, "Progress"),
                            (99, "Error"),
                            (11, "Other"),
                        ],
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        default="web",
                        max_length=10,
                        choices=[
                            ("web", "Web Interface"),
                            ("api", "API"),
                            ("fs", "Filesystem"),
                        ],
                    ),
                ),
                ("notes", models.TextField(null=True, blank=True)),
                (
                    "collection_name",
                    models.CharField(max_length=250, null=True, blank=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        related_name="import_user",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
                "verbose_name": "Import",
                "verbose_name_plural": "Imports",
            },
        ),
        migrations.CreateModel(
            name="ImportFile",
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
                (
                    "status",
                    models.PositiveIntegerField(
                        default=0,
                        choices=[
                            (0, "Init"),
                            (1, "Done"),
                            (2, "Ready"),
                            (3, "Working"),
                            (4, "Warning"),
                            (5, "Duplicate"),
                            (6, "Queued"),
                            (7, "Importing"),
                            (99, "Error"),
                            (11, "Other"),
                        ],
                    ),
                ),
                ("filename", models.CharField(max_length=1024, null=True, blank=True)),
                (
                    "file",
                    models.FileField(
                        storage=importer.models.UnuspiciousStorage(),
                        max_length=1024,
                        upload_to=importer.models.clean_upload_path,
                    ),
                ),
                ("mimetype", models.CharField(max_length=100, null=True, blank=True)),
                (
                    "messages",
                    django_extensions.db.fields.json.JSONField(
                        default=None, null=True, blank=True
                    ),
                ),
                (
                    "settings",
                    django_extensions.db.fields.json.JSONField(
                        default=dict, null=True, blank=True
                    ),
                ),
                (
                    "results_tag",
                    django_extensions.db.fields.json.JSONField(
                        default=dict, null=True, blank=True
                    ),
                ),
                (
                    "results_tag_status",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Result Tags (ID3 & co)",
                        choices=[
                            (0, "Init"),
                            (1, "Done"),
                            (2, "Ready"),
                            (3, "Progress"),
                            (99, "Error"),
                            (11, "Other"),
                        ],
                    ),
                ),
                (
                    "results_acoustid",
                    django_extensions.db.fields.json.JSONField(
                        default=dict, null=True, blank=True
                    ),
                ),
                (
                    "results_acoustid_status",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Result Musicbrainz",
                        choices=[
                            (0, "Init"),
                            (1, "Done"),
                            (2, "Ready"),
                            (3, "Progress"),
                            (99, "Error"),
                            (11, "Other"),
                        ],
                    ),
                ),
                (
                    "results_musicbrainz",
                    django_extensions.db.fields.json.JSONField(
                        default=dict, null=True, blank=True
                    ),
                ),
                (
                    "results_discogs_status",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Result Musicbrainz",
                        choices=[
                            (0, "Init"),
                            (1, "Done"),
                            (2, "Ready"),
                            (3, "Progress"),
                            (99, "Error"),
                            (11, "Other"),
                        ],
                    ),
                ),
                (
                    "results_discogs",
                    django_extensions.db.fields.json.JSONField(
                        default=dict, null=True, blank=True
                    ),
                ),
                (
                    "import_tag",
                    django_extensions.db.fields.json.JSONField(
                        default=dict, null=True, blank=True
                    ),
                ),
                (
                    "imported_api_url",
                    models.CharField(max_length=512, null=True, blank=True),
                ),
                ("error", models.CharField(max_length=512, null=True, blank=True)),
                (
                    "import_session",
                    models.ForeignKey(
                        related_name="files",
                        verbose_name="Import",
                        to="importer.Import",
                        null=True,
                    ),
                ),
                (
                    "media",
                    models.ForeignKey(
                        related_name="importfile_media",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to="alibrary.Media",
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ("created",),
                "verbose_name": "Import File",
                "verbose_name_plural": "Import Files",
            },
        ),
        migrations.CreateModel(
            name="ImportItem",
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
                ("object_id", models.PositiveIntegerField()),
                ("content_type", models.ForeignKey(to="contenttypes.ContentType")),
                (
                    "import_session",
                    models.ForeignKey(
                        related_name="importitem_set",
                        verbose_name="Import",
                        to="importer.Import",
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Import Item",
                "verbose_name_plural": "Import Items",
            },
        ),
    ]
